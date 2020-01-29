import boto3
import click
# import sys


session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List objects in an S3 bucket"
#    bucket = s3.Bucket(name=bucket) - this works too!
    bucket = s3.Bucket(bucket)
    for obj in bucket.objects.all():
        print(obj)



@cli.command()
def hey_jerk2():
    "print out hey-jerk to all jerks"
    print("hey jerk!!!")

if __name__ == '__main__':
    cli()
