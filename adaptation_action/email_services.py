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

    def _notify_aux(self, from_template, context, subject, users):

        template_path_data = {'module': 'email', 'template': from_template}
        template = loader.get_template(self.template_path.format(**template_path_data))

        message_body = template.render(context)
        email_list = []

        for user in users:
            if user and hasattr(user, 'email'):
                email_list.append(user.email)
        
        notification_status, notification_data = self.send_notification(email_list, subject, message_body)

        result = (notification_status, notification_data)

        return result


    def notify_dcc_responsible_adaptation_action_submission(self, adaptation_action, user_approver):

        contact = adaptation_action.report_organization.contact
        context = {'lang': 'es', 'aa_code': adaptation_action.id}
        subject = 'Registro de Acción de Adaptación en SINAMECC'
        users = [contact, adaptation_action.user, user_approver]

        notification_status, notification_data = self._notify_aux('submitted_aa', context, subject, users)

        result = (notification_status, notification_data)

        return result

    def notify_contact_resposible_adaptation_action_evaluation_by_dcc(self, adaptation_action, user_approver):

        contact = adaptation_action.report_organization.contact
        context = {'lang': 'es', 'full_name': contact.contact_name, 'aa_code': adaptation_action.id}
        subject = 'Evaluación de Acción de Adaptación en SINAMECC'
        users = [contact, adaptation_action.user, user_approver]

        notification_status, notification_data = self._notify_aux('evaluation_aa', context, subject, users)

        result = (notification_status, notification_data)
        
        return result
    
    def notify_contact_responsible_mitigation_action_rejection(self, adaptation_action, user_approver):

        contact = adaptation_action.report_organization.contact
        context = {'lang': 'es', 'full_name': contact.contact_name, 'aa_code': adaptation_action.id}
        subject = 'Rechazo de Acción de Adaptación en SINAMECC'
        users = [contact, adaptation_action.user, user_approver]

        notification_status, notification_data = self._notify_aux('rejected_aa', context, subject, users)

        result = (notification_status, notification_data)

        return result
    
    def notify_contact_responsible_mitigation_action_changes(self, adaptation_action, user_approver):
        ...
    
    def notify_contact_responsible_mitigation_action_update(self, adaptation_action, user_approver):

        contact = adaptation_action.report_organization.contact
        context = {'lang': 'es', 'aa_code': adaptation_action.id}
        subject = 'Actualización de Acción de Adaptación en SINAMECC'
        users = [contact, adaptation_action.user, user_approver]

        notification_status, notification_data = self._notify_aux('submitted_updated_aa', context, subject, users)

        result = (notification_status, notification_data)

        return result
    
    def notify_contact_responsible_mitigation_action_approval(self, adaptation_action, user_approver):

        contact = adaptation_action.report_organization.contact
        context = {'lang': 'es', 'full_name': contact.contact_name, 'aa_code': adaptation_action.id}
        subject = 'Aprobación de Acción de Adaptación en SINAMECC'
        users = [contact, adaptation_action.user, user_approver]

        notification_status, notification_data = self._notify_aux('approved_aa', context, subject, users)

        result = (notification_status, notification_data)

        return result
    
    def notify_contact_responsible_mitigation_action_reminder_update(self, adaptation_action, user_approver):

        contact = adaptation_action.report_organization.contact
        context = {'lang': 'es', 'aa_code': adaptation_action.id}
        subject = 'Recordatorio de actualización de Acción de Adaptación en SINAMECC'
        users = [contact, adaptation_action.user, user_approver]

        notification_status, notification_data = self._notify_aux('reminder_update_aa', context, subject, users)

        result = (notification_status, notification_data)

        return result