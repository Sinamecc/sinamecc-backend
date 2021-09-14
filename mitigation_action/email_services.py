from users.services import UserService
from django.contrib.auth import get_user_model
from django.template import loader

User =  get_user_model()

class MitigationActionEmailServices():

    def __init__(self, email_services):
        ##  SES_service instance
        self.email_services = email_services
        self.template_path = "{module}/{template}.html"

    
    def send_notification(self, recipient, subject, message_body):

        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)
        return (result_status, result_data)


    def notify_dcc_responsible_mitigation_action_submission(self, mitigation_action):

        template_path_data = {'module': 'email', 'template': 'submitted_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        context = {'lang': 'es'} 

        ## change this here 
        email = 'izcar@grupoincocr.com'
        subject = 'Registro de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)

        notification_status, notification_data = self.send_notification(email, subject, message_body)

        result = (notification_status, notification_data)
        
        return result
    

    def notify_contact_responsible_mitigation_action_evaluation_by_dcc(self, mitigation_action):

        template_path_data = {'module': 'email', 'template': 'evaluation_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        contact = mitigation_action.contact
        context = {'lang': 'es', 'full_name': contact.full_name}

        ## change this here 
        email = contact.email
        subject = 'Evaluación de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)

        notification_status, notification_data = self.send_notification(email, subject, message_body)

        result = (notification_status, notification_data)
        
        return result
    

    def notify_contact_responsible_mitigation_action_rejection(self, mitigation_action):
        
        template_path_data = {'module': 'email', 'template': 'rejected_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        contact = mitigation_action.contact
        context = {'lang': 'es', 'full_name': contact.full_name}

        ## change this here 
        email = contact.email
        subject = 'Rechazo de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)

        notification_status, notification_data = self.send_notification(email, subject, message_body)

        result = (notification_status, notification_data)

        return result
    

    def notify_dcc_responsible_mitigation_action_update(self, mitigation_action):

        template_path_data = {'module': 'email', 'template': 'submitted_updated_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        context = {'lang': 'es'} 

        ## change this here
        email = 'izcar@grupoincocr.com'
        subject = 'Actualización de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)

        notification_status, notification_data = self.send_notification(email, subject, message_body)

        result = (notification_status, notification_data)

        return result

    ## aproved mitigation action

    def notify_contact_responsible_mitigation_action_approval(self, mitigation_action):
        
        template_path_data = {'module': 'email', 'template': 'approved_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        contact = mitigation_action.contact
        context = {'lang': 'es', 'full_name': contact.full_name}

        ## change this here 
        email = contact.email

        subject = 'Aprobación de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)

        notification_status, notification_data = self.send_notification(email, subject, message_body)

        result = (notification_status, notification_data)

        return result
        









