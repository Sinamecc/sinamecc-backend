from django.contrib.auth import get_user_model

User =  get_user_model()
class MitigationActionEmailServices():

    def __init__(self, emailServices):
        ##  SES_service instance
        self.emailServices = emailServices
    
    def buil_message_mitigation_action(self, mitigation_action):

        message = "<h3>Accion de Mitigaci&Oacute;n:</h3> {0} {1} {2} {3} {4} {5}"
        id = "<p><b>ID: </b> {0}".format(str(mitigation_action.id))
        strategy_name = "<p><b>Nombre de la estrategia: </b>{0}</p>".format(str(mitigation_action.strategy_name))
        name = "<p><b>Nombre: </b>{0}</p>".format(str(mitigation_action.name))
        quantitative_purpose = "<p><b>Prop&oacute;sito cuantitativo: </b>{0}</p>".format(str(mitigation_action.quantitative_purpose))

        notifications = ""
        next_action = ""

        if self.emailServices.base_dir_notification != None:
            notifications = "<br>Detalles en <a href='{0}/mitigation/actions/{1}' >ver ma&#769;s</a>".format(self.emailServices.base_dir_notification ,mitigation_action.id)
            next_action = "<br>Siguientes acciones: <a href='{0}/mitigation/actions/{1}/reviews/new' >ver ma&#769;s</a>".format(self.emailServices.base_dir_notification, mitigation_action.id)
        result = message.format(id, strategy_name, name, quantitative_purpose, notifications, next_action)

        return result

    def sendStatusNotification(self, group, mitigation_action):

        message_body = self.buil_message_mitigation_action(mitigation_action)

        subject = "Mitigation Action: {0}".format(mitigation_action.id)
        recipient_list = self.get_user_by_group(group)

        result = self.emailServices.send_notification(recipient_list, subject, message_body)
        return result

    def get_user_by_group(self, user_group):
        list = []
        for user in User.objects.filter(groups__name=user_group):
            list.append(user.email)
        return list
    