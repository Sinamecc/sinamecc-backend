from django.contrib.auth import get_user_model
from users.services.resources import UserResourcesService
User =  get_user_model()

class MCCREmailServices():

    def __init__(self, email_services):
        ##  SES_service instance
        self.email_services = email_services
        self.user_services = UserResourcesService()
        self.message_subject_mccr = "MCCR #: {0}"
        self.SEND_NOTIFICATION_ERROR = "Unable to send the email to OVV, ERROR: {0}"
        self.SEND_MAIL_ERROR = "Unable to send the email to {0}, ERROR: {1}"

    def send_notification(self, recipient_list, subject, message_body):

        result = self.email_services.send_status_notification(recipient_list, subject, message_body)
        return result

    def notify_submission_ovv(self, mccr, ovv):

        ovv_email = ovv.email
        result = self.send_notification_to_ovv(mccr, ovv_email)
        return result

    def notify_submission_user(self, mccr):

        user_id =  mccr.user.id
        return self.send_status_notification_to_user(mccr, user_id)
    
    def notify_submission_DCC(self, mccr):
        group_name = 'dcc_mccr_responsible'
        return self.send_status_notification_to_group(mccr, group_name)
    
    def notify_submission_exec_secretary(self, mccr):
        group_name = 'dcc_executive_secretary'
        return self.send_status_notification_to_group(mccr, group_name)

    def send_status_notification_to_user(self, mccr, user_id):

        subject = self.message_subject_mccr.format(mccr.id)
        message = self.buil_message(mccr)
        user = self.user_services.get_by_id(user_id)

        user_email = user.email
        result_status, result_email = self.send_notification(user_email, subject, message)

        if not result_status:
            error = self.SEND_MAIL_ERROR.format(user.email, result_email)
            return (result_status, error)

        return (result_status, result_email)

    def send_status_notification_to_group(self, mccr, group_name):

        # subject = self.message_subject_mccr.format(mccr.id)
        # message = self.buil_message(mccr)
        # result_status, result_data = self.user_services.get_group_users(group_name)

        # if not result_status:
        #     return (result_status, result_data)

        # user_list = result_data
        # result_status, result_email = self.send_notification(user_list, subject, message)
        
        # if not result_status:
        #     error = self.SEND_MAIL_ERROR.format(group_name, result_email)
        #     return (result_status, error)

        # return (result_status, result_email)

        return (True, 'OK')
    
    def send_notification_to_ovv(self, mccr, ovv_email):

        subject = self.message_subject_mccr.format(mccr.id)
        message = self.buil_message(mccr)
        result_status, result_email = self.send_notification(ovv_email, subject, message)
        if not result_status:
            #sending again (connection error)
            result_status, result_email = self.send_notification(ovv_email, subject, message)
            if not result_status:
                error = self.SEND_NOTIFICATION_ERROR.format(str(result_email))
                return (result_status, error)
        return (result_status, result_email)


    def buil_message(self, data):
        message =  "<h3>MCCR</h3> {0} {1} {2} {3}"
        mccr = "<p><b>MCCR #: </b> {0}".format(str(data.id))
        mitigation = "<p><b>Mitigaci&oacute;n: </b>{0}</p>".format(str(data.mitigation.name))
        status = "<p><b>Estato: </b>{0}</p>".format(str(data.fsm_state))
        hyperlink = "<br>Detalles en <a href={0}/mccr/registries/{1}>ver m&aacute;s</a>".format(self.email_services.base_dir_notification, data.id)
        result = message.format(mccr, mitigation, status, hyperlink)
        return result

