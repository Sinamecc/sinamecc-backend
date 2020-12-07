from django.contrib.auth import get_user_model
from django.template import loader

User =  get_user_model()
class PPCNEmailServices():

    def __init__(self, email_services):
        
        ##  SES_service instance
        self.email_services = email_services
        self.message_subject_ppcn = "Request of PPCN #: {0}"
        self.USER_DOESNT_EXIST = "The user doesn't exist"
        self.GROUP_DOESNT_HAVE_USERS = "The group {0} doesn't have user associates"
        self.SEND_MAIL_ERROR = "Unable to send the email to {0}, ERROR: {1}"
        self.template_path = "{module}/{template}.html"
    
    def send_notification(self, recipient, subject, message_body):

        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)

        return (result_status, result_data)


    
    def notify_for_submitting_ppcn(self, ppcn):

        ## missing validations:
        contact = ppcn.organization.contact

        template_path_data = {'module': 'email', 'template': 'submitted_ppcn'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))
        
        organization_name = ppcn.organization.name
        representative_name = ppcn.organization.representative_name
        geographic_level = ppcn.geographic_level.level_es
        recognition_type = ppcn.organization_classification.recognition_type.recognition_type_es


        context = {'lang': 'es', 
                    'organization_name': organization_name, 'representative_name': representative_name, 
                    'geographic_level': geographic_level, 'recognition_type': recognition_type
                } 

        email = contact.email
        subject = 'Registro PPCN'
        message_body = template.render(context)

        notification_status, notifiacion_data = self.send_notification(email, subject, message_body)

        return (notification_status, notifiacion_data)