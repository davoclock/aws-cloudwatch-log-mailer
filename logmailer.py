import json
import boto3
import gzip
import base64
import os

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    decoded_event = json.loads(gzip.decompress(base64.b64decode(event['awslogs']['data'])))
    body = '''
    LogGroup: {loggroup}
    Logstream: {logstream}
    Filter Match: {filtermatch}
    '''.format(
        loggroup=decoded_event['logGroup'],
        logstream=decoded_event['logStream'],
        filtermatch=decoded_event['logEvents'][0]['message'],
    )
    
    def send_message(body):
        sns = sns_client.publish(
            TopicArn = os.environ.get('SNS_TOPIC_ARN'),
            Message = body,
        )
    
    send_message(body)
            
