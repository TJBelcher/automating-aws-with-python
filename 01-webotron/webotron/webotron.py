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

import boto3
import click           # for argument processing

from bucket import BucketManager

SESSION = boto3.Session(profile_name='pythonAutomation')
BUCKET_MANAGER = BucketManager(SESSION)


@click.group()
def cli():
    """Webotron deploys websites to AWS."""


@cli.command('list-buckets')   # this is a decorator controlling execution
def list_buckets():
    """List all s3 buckets."""
    for bucket in BUCKET_MANAGER.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')     # this is a decorator that controls
# execution.  If not present the list_bucket_objects name would be used
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an s3 bucket."""
    for obj in BUCKET_MANAGER.all_objects(bucket):
        print(obj.bucket_name, " ", obj.key)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = BUCKET_MANAGER.init_bucket(bucket)
    BUCKET_MANAGER.set_policy(s3_bucket)
    BUCKET_MANAGER.set_config(s3_bucket)


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
    print("'here we are in the sync code with this pathname and bucket:",
          pathname, bucket)
    BUCKET_MANAGER.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
