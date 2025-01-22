from typing import Any
from users.models import CustomUser as UserModel
from users.exceptions import UserNotFoundException
from users.serializers import UserSerializer
from core.auth import roles

"""
NOTE: In the future we will change the way to return the data, currently we are returning a
tuple with the data and a boolean to indicate if the operation was successful or not, but this behavior
is not consistent with the rest of the services, so we will change it to return only the data and raise
"""

class UserResourcesService:

    
    def get_by_id(self, id: int) -> dict[str, Any]:
        try:
            user = UserModel.objects.get(pk=id)

        except UserModel.DoesNotExist:
            raise UserNotFoundException

        serialized_user = UserSerializer(user).data

        return serialized_user

            

    def get_all(self, offset: int, limit: int) -> None:
        
        user_list = UserModel.objects.all()[offset: offset + limit]

        serialized_user_list = UserSerializer(user_list, many=True).data

        return serialized_user_list
        
    
    def create(self, data: dict[str, Any]) ->None:
        ...
    

    def update(self, data: dict[str, Any]) -> None:
        ...
    
    def delete(self, user_id: int) -> None:
        ...

    