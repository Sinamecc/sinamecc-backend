from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.template import loader




User =  get_user_model()
class UserEmailServices():

    def __init__(self, email_services):
        
        ##  SES_service instance
        self.email_services = email_services
        self.message_subject_ppcn = "Request of PPCN #: {0}"
        self.USER_DOESNT_EXIST = "The user doesn't exist"
        self.GROUP_DOESNT_HAVE_USERS = "The group {0} doesn't have associated users"
        self.SEND_MAIL_ERROR = "Unable to send the email to {0}, ERROR: {1}"
        self.template_path = "{module}/{template}.html"
        self.token_generator = PasswordResetTokenGenerator()
    
    def send_notification(self, recipient, subject, message_body):

        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)
        return (result_status, result_data)


    def notify_for_requesting_password_change(self, user, encoded_user_id):
        
        token = self.token_generator.make_token(user)

        template_path_data = {'module': 'email', 'template': 'reset_password'}
        template = loader.get_template(self.template_path.format(**template_path_data))

        redirect_url = f"{self.email_services.base_dir_notification}/changePassword?code={encoded_user_id}&token={token}"
        full_name = f"{user.first_name} {user.last_name}"
        context = {"url": redirect_url, 'lang': 'es', 'full_name': full_name} ## at the moment

        message_body = template.render(context)

        subject = 'Reestablecer Contraseña'

        return self.send_notification(user.email, subject, message_body)
    

    def notify_new_user_creation_to_password_change(self, user, encoded_user_id):
        
        token = self.token_generator.make_token(user)

        template_path_data = {'module': 'email', 'template': 'reset_password_to_new_user'}
        template = loader.get_template(self.template_path.format(**template_path_data))

        redirect_url = f"{self.email_services.base_dir_notification}/changePassword?code={encoded_user_id}&token={token}"
        full_name = f"{user.first_name} {user.last_name}"
        context = {"url": redirect_url, 'lang': 'es', 'full_name': full_name, 'username': user.username, 'email': user.email} ## at the moment

        message_body = template.render(context)

        subject = 'Notificación de creación de usuario'

        return self.send_notification(user.email, subject, message_body)
    

    def notify_password_change_done(self, user):
        
        template_path_data = {'module': 'email', 'template': 'reset_password_done'}

        template = loader.get_template(self.template_path.format(**template_path_data))

        full_name = f"{user.first_name} {user.last_name}"

        context = {'lang': 'es', 'full_name': full_name, 'username': user.username} ## at the moment

        message_body = template.render(context)

        subject = 'Contraseña Reestablecida'

        return self.send_notification(user.email, subject, message_body)

