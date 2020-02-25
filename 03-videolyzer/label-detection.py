# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')
bucket = s3.create_bucket(Bucket='tomvideolyzervideos')
from pathlib import Path
get_ipython().run_line_magic('ls', 'c:\\Users\\TOM\\Downloads\\videos\\*.mp4')
pathname = 'c:\Users\TOM\Downloads\videos\*.mp4c:\Users\TOM\Downloads\videos\Blurry Video Of People Working.mp4'
pathname = 'c:\Users\TOM\Downloads\videos\Blurry Video Of People Working.mp4'
get_ipython().run_line_magic('ls', 'c:/Users/TOM/Downloads/videos/*.mp4')
get_ipython().run_line_magic('ls', 'c:\\Users\\TOM\\Downloads\\videos\\*.mp4')
pathname = r"c:\Users\TOM\Downloads\videos\Blurry Video Of People Working.mp4"
pathname
path = Path(pathname).expanduser().resolve()
print(path)
print(str(path.name))
bucket.upload_file(str(path), str(path.name))
rekognition_client = session.client('rekognition') 
bucket
response = rekognition_client.start_label_detection(
Video={'S3Object': { 'Bucket': bucket.name, 'Name': path.name}})
response
job_id = response['JobId']
job_id
result = rekognition_client.get_label_detection(JobId=job_id)
result
get_ipython().run_line_magic('history', '')
job_id
result.keys()
result['Jobstatus']
result = rekognition_client.get_label_detection(JobId=job_id)
result.keys()
result['Jobstatus']
result
result['Jobstatus']
result.keys()
result['VideoMetadata']
result['Labels']
result.keys()
result['JobStatus']
result['ResponseMetadata']
result['VideoMetadata']
result['Labels']
result['Labels'] > mylabeloutput.txt
with open('out.txt', 'w') as f: f.write(something)
with open('mylabelout.txt', 'w') as f:
    f.write(result['Labels'])
      
with open('mylabelout.txt', 'w') as f:
    f.write(str.result['Labels'])
    
      
mylabelout = result['Labels']
for f in mylabelout:
    print(f)
    
