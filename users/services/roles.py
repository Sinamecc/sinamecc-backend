from typing import Any
from core.auth.roles_services import AuthRolesServices, RoleDict
from users.models import CustomUser as UserModel
from users.exceptions import UserNotFoundException
class UserRolesServices:

    def get_registered_roles(self) -> list[RoleDict]:
        return AuthRolesServices.get_all_registered_roles()
    
    def assign_role_to_user(self, user_id: int, role_list: list[str]) -> UserModel:

        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            raise UserNotFoundException
        
        user = AuthRolesServices.assign_roles_to_user(user, role_list)

        user.refresh_from_db()

        return user