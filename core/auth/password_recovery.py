
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class AuthPasswordServices:

    @staticmethod
    def get_password_recovery_url(
            user: AbstractUser
    ) -> str:
        """
        Get the password recovery URL for the user. 
        The token is valid for 24 hours. (change it in the settings PASSWORD_RESET_TIMEOUT)
        Args:
            user (AbstractUser): The user for which to generate the password recovery URL.
        Returns:
            str: The password recovery URL for the user.
        """
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        return f"changePassword?code={uid}&token={token}"

 