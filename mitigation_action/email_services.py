from users.services.general import UserService
from users.models import CustomUser
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


    def notify_dcc_responsible_mitigation_action_submission(self, mitigation_action, user_approver):

        template_path_data = {'module': 'email', 'template': 'submitted_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        context = {'lang': 'es', 'ma_code': mitigation_action.code, 'frontend_url': self.email_services.base_dir_notification, 'mitigation_id': mitigation_action.id}
      
        subject = 'Registro de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)

        user_approver = CustomUser.objects.filter(username='general_dcc').first()

        notification_status, notification_data = self.send_notification(user_approver.email, subject, message_body)

        result = (notification_status, notification_data)
        
        return result
    

    def notify_contact_responsible_mitigation_action_evaluation_by_dcc(self, mitigation_action):

        template_path_data = {'module': 'email', 'template': 'evaluation_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        contact = mitigation_action.contact
        context = {'lang': 'es', 'full_name': contact.full_name, 'ma_code': mitigation_action.code, 'frontend_url': self.email_services.base_dir_notification, 'mitigation_id': mitigation_action.id}

        subject = 'Evaluación de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)
        contact_email = mitigation_action.user.email
        notification_status, notification_data = self.send_notification(contact_email, subject, message_body)


        result = (notification_status, notification_data)
        
        return result
    

    def notify_contact_responsible_mitigation_action_rejection(self, mitigation_action):
        
        template_path_data = {'module': 'email', 'template': 'rejected_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        contact = mitigation_action.contact
        context = {'lang': 'es', 'full_name': contact.full_name, 'ma_code': mitigation_action.code, 'frontend_url': self.email_services.base_dir_notification, 'mitigation_id': mitigation_action.id}

        subject = 'Rechazo de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)
        contact_email = mitigation_action.user.email
        
        notification_status, notification_data = self.send_notification(contact_email, subject, message_body)


        result = (notification_status, notification_data)

        return result
    

    def notify_dcc_responsible_mitigation_action_request_changes(self, mitigation_action):

        template_path_data = {'module': 'email', 'template': 'changes_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        context = {'lang': 'es', 'ma_code': mitigation_action.code, 'frontend_url': self.email_services.base_dir_notification, 'mitigation_id': mitigation_action.id}

        subject = 'Actualización de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)
        contact_email = mitigation_action.user.email
                
        notification_status, notification_data = self.send_notification(contact_email, subject, message_body)


        result = (notification_status, notification_data)

        return result


    def notify_dcc_responsible_mitigation_action_update(self, mitigation_action, user_approver):

        template_path_data = {'module': 'email', 'template': 'submitted_updated_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        context = {'lang': 'es', 'ma_code': mitigation_action.code, 'frontend_url': self.email_services.base_dir_notification, 'mitigation_id': mitigation_action.id}

        subject = 'Actualización de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)
        
        user_approver = CustomUser.objects.filter(username='general_dcc').first()
                
        notification_status, notification_data = self.send_notification(user_approver.email, subject, message_body)


        result = (notification_status, notification_data)

        return result

    ## aproved mitigation action

    def notify_contact_responsible_mitigation_action_approval(self, mitigation_action):
        
        template_path_data = {'module': 'email', 'template': 'approved_ma'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        contact = mitigation_action.contact
        context = {'lang': 'es', 'full_name': contact.full_name, 'ma_code': mitigation_action.code, 'frontend_url': self.email_services.base_dir_notification, 'mitigation_id': mitigation_action.id}


        subject = 'Aprobación de Acción de Mitigación en SINAMECC'
        message_body = template.render(context)
        contact_email = mitigation_action.user.email
                
        notification_status, notification_data = self.send_notification(contact_email, subject, message_body)


        result = (notification_status, notification_data)

        return result
        









