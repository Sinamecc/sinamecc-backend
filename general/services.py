import boto3
from botocore.exceptions import ClientError

class EmailServices():

    def __init__(self, sender):

        self.sender = sender
        self.AWS_REGION = "us-east-1"
        self.CHARSET = "UTF-8"

    def send_notification(self, recipient_list, subject, message_body):
        
        client = boto3.client('ses', region_name = self.AWS_REGION)
        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': recipient_list
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.CHARSET,
                            'Data': message_body,
                        },
                        'Text': {
                            'Charset': self.CHARSET,
                            'Data': message_body,
                        },
                    },
                    'Subject': {
                        'Charset': self.CHARSET,
                        'Data': subject,
                    },
                },
                Source=self.sender,
                
            )

        except ClientError as e:

            return (False, e.response['Error']['Message'])

        else:

            return (True, response)
