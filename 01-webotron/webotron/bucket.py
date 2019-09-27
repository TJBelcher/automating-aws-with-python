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

from botocore.exceptions import ClientError


class BucketManager:
    """Manage an S3 Bucket."""

    def __init__(self, SESSION):
        """Create a BucketManager object using passed session creds."""
        self.s_three = SESSION.resource('s3')

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

    @staticmethod
    def upload_file(bucket, path, key):
        """Upload file to s3 bucket."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        print("bucket.upload_file called with:",
              bucket, path, key, content_type)
        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            })

    def sync(self, pathname, bucket_name):
        """Sync contents of PATHNAME to BUCKET."""
        bucket = self.s_three.Bucket(bucket_name)

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
