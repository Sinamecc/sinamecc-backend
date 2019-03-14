from django.contrib.auth import get_user_model

User =  get_user_model()
class PPCNEmailServices():

    def __init__(self, email_services):
        ##  SES_service instance
        self.email_services = email_services
        self.message_subject_ppcn = "Request of PPCN #: {0}"
        self.USER_DOESNT_EXIST = "The user doesn't exist"
        self.GROUP_DOESNT_HAVE_USERS = "The group {0} doesn't have user associates"
        self.SEND_MAIL_ERROR = "Unable to send the email to {0}, ERROR: {1}"
    
    def send_notification(self, recipient, subject, message_body):

        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)
        return (result_status, result_data)

    def notify_submission_DCC(self, ppcn):
        group_name = 'dcc_ppcn_responsible'
        return self.send_status_notification_to_group(ppcn, group_name)

    def notify_submission_user(self, ppcn):
        user_id =  ppcn.user.id
        return self.send_status_notification_to_user(ppcn, user_id)

    def send_status_notification_to_user(self, ppcn, user_id):

        subject = self.message_subject_ppcn.format(ppcn.id)
        message = self.buil_message(ppcn)
        result_status, result_data = self.get_user_by_id(user_id)

        if not result_status:
            return (result_status, result_data)

        user = result_data
        user_email = user.email
        result_status, result_email = self.send_notification(user_email, subject, message)

        if not result_status:
            error = self.SEND_MAIL_ERROR.format(user.name, result_email)
            return (result_status, error)

        return (result_status, result_email)


    def send_status_notification_to_group(self, ppcn, group_name):

        subject = self.message_subject_ppcn.format(ppcn.id)
        message = self.buil_message(ppcn)
        result_status, result_data = self.get_users_group(group_name)

        if not result_status:
            return (result_status, result_data)

        user_list = result_data
        result_status, result_email = self.send_notification(user_list, subject, message)
        
        if not result_status:
            error = self.SEND_MAIL_ERROR.format(group_name, result_email)
            return (result_status, error)

        return (result_status, result_email)


    def get_users_group(self, group_name):
        
        user_in_group = User.objects.filter(groups__name=group_name)
        if user_in_group.count() == 0: 
            error = self.GROUP_DOESNT_HAVE_USERS.format(group_name)
            return (False, error)

        user_list = []
        for user in user_in_group.all():
            user_list.append(user.email)

        return (True, user_list)


    def get_user_by_id(self, user_id):
        try:
            user = User.objects.get(pk= user_id)
            return (True, user)
        except (User.DoesNotExist):
            
            return (False, self.USER_DOESNT_EXIST)
        

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
        hyperlink =  "<br>Detalles en <a href={0}/ppcn/{1}>ver ma&#769;s</a>".format(self.email_services.base_dir_notification, data.id)
        result= message.format(organization, representative_name, phone_organization, fax, postal_code, address, ciiu, hyperlink)
        return result

    
    