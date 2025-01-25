from typing import Any
from rolepermissions import roles
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from typing import TypedDict
from django.db import transaction

from core.auth.exceptions import RoleGenericException


UserModel =  get_user_model()

class RoleDict(TypedDict):
    app: str
    role: str
    role_name: str
    available_permissions: list[dict[str, str]]

class AppRolesDict(TypedDict):
    reviewer: bool
    provider: bool

class AuthRolesServices:

    @staticmethod
    def get_roles_from_user(user: AbstractUser) -> list[RoleDict]: 
        
        user_roles = roles.get_user_roles(user)
        serialized_roles_lists = []
        for role in user_roles:
            serialized_roles_lists.append(RoleDict(
                app=role.app,
                role=role.get_name(),
                role_name=role.role,
                available_permissions=[
                    {permission.codename: permission.name}
                    for permission in role.get_default_true_permissions()
                ]
            ))

        return serialized_roles_lists
    
    @staticmethod
    def get_app_roles_from_user(user: AbstractUser) -> dict[str, AppRolesDict]:

        app_permissions = {}
        user_roles = roles.get_user_roles(user)

        for role in user_roles:
            apps_list = []
            if not isinstance(role.app, list):
                apps_list.append(role.app)
            else:
                apps_list = role.app
                
            for app in apps_list:
                if app in apps_list:
                    app_permissions[app] = AppRolesDict(
                        reviewer=False,
                        provider=False
                    )
                    app_permissions.get(app)[role.type] = True

                
        return app_permissions
    

    @staticmethod
    def get_all_registered_roles() -> list[RoleDict]:
        serialized_roles_lists = []
        for role in roles.registered_roles.values():
            serialized_roles_lists.append(RoleDict(
                app=role.app,
                role=role.get_name(),
                role_name=role.role,
                available_permissions=[
                    {permission.codename: permission.name}
                    for permission in role.get_default_true_permissions()
                ]
            ))

        return serialized_roles_lists


    @staticmethod
    def assign_roles_to_user(user: AbstractUser, role_list: list[str]) -> AbstractUser:
        try:
            with transaction.atomic():
                roles.clear_roles(user)
                [roles.assign_role(user, role) for role in role_list]

        except Exception as e:
            raise RoleGenericException('Could not assign roles to user')

        return user