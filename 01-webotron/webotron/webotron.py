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

from pprint import pprint
import boto3
import click

from bucket import BucketManager
from domain import DomainManager

import util

session = None
bucket_manager = None
domain_manager = None


@click.group()
@click.option('--profile', default=None, help="Use a given AWS profile.")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager, domain_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(profile_name=session_cfg.pop('profile_name',
                                                         'pythonAutomation'))
    # session = boto3.Session(**session_cfg)
    # print(session)
    bucket_manager = BucketManager(session)
    domain_manager = DomainManager(session)


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
#   in below statement, bucket_manager.s3.Bucket(bucket) resolves to
#   s3.Bucket(name='automatingawstomb-boto3d')
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))


@cli.command('setup-domain')
@click.argument('domain')
def setup_domain(domain):
    """Configure domain to point to bucket."""
    # get the entire bucket when passing just bucket name to this function
    bucket = bucket_manager.get_bucket(domain)

    zone = domain_manager.find_hosted_zone(domain) \
        or domain_manager.create_hosted_zone(domain)
    # print(zone)
    print("zone = ")
    pprint(zone)
    # endpoint is the domain endpoint for the bucket we're building record for
    endpoint = util.get_endpoint(bucket_manager.get_region_name(bucket))
    a_record = domain_manager.create_s3_domain_record(zone, domain, endpoint)
    # Note - there's no need to do an or-check during domain record creation
    # as upsert either uploads a record if not present or updates if it is
    print("Domain configure:  http://{}".format(domain))
    print("A_Record = ")
    pprint(a_record)


if __name__ == '__main__':
    cli()
