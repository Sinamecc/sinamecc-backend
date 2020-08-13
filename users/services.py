from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, ProfilePicture
from .serializers import CustomUserSerializer, NewCustomUserSerializer, PermissionSerializer, \
    GroupSerializer, ProfilePictureSerializer
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from rolepermissions import roles
from general.storages import S3Storage
from django.urls import reverse
import datetime
import os
from io import BytesIO
import json
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from general.services import EmailServices
from users.email_services import UserEmailServices
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator



ses_service = EmailServices()

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'


class UserService():
    def __init__(self):
        self.UNABLE_CREATE_USER = "Unable to create user"
        self.USER_DOESNT_EXIST = "The user doesn't exist"
        self.GROUP_DOESNT_EXIST = "The group doesn't exist"
        self.GROUP_DOESNT_HAVE_USERS = "The group {0} doesn't have associated users"
        self.ASSIGN_USER_GROUPS_ERROR = "Error at the moment of assigning user to groups."
        self.ASSIGN_USER_PERMISSION_ERROR = "Error at the moment of assigning user to permissions."
        self.UNASSIGN_USER_PERMISSION_ERROR = "Error at the moment of unassigning user to permissions."
        self.UNASSIGN_USER_GROUP_ERROR = "Error at the moment of unassigning user to groups."
        self.CREATE_GROUP_ERROR = "Error at the moment of create group."
        self.CREATE_PERMISSION_ERROR = "Error at the moment of create permissions."
        self.PROFILE_PICTURE_ERROR = "Error at the moment to create profile picture"
        self.SUCCESSFUL_REQUEST = "successful request"
        self.MISSING_EMAIL_ERROR = "missing email"
        self.RESET_PASSWORD_ERROR = "Error at the moment to reset password"
        self.storage = S3Storage()
        self.email_services = UserEmailServices(ses_service)
        self.token_generator = PasswordResetTokenGenerator()

    def get_serialized_profile_picture(self, request):
        version_str_format = '%Y%m%d_%H%M%S.%f'
        version_str = datetime.datetime.now().strftime(version_str_format)
        data = {
            'version': f'pp-{version_str}',
            'image': request.data.get('image'),
            'current': True,
            'user': request.data.get('user')
        }
        serializer = ProfilePictureSerializer(data=data)

        return serializer

    def get_serialized_new_user(self, request, user=False):
        new_user = {}
        for field in NewCustomUserSerializer.Meta.fields:
            if field in request.data:
                new_user[field] = request.data.get(field)

        if user:
            serializer = NewCustomUserSerializer(user, data=new_user)
        else:
            serializer = NewCustomUserSerializer(data=new_user)

        return serializer

    def get_serialized_permission(self, request, permission=False):
        new_permission = {}
        for field in PermissionSerializer.Meta.fields:
            if field in request.data:
                new_permission[field] = request.data.get(field)

        if permission:
            serializer = PermissionSerializer(permission, data=new_permission)
        else:
            serializer = PermissionSerializer(data=new_permission)

        return serializer

    def get_serialized_existing_user(self, request, user=False):
        existing_user = {}
        for field in CustomUserSerializer.Meta.fields:
            if field in request.data:
                existing_user[field] = request.data.get(field)

        if user:
            serializer = CustomUserSerializer(user, data=existing_user)
        else:
            serializer = CustomUserSerializer(data=existing_user)

        return serializer

    def get(self, request, username):

        UserModel = get_user_model()
        try:
            user = UserModel.objects.filter(username=username).get()
            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            validation_list = []
            available_apps_status, available_apps_data = self.get_user_app_roles(
                user)
            validation_list.append(available_apps_status)

            roles_status, roles_data = self.get_user_roles(user)
            validation_list.append(roles_status)

            profile_picture_status, profile_picture_data = self.get_current_profile_picture(
                user.id)
            validation_list.append(profile_picture_status)
            if all(validation_list):
                content_user['available_apps'] = available_apps_data
                content_user['roles'] = roles_data
                content_user['profile_picture'] = profile_picture_data if profile_picture_status else [
                ]
                result = (True, content_user)
                login(request, user)
            else:
                result = (False, self.USER_DOESNT_EXIST)

        except UserModel.DoesNotExist:
            result = (False, self.USER_DOESNT_EXIST)
        return result

    def get_user_roles(self, user):

        user_roles = roles.get_user_roles(user)
        serialized_roles_lists = []
        for role in user_roles:
            serialized_role = {}
            serialized_role['role'] = role.get_name()
            serialized_role['role_name'] = role.role
            # roles.get_or_create_permission(permission_codename) returns a tuple with the folllowing structure
            # (<Permission: users | user | Create Ppcn>, False), so for this reason we get the 0 index.
            serialized_role['available_permissions'] = [
                {kp: roles.get_or_create_permission(kp)[0].name} for kp, pv in role.available_permissions.items() if pv
            ]
            serialized_role['app'] = role.app

            serialized_roles_lists.append(serialized_role)

        result = (True, serialized_roles_lists)

        return result

    def get_user_app_roles(self, user):

        app_permissions = {}
        user_roles = roles.get_user_roles(user)

        result = (True, app_permissions)
        for role in user_roles:
            if isinstance(role.app, list):
                for app in role.app:
                    if not (app in app_permissions):
                        app_permissions[app] = {
                            'reviewer': False, 'provider': False}
                    app_permissions.get(app, {})[role.type] = True

            elif role.app in app_permissions:
                app_permissions.get(role.app, {})[role.type] = True

            else:
                app_permissions[role.app] = {
                    'reviewer': False, 'provider': False}
                app_permissions.get(role.app, {})[role.type] = True

        return result

    def get_all(self, request):
        UserModel = get_user_model()
        user_list = UserModel.objects.all()
        serialized_users_list = []
        for user in user_list:
            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            available_apps_status, available_apps_data = self.get_user_app_roles(
                user)
            roles_status, roles_data = self.get_user_roles(user)

            if available_apps_status and roles_status:
                content_user['available_apps'] = available_apps_data
                content_user['roles'] = roles_data
            serialized_users_list.append(content_user)

        result = (True, serialized_users_list)

        return result

    def create(self, request):
        errors = []
        result = (False, self.UNABLE_CREATE_USER)
        serialized_user = self.get_serialized_new_user(request)
        if serialized_user.is_valid():
            user = serialized_user.save()
            user.set_password(request.data.get('password'))
            user.save()

            result = (True, CustomUserSerializer(user).data)
        else:
            errors.append(serialized_user.errors)
            result = (False, errors)

        return result

    def get_permissions(self, request):
        permission_list = []
        perms = Permission.objects.exclude(
            codename__regex=r'^(change|add|delete)_.').all()
        for p in perms:
            permission_serialized = PermissionSerializer(p).data
            permission_list.append(permission_serialized)

        return (True, permission_list)

    # New method
    def create_permission(self, request):
        errors = []
        result = (False, self.CREATE_PERMISSION_ERROR)
        serialized_permission = self.get_serialized_permission(request)
        if serialized_permission.is_valid():
            saved_permission = serialized_permission.save()
            result = (True, PermissionSerializer(saved_permission).data)
        else:
            errors.append(serialized_permission.errors)
            result = (False, errors)

        return result

    def get_user_by_id(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
            return (True, user)
        except UserModel.DoesNotExist:

            return (False, self.USER_DOESNT_EXIST)

    def update(self, request, user_id):

        errors = []
        UserModel = get_user_model()
        user_query = UserModel.objects.filter(pk=user_id)
        if user_query.count() == 0:
            error = self.USER_DOESNT_EXIST
            return (False, error)
        user = user_query.last()
        serialized_user = self.get_serialized_existing_user(request, user)
        if serialized_user.is_valid():
            user = serialized_user.save()
            user.save()
            result = (True, CustomUserSerializer(user).data)

        else:
            errors.append(serialized_user.errors)
            result = (False, errors)

        return result

    def update_password(self, request, user_id):
        errors = []
        UserModel = get_user_model()
        user_query = UserModel.objects.filter(pk=user_id)
        if user_query.count() == 0:
            error = self.USER_DOESNT_EXIST
            return (False, error)

        user = user_query.last()
        user.set_password(request.data.get('password'))
        try:
            user.save()
            result = (True, CustomUserSerializer(user).data)

        except:
            errors.append(user.errors)
            result = (False, errors)

        return result


    def request_to_change_password(self, request):

        data = request.data
        UserModel = get_user_model()
        user_email = data.get('email', False)
        result = (True, self.SUCCESSFUL_REQUEST)
        if user_email:
            try:
                user = UserModel.objects.get(email=user_email)
                encode_b64_user_id_status, encode_b64_user_id_data = self.encode_b64_user_id(user.pk)
                if encode_b64_user_id_status:
                    email_status, email_data = self.email_services.notify_for_requesting_password_change(user, encode_b64_user_id_data)
                    
            except UserModel.DoesNotExist:
                result = (True, self.SUCCESSFUL_REQUEST)

        else:
            
            result = (False, self.MISSING_EMAIL_ERROR)

        return result

    

    def update_password_by_request(self, request, token, code):

        user_id_status, user_id_data = self.decode_b64_user_id(code)
        if user_id_status:
            UserModel = get_user_model()
            user_query = UserModel.objects.filter(pk=user_id_data).last()
            if user_query:
                if self.token_generator.check_token(user_query, token):
                    print(request.data.get('password'))
                    user_query.set_password(request.data.get('password'))
                    user_query.save()
                    result = (True, CustomUserSerializer(user_query).data)

                else:
                    result = (False, self.RESET_PASSWORD_ERROR)

            else:
                result = (False, self.RESET_PASSWORD_ERROR)
        else:
            result = (user_id_status, user_id_data)

        return result

        errors = []


    def get_all_profile_picture(self, user_id):

        UserModel = get_user_model()
        user_query = UserModel.objects.filter(pk=user_id)
        if user_query.count() == 0:
            error = self.USER_DOESNT_EXIST
            result = (False, error)
        else:
            user = user_query.last()
            profile_picture = self._get_profile_picture_list(
                user.profile_picture)

            result = (True, profile_picture)

        return result

    def get_current_profile_picture(self, user_id):

        UserModel = get_user_model()
        user_query = UserModel.objects.filter(pk=user_id)
        if user_query.count() == 0:
            error = self.USER_DOESNT_EXIST
            result = (False, error)
        else:
            user = user_query.last()
            profile_picture = self._get_profile_picture_list(
                user.profile_picture.filter(current=True))

            result = (True, profile_picture)

        return result

    def download_profile_picture(self, image_id, user_id):
        return self.get_file_content(image_id, user_id)

    def get_file_content(self,  image_id, user_id):
        profile_picture = ProfilePicture.objects.get(
            id=image_id, user__id=user_id)
        path, filename = os.path.split(profile_picture.image.name)
        return (filename, BytesIO(self.storage.get_file(profile_picture.image.name)))

    def create_profile_picture(self, request, user_id):

        result = (False, self.PROFILE_PICTURE_ERROR)
        UserModel = get_user_model()
        user_query = UserModel.objects.filter(pk=user_id)
        if user_query.count() == 0:
            error = self.USER_DOESNT_EXIST
            result = (False, error)
        else:
            serialized_profile_picture = self.get_serialized_profile_picture(
                request)
            if serialized_profile_picture.is_valid():

                profile_picture_query = ProfilePicture.objects.filter(
                    user__id=user_id, current=True)
                for pp in profile_picture_query:
                    pp.current = False
                    pp.save()

                profile_picture = serialized_profile_picture.save()

                profile_picture_content = ProfilePictureSerializer(
                    profile_picture).data
                profile_picture_content['name'] = self._get_filename(
                    profile_picture.image.name)
                profile_picture_content['image'] = self._get_profile_picture_path(
                    str(profile_picture.user.id), str(profile_picture.id))

                result = (True, profile_picture_content)

            else:
                result = (False, serialized_profile_picture.errors)

        return result

    # Refactor user module for get all attr

    def assign_role_to_user(self, request, user_id):

        UserModel = get_user_model()
        try:
            user = UserModel.objects.filter(pk=user_id).get()
            roles_list = json.loads(request.data.get('roles'))
            roles.clear_roles(user)
            for role in roles_list:
                roles.assign_role(user, role)

            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data

            available_apps_status, available_apps_data = self.get_user_app_roles(
                user)
            roles_status, roles_data = self.get_user_roles(user)
            if available_apps_status and roles_status:
                content_user['available_apps'] = available_apps_data
                content_user['roles'] = roles_data

            result = (True, content_user)

        except UserModel.DoesNotExist:
            result = (False, self.USER_DOESNT_EXIST)

        return result

    def get_roles(self, request):

        result = (True, {})
        roles_registered = roles.registered_roles.items()
        serialized_roles_lists = []
        for k, v in roles_registered:
            serialized_role = {}
            serialized_role['role'] = k
            serialized_role['role_name'] = v.role
            # roles.get_or_create_permission(permission_codename) returns a tuple with the folllowing structure
            # (<Permission: users | user | Create Ppcn>, False), so for this reason we get the 0 index.

            serialized_role['available_permissions'] = [
                {kp: roles.get_or_create_permission(kp)[0].name} for kp, pv in v.available_permissions.items() if pv
            ]
            serialized_role['app'] = v.app

            serialized_roles_lists.append(serialized_role)

        result = (True, serialized_roles_lists)
        return result

    def _get_profile_picture_list(self, profile_picture_list):

        profile_picture_list = [
            {
                'id': profile_picture.id,
                'current': profile_picture.current,
                'name': self._get_filename(profile_picture.image.name),
                'image': self._get_profile_picture_path(str(profile_picture.user.id), str(profile_picture.id))

            } for profile_picture in profile_picture_list.all()
        ]

        return profile_picture_list

    def _get_profile_picture_path(self, user_id, image_id):
        url = reverse("get_profile_picture_version", kwargs={
                      'user_id': user_id, 'image_id': image_id})
        return url

    def _get_filename(self, filename):
        fpath, fname = os.path.split(filename)
        return fname


    def encode_b64_user_id(self, user_id):
        encoding = 'utf-8'
        rand_len =  int(get_random_string(1, "3456789"))
        list_to_encode_id = ["{0}{1}".format(x, y) for x, y in zip((list(get_random_string(rand_len - 1)) + [str(hex(user_id + rand_len)[2:])]) , \
                                                                    [str(rand_len)] + list(get_random_string(rand_len-1)))]
        user_b64 = str(urlsafe_base64_encode(force_bytes("".join(list_to_encode_id))), encoding)

        return True , user_b64

    def decode_b64_user_id(self, encoded_user_id):
        encoding = 'utf-8'
        try:
            decoded_user_id = str(urlsafe_base64_decode(encoded_user_id), encoding)
            rand_len = int(decoded_user_id[1])
            user_id = int(decoded_user_id[((rand_len -1 ) * 2) : -1], 16) - rand_len
            result =  (True, user_id)
        except Exception as exc:
            result = (False, self.RESET_PASSWORD_ERROR)

        return result
        