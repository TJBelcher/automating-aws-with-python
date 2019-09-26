#!/usr/bin/python
# -*- coding:  utf-8 -*-

"""Webotron:  Deploy websites with AWS.

Webotron automates the process of deploying static websites to AWS
- Configure AWS S3 buckets
  - Create them
  - Set them up for static website hosting
  - Deply local files to them
- Configure DNS with AWS Route 53
- Configure a Content Delivery Network and SSL with AWS Cloudfront
"""

from pathlib import Path
import mimetypes

import boto3
from botocore.exceptions import ClientError
import click           # for argument processing

SESSION = boto3.Session(profile_name='pythonAutomation')
S3 = SESSION.resource('s3')


@click.group()
def cli():
    """Webotron deploys websites to AWS."""


@cli.command('list-buckets')   # this is a decorator controlling execution
def list_buckets():
    """List all s3 buckets."""
    for bucket in S3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')     # this is a decorator that controls
# execution.  If not present the list_bucket_objects name would be used
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an s3 bucket."""
    for obj in S3.Bucket(bucket).objects.all():
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = None

    try:
        s3_bucket = S3.create_bucket(
            Bucket=bucket
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = S3.Bucket(bucket)
        else:
            raise error

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
    """ % s3_bucket.name
    policy = policy.strip()
    pol = s3_bucket.Policy()
    pol.put(Policy=policy)

    s3_bucket.Website().put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })


def upload_file(s3_bucket, path, key):
    """Upload file s3 bucket."""
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    print("s3_bucket.upload_file called with:",
          s3_bucket, path, key, content_type)
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
            'ContentType': content_type
        })


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
    print("'here we are in the sync code with this pathname and bucket:",
          pathname, bucket)
    s3_bucket = S3.Bucket(bucket)

    print('s3_bucket has been set to:', s3_bucket)
    root = Path(pathname).expanduser().resolve()
    print('root has been set to:', root)

    def handle_directory(target):
        """Constructs path name. """
        for path_1 in target.iterdir():
            if path_1.is_dir():
                handle_directory(path_1)
            if path_1.is_file():
                upload_file(s3_bucket, str(path_1),
                            str(path_1.relative_to(root)))

    handle_directory(root)


if __name__ == '__main__':
    cli()
