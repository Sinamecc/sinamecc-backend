from django.contrib.auth import get_user_model
from django.template import loader

User = get_user_model()

class AdaptationActionEmailServices():

    def __init__(self, email_services):
        self.email_services = email_services
        self.template_path = "{module}/{template}.html"
    
    def send_notification(self, recipient, subject, message_body):
        
        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)
        return (result_status, result_data)

    def notify_dcc_responsible_adaptation_action_submission(self, adaptation_action, user_approver):

        template_path_data = {'module': 'email', 'template': 'submitted_aa'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        contact = adaptation_action.report_organization.contact
        context = {'lang': 'es', 'aa_code': adaptation_action.id}

        subject = 'Registro de Acción de Adaptación en SINAMECC'
        message_body = template.render(context)
        email_list = []
        for user in [contact, adaptation_action.user , user_approver]:
            if user and hasattr(user, 'email'):
                email_list.append(user.email)

        notification_status, notification_data = self.send_notification(email_list, subject, message_body)

        result = (notification_status, notification_data)

        return result

    def notify_contact_resposible_adaptation_action_evaluation_by_dcc(self, adaptation_action, user_approver):

        template_path_data = {'module': 'email', 'template': 'evaluation_aa'}
        
        template = loader.get_template(self.template_path.format(**template_path_data))

        contact = adaptation_action.report_organization.contact
        context = {'lang': 'es', 'full_name': contact.contact_name, 'aa_code': adaptation_action.id}

        email = contact.email
        subject = 'Evaluación de Acción de Adaptación en SINAMECC'
        message_body = template.render(context)

        notification_status, notification_data = self.send_notification(email, subject, message_body)

        result = (notification_status, notification_data)
        
        return result