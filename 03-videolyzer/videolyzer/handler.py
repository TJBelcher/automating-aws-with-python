import json
import os
import urllib

import boto3

def start_label_detection(bucket, key):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
        Video={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        NotificationChannel={
            'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
            'RoleArn': os.environ['REKOGNITION_ROLE'],
            })

    print(response)

    return

def get_video_labels(job_id):
    rekognition_client = boto3.client('rekognition')
# first set response to initial get label detection results
    response = rekognition_client.get_label_detection(JobId=job_id)
# set next_token to the next_token value stored in first record or set to none
    next_token = response.get('NextToken', None)

    while next_token:
# load next_page with the label data from next token if there is some
        next_page = rekognition_client.get_label_detection(
            JobId=job_id,
            NextToken=next_token
        )
# then set next token to the next token value in the next page read above
        next_token = next_page.get('NextToken', None)
# extend the response in labels with the label data from the next page
# that was read above in the loop
        response['Labels'].extend(next_page['Labels'])

    return response

def make_item(data):
    if isinstance(data, dict):
        return { k: make_item(v) for k, v in data.items() }

    if isinstance(data, list):
        return [ make_item(v) for v in data ]

    if isinstance(data, float):
        return str(data)

    return data

def put_labels_in_db(data, video_name, video_bucket):
    pass
#    del data['ResponseMetadata']
#    del data['JobStatus']

#    data['videoName'] = video_name
#    data['videoBucket'] = video_bucket

#    dynamodb = boto3.resource('dynamodb')
#    table_name = os.environ['DYNAMODB_TABLE_NAME']
#    videos_table = dynamodb.Table(table_name)

#    data = make_item(data)

#    videos_table.put_item(Item=data)

#    return

# Lambda events

def start_processing_video(event, context):
    for record in event['Records']:
        start_label_detection(
            record['s3']['bucket']['name'],
            urllib.parse.unquote_plus(record['s3']['object']['key'])
        )

    return

# def handle_label_detection(event, context):

#    print("handle_label_detection:  ", event)

#    return

def handle_label_detection(event, context):
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        job_id = message['JobId']
        s3_object = message['Video']['S3ObjectName']
        s3_bucket = message['Video']['S3Bucket']

        response = get_video_labels(job_id)
        print(response)
        put_labels_in_db(response, s3_object, s3_bucket)

    return
