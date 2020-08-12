from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.crypto import get_random_string
from django.utils import six
User =  get_user_model()
class UserEmailServices():

    def __init__(self, email_services):
        
        ##  SES_service instance
        self.email_services = email_services
        self.message_subject_ppcn = "Request of PPCN #: {0}"
        self.USER_DOESNT_EXIST = "The user doesn't exist"
        self.GROUP_DOESNT_HAVE_USERS = "The group {0} doesn't have user associates"
        self.SEND_MAIL_ERROR = "Unable to send the email to {0}, ERROR: {1}"
        self.token_generator = PasswordResetTokenGenerator()
    
    def send_notification(self, recipient, subject, message_body):

        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)
        return (result_status, result_data)


    def notify_for_requesting_password_change(self, user, encoded_user_id):
    
        token = self.token_generator.make_token(user)
        

        return False , encoded_user_id

