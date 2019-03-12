import boto3
from botocore.exceptions import ClientError
from django.conf import settings
class EmailServices():

    def __init__(self, sender = "sinamec@grupoincocr.com", base_dir_notification =  settings.BASE_DIR_VIEW ):
        self.sender = sender
        self.base_dir_notification = base_dir_notification
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

    def send_status_notification(self, recipient_list, subject, message_body, link = False):
        """first implementation"""
        subject = "General: " + subject

        if link:
            message_body += "\nlink: " + link

        result = self.send_notification(recipient_list, subject, message_body)

        return result

class HandlerErrors():

    def error_400(self, errors):
        result_error = {"error_code": 400, "error_message": errors}
        return (False, result_error)