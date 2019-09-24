# coding: utf-8
# pipenv session setup at start
# to run this script, type the following from project folder in Powershell:
#   pipenv run ipython -i ipythonsession.py

import boto3
session = boto3.Session('profile_name=pythonAutomation')
s3 = session.resource('s3')
