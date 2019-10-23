# -*- coding: utf-8 -*-

"""bucket:  Utility functions for Deploying websites with AWS.

bucket provides subprograms to automate deploying static websites to AWS
- Configure AWS S3 buckets
  - Create them
  - Set them up for static website hosting
  - Deploy local files to them
"""


from pathlib import Path
import mimetypes
from functools import reduce

from botocore.exceptions import ClientError

from hashlib import md5
import util  # import util.py code
import boto3

class BucketManager:
    """Manage an S3 Bucket."""

    CHUNK_SIZE = 8388608

    def __init__(self, SESSION):
        """Create a BucketManager object using passed session creds."""
        self.s_three = SESSION.resource('s3')
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize=self.CHUNK_SIZE,
            multipart_threshold=self.CHUNK_SIZE
        )

        self.manifest = {}


    def get_region_name(self, bucket):
        """Get the bucket's region name."""
        client = self.s_three.meta.client
        bucket_location = client.get_bucket_location(Bucket=bucket.name)

        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self, bucket):
        """Generate bucket URL using Named Tuple."""
        return "http://{}.{}".format(bucket.name,
                                     util.get_endpoint
                                     (self.get_region_name(bucket)).host)

    def all_buckets(self):
        """Get an iterator for all buckets."""
        return self.s_three.buckets.all()

    def all_objects(self, bucket_name):
        """Get an iterator for all objects."""
        return self.s_three.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Initiate bucket creation."""
        s3_bucket = None
        try:
            s3_bucket = self.s_three.create_bucket(Bucket=bucket_name)
        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s_three.Bucket(bucket_name)
            else:
                raise error

        return s3_bucket

    @staticmethod
    def set_policy(bucket):
        """Apply web policies to bucket."""
        policy = """
        {
            "Version":"2012-10-17",
            "Statement":[{
            "Sid":"PublicReadGetObject",
            "Effect":"Allow",
            "Principal": "*",
                "Action":["s3:GetObject"],
                "Resource":["arn:aws:s3:::%s/*"
                ]
              }
           ]
        }
        """ % bucket.name
        policy = policy.strip()
        pol = bucket.Policy()
        pol.put(Policy=policy)

    @staticmethod
    def set_config(bucket):
        """Apply web config settings to bucket."""
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })

    def load_manifest(self, bucket):
        """Load manifest for caching purposes."""
        paginator = self.s_three.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                self.manifest[obj['Key']] = obj['ETag']

    @staticmethod
    def hash_data(data):
        """Generate md5 hash for data."""
        hash = md5()
        hash.update(data)

        return hash

    def gen_etag(self, path):
        """Generate etag for file."""
        hashes = []

        with open(path, 'rb') as f:   # open file for read binary mode
            while True:
                data = f.read(self.CHUNK_SIZE)

                if not data:
                    break

                hashes.append(self.hash_data(data))

        if not hashes:
            return
        elif len(hashes) == 1:
            return '"{}"'.format(hashes[0].hexdigest()) # '"{}"' prefix is
            # due to the double quotes inside the etag value string - using
            # format to perform string replacement at brackets
        else:  # below, all hashes are created and recursively concatanated
            # and then hashed again.  this is the process aws uses to get a hash
            # for a multi-part upload
            hash = self.hash_data(reduce(lambda x, y: x+y, (h.digest() for h in hashes)))
            # hash of hashes returned along with number of chunks in line below
            return '"{}-{}"'.format(hash.hexdigest(), len(hashes))

    def upload_file(self, bucket, path, key):
        """Upload file to s3 bucket."""
        print("upload-file with: ", bucket, path, key)
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        etag = self.gen_etag(path)
        # in line below, if hashes are equal then return, otherwise upload file
        if self.manifest.get(key, '') == etag:
            print("Skipping {}, etags match".format(key))
            return

        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            },
            Config=self.transfer_config
            )

    def sync(self, pathname, bucket_name):
        """Sync contents of PATHNAME to BUCKET."""
        bucket = self.s_three.Bucket(bucket_name)
        self.load_manifest(bucket)

        root = Path(pathname).expanduser().resolve()
        print('root has been set to:', root)

        def handle_directory(target):
            """Construct path name."""
            for path_1 in target.iterdir():
                if path_1.is_dir():
                    handle_directory(path_1)
                if path_1.is_file():
                    self.upload_file(bucket, str(path_1),
                                     str(path_1.relative_to(root)))

        handle_directory(root)
