from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, CustomGroup
from .serializers import CustomUserSerializer, NewCustomUserSerializer, PermissionSerializer, GroupSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login

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
        self.GROUP_DOESNT_HAVE_USERS = "The group {0} doesn't have user associates"
        self.ERROR_ASSIGN_USER_GROUPS = "Error at the moment of assigning user to groups."
        self.ERROR_ASSIGN_USER_PERMISSION = "Error at the moment of assigning user to permissions."


    def get_serialized_new_user(self, request, user = False):
        new_user = {}
        for field in NewCustomUserSerializer.Meta.fields:
            if field in request.data:
                new_user[field] = request.data.get(field)

        if user:
            serializer = NewCustomUserSerializer(user, data = new_user)
        else:
            serializer = NewCustomUserSerializer(data = new_user)


        return serializer

    def get(self, request, username):
    
        UserModel = get_user_model()
        try:
            user = UserModel.objects.filter(username=username).get()
            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            content_user['groups'] = self.get_user_groups(user)
            content_user['permission_app'] = self.get_permission_app(user)
            content_user['available_apps'] = self.get_available_app(user)
            # we need this line for permissions in endpoints
            login(request, user)
            result = (True, content_user)
        except UserModel.DoesNotExist:
            result = (False, self.USER_DOESNT_EXIST)
        return result

    def get_all(self, request):
        UserModel = get_user_model()
        user_list = UserModel.objects.all()
        serialized_users_list = []
        for user in user_list:
            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            content_user['groups'] = self.get_user_groups(user)
            content_user['permission_app'] = self.get_permission_app(user)
            serialized_users_list.append(content_user)

        result = (True, serialized_users_list)

        return result
    def get_user_groups(self, user):
       
        user_groups = [
            {
                "id": g.id,
                "name": g.name,
                "label": g.custom_group.label
            } for g in (Group.objects.all() if user.is_superuser else user.groups.all())
        ]

        return user_groups


    def get_available_app(self, user):
        permission_groups = []

        permission_user = [p for p in user.user_permissions.all()] 
        for g in user.groups.all():
            permission_groups.extend([p for p in g.permissions.all()])
        permission = Permission.objects.all() if user else list(set(permission_user) | set(permission_groups)) 

        available_apps = {}
        for p in permission:
            app = ContentType.objects.get(id=p.content_type_id).app_label
            if not (app in available_apps):
                available_apps[app] = True
        return available_apps
        


    def get_permission_app(self, user):
        permission_groups = []
        permission_user = [p for p in user.user_permissions.all()] 
        for g in user.groups.all():
            permission_groups.extend([p for p in g.permissions.all()])
        permission = list(set(permission_user) | set(permission_groups)) 
        
        permission_app = [
            {
                'id': p.id,
                'name': p.name,
                'codename': p.codename, 
                'app': ContentType.objects.get(id=p.content_type_id).app_label
            } for p in permission
        ]

        return permission_app

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


    def assign_user_to_permission(self, request, username):
        key = 'permissions'
        UserModel = get_user_model()
        result = (False, None)
        user = UserModel.objects.get(username=username)
        if key in request.data:
            for p in request.data.get(key):    
                user.user_permissions.add(p)

            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            content_user['groups'] = self.get_user_groups(user)
            content_user['permission_app'] = self.get_permission_app(user)
            result = (True, content_user)
        else:
            result = (False, self.ERROR_ASSIGN_USER_PERMISSION)
            
        return result


    def assign_user_to_group(self, request, username):

        key = 'groups'
        UserModel = get_user_model()
        result = (False, None)
        user = UserModel.objects.get(username=username)
        if key in request.data:
            for g in request.data.get(key):
                user.groups.add(g)
            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            content_user['groups'] = self.get_user_groups(user)
            content_user['permission_app'] = self.get_permission_app(user)
            result = (True, content_user)
        else:
            result = (False, self.ERROR_ASSIGN_USER_GROUPS)
            
        return result

    def get_permissions(self, request):
        permission_list = []
        perms = Permission.objects.exclude(codename__regex=r'^(change|add|delete)_.').all()
        for p in perms:
            permission_serialized = PermissionSerializer(p).data
            permission_list.append(permission_serialized)
            
        return (True, permission_list)

    
    def get_groups(self, request):

        group_list = []
        for g in Group.objects.all():
            group_serialized = GroupSerializer(g).data
            group_serialized['label'] = g.custom_group.label
            group_list.append(group_serialized)
            
        return (True, group_list)
    
    def get_group_users(self, group_name):
        UserModel = get_user_model()
        user_in_group = UserModel.objects.filter(groups__name=group_name)
        if user_in_group.count() == 0: 
            error = self.GROUP_DOESNT_HAVE_USERS.format(group_name)
            return (False, error)

        user_list = []
        for user in user_in_group.all():
            user_list.append(user.email)

        return (True, user_list)

    def get_user_by_id(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk= user_id)
            return (True, user)
        except UserModel.DoesNotExist:

            return (False, self.USER_DOESNT_EXIST) 
