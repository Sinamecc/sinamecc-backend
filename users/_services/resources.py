from typing import Any
from general.services import EmailServices
from users.email_services import UserEmailServices
from users.models import CustomUser as UserModel
from users.exceptions import UserNotFoundException
from users.serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer
from core.auth import roles
from core.auth.password_recovery import AuthPasswordServices
"""
NOTE: In the future we will change the way to return the data, currently we are returning a
tuple with the data and a boolean to indicate if the operation was successful or not, but this behavior
is not consistent with the rest of the services, so we will change it to return only the data and raise
"""

class UserResourcesService:

    def __init__(self) -> None:
        self._email_services = UserEmailServices(EmailServices())

    def get_by_id(self, id: int) -> dict[str, Any]:
        try:
            user = UserModel.objects.get(pk=id)

        except UserModel.DoesNotExist:
            raise UserNotFoundException

        serialized_user = UserSerializer(user).data

        return serialized_user


    def get_all(self, offset: int, limit: int) -> list[dict[str, Any]]:
        
        user_list = UserModel.objects.all()[offset: offset + limit]

        serialized_user_list = UserSerializer(user_list, many=True).data

        return serialized_user_list
        
    
    def create(self, data: dict[str, Any]) -> dict[str, Any]:

        serialized_user = UserCreateSerializer(data=data)
        serialized_user.is_valid(raise_exception=True)
        user = serialized_user.save()

        _password_recovery_url = AuthPasswordServices.get_password_recovery_url(user)

        self._email_services.notify_new_user_creation_to_password_change(user, _password_recovery_url)

        serialized_new_user = UserSerializer(user).data

        return serialized_new_user
            

    def update(self, id: int, data: dict[str, Any]) -> dict[str, Any]:
        
        try:
            user = UserModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            raise UserNotFoundException
        
        serialized_user = UserUpdateSerializer(user, data=data, partial=True)
        serialized_user.is_valid(raise_exception=True)

        user = serialized_user.save()

        serialized_user = UserSerializer(user).data

        return serialized_user
        


    def delete(self, user_id: int) -> dict[str, Any]:
        
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            raise UserNotFoundException
        
        serialized_user = UserSerializer(user).data
        user.delete()

        return serialized_user


    