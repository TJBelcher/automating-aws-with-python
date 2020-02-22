# coding: utf-8
import requests
url='https://to.be.replaced' 
data = { "text": "Hello, World." }
requests.post(url, json=data)
