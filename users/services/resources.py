from typing import Any

from core.auth.password_recovery import AuthPasswordServices
from general.services import EmailServices
from users.exceptions import UserNotFoundException
from users.models import CustomUser as UserModel
from users.serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer
from users.services.emails import UserEmailServices

"""
NOTE: In the future we will change the way to return the data, currently we are returning a
tuple with the data and a boolean to indicate if the operation was successful or not, but this behavior
is not consistent with the rest of the services, so we will change it to return only the data and raise
"""

class UserResourcesService:

    def __init__(self) -> None:
        self._email_services = UserEmailServices(EmailServices())

    def get_by_id(self, id: int) -> UserModel:
        try:
            user = UserModel.objects.get(pk=id)

        except UserModel.DoesNotExist:
            raise UserNotFoundException
        
        return user


    def get_all(self, offset: int, limit: int) -> list[UserModel]:
        
        user_list = UserModel.objects.all()[offset: offset + limit]

        return list(user_list)
        
    
    def create(self, data: dict[str, Any]) -> UserModel:

        serialized_user = UserCreateSerializer(data=data)
        serialized_user.is_valid(raise_exception=True)
        user = serialized_user.save()

        _password_recovery_url = AuthPasswordServices.get_password_recovery_url(user)

        self._email_services.notify_new_user_creation_to_password_change(user, _password_recovery_url)

        return user
            

    def update(self, id: int, data: dict[str, Any]) -> UserModel:
        
        try:
            user = UserModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            raise UserNotFoundException
        
        serialized_user = UserUpdateSerializer(user, data=data, partial=True)
        serialized_user.is_valid(raise_exception=True)

        user = serialized_user.save()
        user.refresh_from_db()

        return user
        


    def delete(self, user_id: int) -> dict[str, Any]:
        
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            raise UserNotFoundException
        
        serialized_user = UserSerializer(user).data
        user.delete()

        return serialized_user
