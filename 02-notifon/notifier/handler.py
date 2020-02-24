import os

import requests

def post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

# following data assignment uses the glob object for **event - this allows
# overlay of data fields using the formatting command. Note that all
# globbed fields must exist or it will throw an error.
    slack_message = "From {source} at {detail[StartTime]}: {detail[Description]}".format(**event)
    data = { "text": slack_message }
    requests.post(slack_webhook_url, json=data)

#    print(slack_webhook_url)
#    print(event)

    return
