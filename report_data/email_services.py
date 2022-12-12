from django.contrib.auth import get_user_model
from django.template import loader

User = get_user_model()

class ReportDataEmailServices():

    def __init__(self, email_services):
        self.email_services = email_services
        self.template_path = "{module}/{template}.html"
    
    def send_notification(self, recipient, subject, message_body):
        
        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)
        return (result_status, result_data)

    def _notify_aux(self, from_template, context, subject, users):

        template_path_data = {'module': 'email', 'template': from_template}
        template = loader.get_template(self.template_path.format_map(template_path_data))

        message_body = template.render(context)
        email_list = []

        for user in users:
            if user and hasattr(user, 'email'):
                email_list.append(user.email)
        
        notification_status, notification_data = self.send_notification(email_list, subject, message_body)

        result = (notification_status, notification_data)

        return result


    def notify_dcc_responsible_report_data_submission(self, report_data, user_approver):

        contact = report_data.contact
        context = {'lang': 'es', 'rd_code': report_data.id}
        subject = 'Registro de datos en SINAMECC'
        users = [user_approver]

        notification_status, notification_data = self._notify_aux('submitted_rd', context, subject, users)

        result = (notification_status, notification_data)

        return result

    def notify_contact_resposible_report_data_evaluation_by_dcc(self, report_data, user_approver):

        contact = report_data.contact
        context = {'lang': 'es', 'full_name': contact.contact_name, 'rd_code': report_data.id}
        subject = 'Evaluación de Captura de datos en SINAMECC'
        users = [contact]

        notification_status, notification_data = self._notify_aux('evaluation_rd', context, subject, users)

        result = (notification_status, notification_data)
        
        return result
    
    def notify_contact_responsible_report_data_rejection(self, report_data, user_approver):

        contact = report_data.contact
        context = {'lang': 'es', 'full_name': contact.contact_name, 'rd_code': report_data.id}
        subject = 'Rechazo de Captura de datos en SINAMECC'
        users = [contact]

        notification_status, notification_data = self._notify_aux('rejected_rd', context, subject, users)

        result = (notification_status, notification_data)

        return result
    
    def notify_contact_responsible_report_data_requested_changes(self, report_data, user_approver):
        
        contact = report_data.contact
        context = {'lang': 'es', 'full_name': contact.contact_name, 'rd_code': report_data.id}
        subject = 'Solicitud de cambios en Captura de datos en SINAMECC'
        users = [contact]

        notification_status, notification_data = self._notify_aux('changes_rd', context, subject, users)

        result = (notification_status, notification_data)

        return result

    def notify_contact_responsible_report_data_update(self, report_data, user_approver):

        contact = report_data.contact
        context = {'lang': 'es', 'rd_code': report_data.id}
        subject = 'Actualización de Captura de datos en SINAMECC'
        users = [user_approver]

        notification_status, notification_data = self._notify_aux('submitted_updated_rd', context, subject, users)

        result = (notification_status, notification_data)

        return result
    
    def notify_contact_responsible_report_data_approval(self, report_data, user_approver):

        contact = report_data.contact
        context = {'lang': 'es', 'full_name': contact.contact_name, 'rd_code': report_data.id}
        subject = 'Aprobación de Captura de datos en SINAMECC'
        users = [contact]

        notification_status, notification_data = self._notify_aux('approved_rd', context, subject, users)

        result = (notification_status, notification_data)

        return result
    
    def notify_contact_responsible_report_data_reminder_update(self, report_data, user_approver):

        contact = report_data.contact
        context = {'lang': 'es', 'rd_code': report_data.id}
        subject = 'Recordatorio de actualización de Captura de datos en SINAMECC'
        users = [contact, report_data.user, user_approver]

        notification_status, notification_data = self._notify_aux('reminder_update_rd', context, subject, users)

        result = (notification_status, notification_data)

        return result