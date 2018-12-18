from django.contrib.auth import get_user_model
User =  get_user_model()

class MCCREmailServices():

    def __init__(self, emailServices):
        ##  SES_service instance
        self.emailServices = emailServices

    def sendNotification(self, recipient_list, subject, message_body):
        result = self.emailServices.send_notification(recipient_list, subject, message_body)
        return result

    def sendStatusNotification(self,  mccr, ovv):
        subject = "MCCR #: {0}".format(mccr.id)

        message = self.buil_message(mccr)
        result_status, result_email = self.sendNotification([ovv], subject, message)
        if not result_status:
            #sending again (connection error)
            result_status, result_email = self.sendNotification([ovv], subject, message)
            if not result_status:
                error = "Unable to send the email to OVV, ERROR: {0}".format(str(result_email))
                return (result_status, error)
        return (result_status, result_email)

    def buil_message(self, data):
        message =  "<h3>MCCR</h3> {0} {1} {2} {3}"
        mccr = "<p><b>MCCR id: </b> {0}".format(str(data.id))
        mitigation = "<p><b>Mitigaci&oacute;n: </b>{0}</p>".format(str(data.mitigation.name))
        status = "<p><b>Estato: </b>{0}</p>".format(str(data.fsm_state))
        hyperlink = "<br>Detalles en <a href={0}/mccr/registries/{1}>ver m&aacute;s</a>".format(self.emailServices.base_dir_notification, data.id)
        result = message.format(mccr, mitigation, status, hyperlink)
        return result

    def sendStatusNotificationToUser(self,  mccr, user_name):
        subject = "MCCR #: {0}".format(mccr.id)
        user = User.objects.get(username=user_name)
        user_email = user.email
        message = self.buil_message(mccr)
        result_status, result_email = self.sendNotification([user_email], subject, message)
        print("result_email: ", result_email)
        if not result_status:
            #sending again (connection error)
            result_status, result_email = self.sendNotification([user_email], subject, message)
            if not result_status:
                error = "Unable to send the email to executive  secretary, ERROR: {0}".format(str(result_email))
                return (result_status, error)
        return (result_status, result_email)

    def sendStatusNotificationUserMccr(self,  mccr):
        subject = "MCCR #: {0}".format(mccr.id)
        user = User.objects.get(id=mccr.user_id)
        user_email = user.email
        message = self.buil_message(mccr)
        result_status, result_email = self.sendNotification([user_email], subject, message)
        print("result_email: ", result_email)
        if not result_status:
            #sending again (connection error)
            result_status, result_email = self.sendNotification([user_email], subject, message)
            if not result_status:
                error = "Unable to send the email to MCCR user, ERROR: {0}".format(str(result_email))
                return (result_status, error)
        return (result_status, result_email)