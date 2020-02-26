# coding: utf-8
event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2020-02-26T14:52:43.300Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDATAJRUERRWD7U4LDC5'}, 'requestParameters': {'sourceIPAddress': '108.40.123.30'}, 'responseElements': {'x-amz-request-id': '3B9A1ADA0731C204', 'x-amz-id-2': 'VfDABxe2KJHHJomeP+B23h0jKMgPJKGFLEfOQcZPFuH4vWYoGnXwriWMKKVQ/Ejv5Tmt4SZtRf1TptmSPIprcYOCMDYhepZq'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '741708f3-3e5e-463d-82f7-8c87c81b86ce', 'bucket': {'name': 'tomvideolyzervideos57', 'ownerIdentity': {'principalId': 'A1NLASXFNIDCFV'}, 'arn': 'arn:aws:s3:::tomvideolyzervideos57'}, 'object': {'key': 'van+video.mp4', 'size': 6234342, 'eTag': 'bfff9edb4923d7f8b26239e10efdbee6', 'sequencer': '005E56863E5A71C212'}}}]}
event
event['Records'][0]
event['Records'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['object']['key']
import urllib
urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
