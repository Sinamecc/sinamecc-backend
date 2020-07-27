from django.contrib.auth import get_user_model
User =  get_user_model()
class UserEmailServices():

    def __init__(self, email_services):
        
        ##  SES_service instance
        self.email_services = email_services
        self.message_subject_ppcn = "Request of PPCN #: {0}"
        self.USER_DOESNT_EXIST = "The user doesn't exist"
        self.GROUP_DOESNT_HAVE_USERS = "The group {0} doesn't have user associates"
        self.SEND_MAIL_ERROR = "Unable to send the email to {0}, ERROR: {1}"
    
    def send_notification(self, recipient, subject, message_body):

        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)
        return (result_status, result_data)


    def notify_for_requesting_password_change(self):
        pass