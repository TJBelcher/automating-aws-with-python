# coding: utf-8
import boto3
import sys #not needed but kept in anyway
import click #for argument processing

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass

@cli.command('list-buckets') #this is a decorator controlling execution
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects') #this is a decorator controlling execution
                                    #if not present the list_bucket_objects
                                    #name would be used - hyphens more friendly
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List objects in an S3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

if __name__ == '__main__':
    cli()
