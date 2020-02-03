#!/usr/bin/python  (interpreter used)
# -*- coding:  utf-8 -*- ()
# (First line above developers what interpreter was used to develop
# and next tells text editor that it's encoded with utf-8.)

"""Webotron:  Deploy websites with AWS.

Webotron automates the process of deploying static websites to AWS
- Configure AWS S3 buckets
  - Create them
  - Set them up for static website hosting
  - Deploy local files to them
- Configure DNS with AWS Route 53
- Configure a Content Delivery Network and SSL with AWS Cloudfront
"""

import boto3
import click

from bucket import BucketManager

session = None
bucket_manager = None

@click.group()
@click.option('--profile', default=None,
    help="Use a given AWS profile.")

def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(profile_name=session_cfg.pop('profile_name', 'pythonAutomation'))
    # session = boto3.Session(**session_cfg)
    print(session)
    bucket_manager = BucketManager(session)


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an S3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)
        # print(obj.bucket_name, obj.key)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    print(s3_bucket, " Initialized!")
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

#   return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
