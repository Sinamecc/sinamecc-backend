from users.services import UserService
from django.contrib.auth import get_user_model
User =  get_user_model()

class MitigationActionEmailServices():

    def __init__(self, email_services):
        ##  SES_service instance
        self.email_services = email_services
        self.user_services = UserService()
        self.message_subject = "Request of Mitigation Action: #: {0}"
        self.USER_DOESNT_EXIST = "The user doesn't exist"
        self.GROUP_DOESNT_HAVE_USERS = "The group {0} doesn't have user associates"
        self.SEND_MAIL_ERROR = "Unable to send the email to {0}, ERROR: {1}"
    

    
    def send_notification(self, recipient, subject, message_body):

        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)
        return (result_status, result_data)

    def notify_submission_user(self, mitigation_action):

        user_id =  mitigation_action.user.id
        return self.send_status_notification_to_user(mitigation_action, user_id)



    def send_status_notification_to_user(self, mitigation_action, user_id):

        subject = self.message_subject.format(mitigation_action.id)
        message = self.buil_message(mitigation_action)
        result_status, result_data = self.user_services.get_user_by_id(user_id)

        if not result_status:
            return (result_status, result_data)

        user = result_data
        user_email = user.email
        full_user_name = "{0} {1}".format(user.first_name, user.last_name)
        result_status, result_email = self.send_notification(user_email, subject, message)

        if not result_status:
            error = self.SEND_MAIL_ERROR.format(full_user_name, result_email)
            return (result_status, error)

        return (result_status, result_email)



    def buil_message(self, mitigation_action):

        message = "<h3>Accion de Mitigaci&Oacute;n:</h3> {0} {1} {2} {3} {4}"
        id = "<p><b>ID: </b> {0}".format(str(mitigation_action.id))
        strategy_name = "<p><b>Nombre de la estrategia: </b>{0}</p>".format(str(mitigation_action.strategy_name))
        name = "<p><b>Nombre: </b>{0}</p>".format(str(mitigation_action.name))

        notifications = ""
        next_action = ""

        if self.email_services.base_dir_notification != None:
            notifications = "<br>Detalles en <a href='{0}/mitigation/actions/{1}' >ver ma&#769;s</a>".format(self.email_services.base_dir_notification ,mitigation_action.id)
            next_action = "<br>Siguientes acciones: <a href='{0}/mitigation/actions/{1}/reviews/new' >ver ma&#769;s</a>".format(self.email_services.base_dir_notification, mitigation_action.id)
        result = message.format(id, strategy_name, name, notifications, next_action)

        return result