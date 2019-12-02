from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, CustomGroup
from .serializers import CustomUserSerializer, NewCustomUserSerializer, PermissionSerializer, \
    GroupSerializer, CustomGroupSerializer
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login
from rolepermissions import roles

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
        self.GROUP_DOESNT_HAVE_USERS = "The group {0} doesn't have user associates"
        self.ASSIGN_USER_GROUPS_ERROR = "Error at the moment of assigning user to groups."
        self.ASSIGN_USER_PERMISSION_ERROR = "Error at the moment of assigning user to permissions."
        self.UNASSIGN_USER_PERMISSION_ERROR = "Error at the moment of unassigning user to permissions."
        self.UNASSIGN_USER_GROUP_ERROR = "Error at the moment of unassigning user to groups."
        self.CREATE_GROUP_ERROR = "Error at the moment of create group."
        self.CREATE_PERMISSION_ERROR = "Error at the moment of create permissions."


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

    def get_serialized_permission(self, request, permission = False):
        new_permission = {}
        for field in PermissionSerializer.Meta.fields:
            if field in request.data:
                new_permission[field] = request.data.get(field)

        if permission:
            serializer = PermissionSerializer(permission, data = new_permission)
        else:
            serializer = PermissionSerializer(data = new_permission)

        return serializer

    def get_serialized_group(self, request, group = False):
        new_group = {}
        for field in GroupSerializer.Meta.fields:
            if field in request.data:
                new_group[field] = request.data.get(field)

        if group:
            serializer = GroupSerializer(group, data = new_group)
        else:
            serializer = GroupSerializer(data = new_group)

        return serializer
    
    def get_serialized_label_group(self, request, group_id = False, label_group = False):

        new_label_group = {}
        for field in CustomGroupSerializer.Meta.fields:
            if field in request.data:
                new_label_group[field] = request.data.get(field)

        if group_id : new_label_group['group'] = group_id
 
        if label_group: 
            serializer = CustomGroupSerializer(label_group, data = new_label_group, partial=True)
        else: 
            serializer = CustomGroupSerializer(data = new_label_group)

        return serializer

    
    def get_serialized_existing_user(self, request, user = False):
        existing_user = {}
        for field in CustomUserSerializer.Meta.fields:
            if field in request.data:
                existing_user[field] = request.data.get(field)

        if user:
            serializer = CustomUserSerializer(user, data = existing_user)
        else:
            serializer = CustomUserSerializer(data = existing_user)

        return serializer

    def get(self, request, username):
    
        UserModel = get_user_model()
        try:
            user = UserModel.objects.filter(username=username).get()
            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            available_apps_status, available_apps_data = self.get_user_roles(user)
            if available_apps_status:
                content_user['available_apps'] = available_apps_data
                result = (True, content_user)
                login(request, user)
            else:
                result = (False, self.USER_DOESNT_EXIST)
            
            
        except UserModel.DoesNotExist:
            result = (False, self.USER_DOESNT_EXIST)
        return result

    def get_user_roles(self, user):
        
        app_permissions = {}
        user_roles = roles.get_user_roles(user)

        result = (True, app_permissions)
        for role in user_roles:
            if isinstance(role.app, list):
                for app in role.app:
                    if not (app in app_permissions):
                        app_permissions[app] = {'reviewer':False, 'provider':False}
                    app_permissions.get(app, {})[role.type] = True

            elif role.app in app_permissions:
                    app_permissions.get(role.app, {})[role.type] = True

            else:
                app_permissions[role.app] = {'reviewer':False, 'provider':False}
                app_permissions.get(role.app, {})[role.type] = True

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

    
    def get_available_app(self, user):
        permission_groups = []

        permission_user = [p for p in user.user_permissions.all()] 
        for g in user.groups.all():
            permission_groups.extend([p for p in g.permissions.all()])
        permission = Permission.objects.all() if user.is_superuser else list(set(permission_user) | set(permission_groups)) 

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
            result = (False, self.ASSIGN_USER_PERMISSION_ERROR)
            
        return result

    
    def unassign_user_to_permission(self, request, username):
        key = 'permissions'
        UserModel = get_user_model()
        result = (False, None)
        user = UserModel.objects.get(username=username)
        remove_permission = lambda perm, user = user : user.user_permissions.remove(perm)

        if key in request.data and isinstance(request.data.get(key), list):
            list(map(remove_permission, request.data.get(key)))
            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            content_user['groups'] = self.get_user_groups(user)
            content_user['permission_app'] = self.get_permission_app(user)
            result = (True, content_user)

        else:
            result = (False, self.UNASSIGN_USER_PERMISSION_ERROR)
            
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
            result = (False, self.ASSIGN_USER_GROUPS_ERROR)
            
        return result
    
    def unassign_user_to_group(self, request, username):
        key = 'groups'
        UserModel = get_user_model()
        result = (False, None)
        user = UserModel.objects.get(username=username)
        remove_group = lambda perm, user = user : user.groups.remove(perm)

        if key in request.data and isinstance(request.data.get(key), list):
            list(map(remove_group, request.data.get(key)))
            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            content_user['groups'] = self.get_user_groups(user)
            content_user['permission_app'] = self.get_permission_app(user)
            result = (True, content_user)

        else:
            result = (False, self.UNASSIGN_USER_GROUP_ERROR)
            
        return result

    def get_permissions(self, request):
        permission_list = []
        perms = Permission.objects.exclude(codename__regex=r'^(change|add|delete)_.').all()
        for p in perms:
            permission_serialized = PermissionSerializer(p).data
            permission_list.append(permission_serialized)
            
        return (True, permission_list)

    ## New method 
    def create_permission(self, request):
        errors = []
        result = (False, self.CREATE_PERMISSION_ERROR)
        serialized_permissioon = self.get_serialized_permission(request)
        if serialized_permissioon.is_valid():
            saved_permission = serialized_permissioon.save()
            result = (True, PermissionSerializer(saved_permission).data)
        else:
            errors.append(serialized_permissioon.errors)
            result = (False, errors)

        return result
    
    def get_group(self, request, group_id):
        errors = []
        result = (False, self.GROUP_DOESNT_EXIST)
        group_query = Group.objects.filter(pk=group_id)
        if group_query.count() > 0:
            group = group_query.last()
            serialized_group = GroupSerializer(group).data
            serialized_group["label"] = group.custom_group.label
            result = (True, serialized_group)

        return result
    
    def update_group(self, request, group_id):
        errors = []
        result = (False, self.GROUP_DOESNT_EXIST)
        group_query = Group.objects.filter(pk=group_id)
        if group_query.count() > 0:
            group = group_query.last()
            label_group = group.custom_group

            serialized_group = self.get_serialized_group(request, group)
            serialized_label = self.get_serialized_label_group(request, label_group=label_group)
            validation = [serialized_group.is_valid(), serialized_label.is_valid()]
            if validation.count(False) == 0:
                group = serialized_group.save()
                serialized_label.save()
                serialized_group = GroupSerializer(group).data
                serialized_group["label"] =  group.custom_group.label   
                result = (True, serialized_group)
            else: 
                errors.append(serialized_group.errors)
                errors.append(serialized_label.errors)
                result = (False, errors)            

        return result

    def get_all_groups(self, request):

        group_list = []
        for g in Group.objects.all():
            group_serialized = GroupSerializer(g).data
            group_serialized['label'] = g.custom_group.label
            group_list.append(group_serialized)
            
        return (True, group_list)
    
    def create_label_group(self, request, group_id):
        errors = []
        result = (False, self.CREATE_GROUP_ERROR)
        serialized_label_group = self.get_serialized_label_group(request, group_id=group_id)

        if serialized_label_group.is_valid():
            serialized_label_group.save()
            result = (True, CustomGroupSerializer(data = serialized_label_group))
        else:
            errors.append(serialized_label_group.errors)
            result = (False, errors)

        return result

    def create_group(self, request):
        
        errors = []
        result = (False, self.CREATE_GROUP_ERROR)

        serialized_group = self.get_serialized_group(request)
        if serialized_group.is_valid():
            saved_group = serialized_group.save()
            group_id = saved_group.id
            result_status, result_detail = self.create_label_group(request, group_id)
            if result_status:
                group_serialized = GroupSerializer(saved_group).data
                group_serialized['label'] = saved_group.custom_group.label
                result = (True, group_serialized)
            else: 
                errors.append(result_detail)
                result = (False, errors)
        else:
            errors.append(serialized_group.errors)
            result = (False, errors)

        return result
        
    
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
        user  = user_query.last()
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

        user  = user_query.last()
        user.set_password(request.data.get('password'))
        try:
            user.save()
            result = (True, CustomUserSerializer(user).data)

        except :
            errors.append(user.errors)
            result = (False, errors)

        return result

   
def jwt_response_payload_handler(token, user=None, request=None):
    return {
    'token': token,
    'user': {'username':user.username}
}
        

        

