from datetime import time
from typing import Any
from core.auth.password_recovery import AuthPasswordServices
from core.exceptions import InvalidParameterException
from general.services import EmailServices
from users.email_services import UserEmailServices
from users.models import CustomUser as UserModel
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
class PasswordManagementService:

    def __init__(self) -> None:
        self._email_services = UserEmailServices(EmailServices())
        
    def change_password_request(self, user_email: str) -> dict[str, Any]:
        
        default_response = {
            'message': 'The request to change the password has been sent to the user email',
        }
        
        user = UserModel.objects.filter(email=user_email).first()
        if not user:
            ## add delay to avoid brute force attack
            time.sleep(1)
            return default_response
        
        _password_recovery_url = AuthPasswordServices.get_password_recovery_url(user)

        self._email_services.notify_for_requesting_password_change(user, _password_recovery_url)

        return default_response

    def update_password_by_request(self, *, token: str, code: str, new_password: str) -> dict[str, Any]:
        
        try:
            user_id = urlsafe_base64_decode(code).decode()
            user = UserModel.objects.get(pk=user_id)

        except Exception as e:
            raise InvalidParameterException('Invalid code parameter')
        
        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
           raise InvalidParameterException('Could not change the password, contact the support team')
        
        user.set_password(new_password)
        user.save()

        self._email_services.notify_password_change_done(user)

        return {'message': 'The password has been changed successfully'}
        



