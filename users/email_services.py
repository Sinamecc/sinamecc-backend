from django.contrib.auth import get_user_model
from django.template import loader
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator

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

    def notify_new_user_creation_to_password_change(
        self,
        user: AbstractUser,
        password_recovery_url: str
    ) -> None:
        
        template = loader.get_template(
                    self.template_path.format(
                        module='email',
                        template='reset_password_to_new_user'
                    )
                )   

        redirect_url = f"{self.email_services.base_dir_notification}/{password_recovery_url}"
        full_name = f"{user.first_name} {user.last_name}".title()
        context = {
            'url': redirect_url,
            'lang': 'es',
            'full_name': full_name,
            'username': user.username,
            'email': user.email
        }

        message_body = template.render(context)

        subject = 'Notificación de creación de usuario'

        self.send_notification(user.email, subject, message_body)
    
    def send_notification(self, recipient, subject, message_body):

        result_status, result_data = self.email_services.send_status_notification(recipient , subject, message_body)
        return (result_status, result_data)


    def notify_for_requesting_password_change(self, user: AbstractUser, password_recovery_url: str) -> None:
        
        template = loader.get_template(
                    self.template_path.format(
                        module='email',
                        template='reset_password'
                    )
                )   

        redirect_url = f"{self.email_services.base_dir_notification}/{password_recovery_url}"
        full_name = f"{user.first_name} {user.last_name}".title()
        context = {
            'url': redirect_url,
            'lang': 'es',
            'full_name': full_name
        }
        message_body = template.render(context)

        subject = 'Reestablecer Contraseña'

        self.send_notification(user.email, subject, message_body)
    


    def notify_password_change_done(self, user: AbstractUser) -> None:
        template = loader.get_template(
                    self.template_path.format(
                        module='email',
                        template='reset_password_done'
                    )
                )

        full_name = f"{user.first_name} {user.last_name}".title()

        context = {
            'lang': 'es',
            'full_name': full_name,
            'username': user.username
        } 
        message_body = template.render(context)

        subject = 'Contraseña Reestablecida'

        return self.send_notification(user.email, subject, message_body)

