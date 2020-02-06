# -*- coding: utf-8 -*-

"""Classes for S3 Buckets."""

from pathlib import Path
import mimetypes
from functools import reduce

import boto3
from botocore.exceptions import ClientError

from hashlib import md5
import util


class BucketManager:
    """Manage an S3 Bucket."""

    CHUNK_SIZE = 8388608

    def __init__(self, session):
        """Create a BucketManager object."""
        self.session = session
        self.s3 = self.session.resource('s3')
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize=self.CHUNK_SIZE,
            multipart_threshold=self.CHUNK_SIZE
        )

        self.manifest = {}

    def get_region_name(self, bucket):
        """Get region name for a bucket."""
        client = self.s3.meta.client
        bucket_location = client.get_bucket_location(Bucket=bucket.name)

        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self, bucket):
        """Get the website URL for this bucket."""
        return "http://{}.{}".format(
            bucket.name,
            util.get_endpoint(self.get_region_name(bucket)).host
            )

    def all_buckets(self):
        """Get an iterator for all buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket):
        """Get an iterator for all objects in a bucket."""
        return self.s3.Bucket(bucket).objects.all()

    def init_bucket(self, bucket_name):
        """Create new bucket or return exisitng one by name."""
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(
                Bucket=bucket_name
                # Bucket=bucket,
                # CreateBucketConfiguration={'LocationConstraint': 'us-east-2'}
            )
        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print(error)
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise error

        return s3_bucket

    @staticmethod
    def set_policy(bucket):
        """Set bucket policy to be readable by everyone."""
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
        # note - the % value just above is substituted into the policy at %s
        policy = policy.strip()

        pol = bucket.Policy()
        pol.put(Policy=policy)

    @staticmethod
    def configure_website(bucket):
        """Configure website for Error and Index documents."""
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
        paginator = self.s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                # pprint(obj)
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

        with open(path, 'rb') as f:
            while True:
                data = f.read(self.CHUNK_SIZE)

                if not data:
                    # print("path1")
                    break

                hashes.append(self.hash_data(data))

        if not hashes:
            # print("path2 - 0 byte file?")
            return
        elif len(hashes) == 1:
            # print("path3")
            return '"{}"'.format(hashes[0].hexdigest())
        else:
            # print("path4")
            hash = self.hash_data(reduce(lambda x, y: x + y,
                                 (h.digest() for h in hashes))
                                 )
            return '"{}-{}"'.format(hash.hexdigest(), len(hashes))


    def upload_file(self, bucket, path, key):
        """Upload object to S3 bucket."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        # print("path being uploaded is", path)
        # print("key being uploaded is:", key)
        etag = self.gen_etag(path)

        if self.manifest.get(key, '') == etag:
            print("Skipping upload of {}-{} as etags match".format(key, path))
            # note - if 0 byte file upload always occurs as local key is None
            return

        print("Uploading {}-{} etag mismatch or 0 byte file".format(key, path))
        print("Local Key:  ",etag)
        print("  AWS Key:  ",self.manifest.get(key, ''))
        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            },
            Config=self.transfer_config
        )

    def sync(self, pathname, bucket_name):
        """Sync local folder to S3 bucket."""
        bucket = self.s3.Bucket(bucket_name)
        self.load_manifest(bucket)

        root = Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for path in target.iterdir():
                if path.is_dir():
                    handle_directory(path)
                if path.is_file():
                    self.upload_file(bucket, str(path.as_posix()),
                                     str(path.relative_to(root).as_posix()))

        handle_directory(root)
