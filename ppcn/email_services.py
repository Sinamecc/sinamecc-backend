from django.contrib.auth import get_user_model

User =  get_user_model()
class PPCNEmailServices():

    def __init__(self, emailServices):
        ##  SES_service instance
        self.emailServices = emailServices
    
    def sendNotification(self, recipient_list, subject, message_body):

        result = self.emailServices.send_notification(recipient_list, subject, message_body)

        return result
            
    def sendStatusNotification(self, ppcn, user_name):
        """first implementation"""
        subject = "Request of PPCN #: {0}".format(ppcn.id)
        user = User.objects.get(username=user_name)
        user_email = user.email
        message = self.buil_message(ppcn)
        result_status, result_email = self.sendNotification([user_email], subject, message)
        if not result_status:
            result_status, result_email = self.sendNotification([user_email], subject, message)
            if not result_status:
                error = "Unable to send the email to DCC, ERROR: {0}".format(str(result_email))
                return (result_status, error)
        return (result_status, result_email)



    def buil_message(self, data):
        message = "<h3>PPCN</h3> {0} {1} {2} {3} {4} {5} {6} {7}"
        organization = representative_name = phone_organization = fax = postal_code = address = ciiu = ""
        if data.organization != None:
            organization = "<p><b>Organizaci&oacute;n, Distrito o Cant&oacute;n: </b> {0}".format(str(data.organization.name))
            representative_name = "<p><b>Nombre  del Representante: </b>{0}</p>".format(str(data.organization.representative_name))
            phone_organization = "<p><b>Tel&eacute;fono: </b>{0}</p>".format(str(data.organization.phone_organization))
            if data.organization.postal_code != None:
                postal_code = "<p><b>C&oacute;digo Postal: </b>{0}</p>".format(str(data.organization.postal_code))
            if data.organization.fax != None:
                fax = "<p><b>Fax </b>{0}</p>".format(str(data.organization.fax))
            address = "<p><b>Direcci&oacute;n: </b>{0}".format(str(data.organization.address))
            if data.organization.ciiu != None:
                ciiu = "<p><b>CIIU: </b>{0}</p>".format(str(data.organization.ciiu))
        hyperlink =  "<br>Detalles en <a href={0}/ppcn/{1}>ver ma&#769;s</a>".format(self.emailServices.base_dir_notification, data.id)
        result= message.format(organization, representative_name, phone_organization, fax, postal_code, address, ciiu, hyperlink)
        return result

    def get_user_by_group(self, user_group):
        list = []
        for user in User.objects.filter(groups__name=user_group):
            list.append(user.email)
        return list
    