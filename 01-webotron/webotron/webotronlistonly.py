"""Webotron:  list only test script."""
import boto3
import click
# import sys


session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')


@click.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in s3.buckets.all():
        print(bucket)


if __name__ == '__main__':
    list_buckets()
