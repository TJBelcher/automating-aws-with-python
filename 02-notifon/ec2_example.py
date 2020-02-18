# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
ec2 = session.resource('ec2')
key_name = 'python_automation_key'
key_path = key_name + '
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)
key.key_material
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)

get_ipython().run_line_magic('ls', '-l python_automation_key.pem')
import os, stat
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
get_ipython().run_line_magic('ls', '-l python_automation_key.pem')
dir
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('ls', '-l python_automation_key.pem')
get_ipython().run_line_magic('ls', '-la python_automation_key.pem')
get_ipython().run_line_magic('ls', '-l -a python_automation_key.pem')
ec2.images.filter(Owners=['amazon'])
list(ec2.images.filter(owners=['amazon']))
list(ec2.images.filter(Owners=['amazon']))
get_ipython().run_line_magic('cls', '')
list(ec2.images.filter(Owners=['amazon']))
img = ec2.Image('ami-0a887e401f7654935')
img.name
ami_name = 'amzn2-ami-hvm-2.0.20200207.1-x86_64-gp2'
filters = [{'Name': 'NAME', 'Values': [ami_name]}]
list(ec2.imatges.filter(Owners=['amazon'], Filters=filters))
list(ec2.images.filter(Owners=['amazon'], Filters=filters))
list(ec2.images.filter(Owners=['amazon'], Filters=filters))
filters
filters = [{'Name': 'name', 'Values': [ami_name]}]
list(ec2.images.filter(Owners=['amazon'], Filters=filters))
list(ec2_apse2.images.filter(Owners=['amazon'], Filters=filters))
list(ec2.apse2.images.filter(Owners=['amazon'], Filters=filters))
list(ec2_apse2.images.filter(Owners=['amazon'], Filters=filters))
ec2aspe = session.resource('ec2', region_name='ap-sourtheast-2')
list(ec2apse.images.filter(Owners=['amazon'], Filters=filters))
ec2apse
ec2_apse2 = session.resource('ec2', region_name='ap-southeast-2')
list(ec2_apse2.images.filter(Owners=['amazon'], Filters=filters))
img
key
ec2.type
ec2
ec2.Image
img
instances = ec2.create.instances(ImageId=img.id, MinCount=1, Maxcount=1, InstanceType='t2.micro', KeyName=key.key_name)
instances = ec2.create_instances(ImageId=img.id, MinCount=1, Maxcount=1, InstanceType='t2.micro', KeyName=key.key_name)
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
instances
ec2.Instance(id='i-0f35030734c0c2e4c')
ec2.Instance(id='i-0f35030734c0c2e4c').name
ec2.Instance(id='i-0f35030734c0c2e4c').type
ec2.Instance(id='i-0f35030734c0c2e4c')[0]
inst = instances[0]
inst
ec2.Instance(id='i-0f35030734c0c2e4c').hypervisor
ec2.Instance(id='i-0f35030734c0c2e4c').terminate()
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
inst = instances[0]
inst.public_dns_name
inst.public_dns_name
inst.public_dns_name
inst.wait_until_running()
inst.public_dns_name
inst.public_dns_name
inst.reload()
inst.public_dns_name
inst.security_groups
sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg
sg.authorize_ingress(IpPermissions=[{'FromPort':22, 'ToPort': 22, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '108.40.123.30/32'}]}])
sg.authorize_ingress(IpPermissions=[{'FromPort':22, 'ToPort': 22, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '108.40.123.30/32'}]}])
sg.authorize_ingress(IpPermissions=[{'FromPort':80, 'ToPort': 80, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
