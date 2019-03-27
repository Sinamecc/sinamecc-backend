from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, CustomGroup
from .serializers import CustomUserSerializer
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class UserService():
    def __init__(self):
        self.USER_DOES_NOT_EXIST = "User does not exist."

    def get(self, request, username):
    
        UserModel = get_user_model()
        try:
            user = UserModel.objects.filter(username=username).get()
            serialized_user = CustomUserSerializer(user)
            content_user = serialized_user.data
            content_user['groups'] = self.get_group_user(user)
            content_user['permission_app'] = self.get_permission_app(user)
            # we need this line for permissions in endpoints
            login(request, user)

            result = (True, content_user)
        except UserModel.DoesNotExist:
            result = (False, self.USER_DOES_NOT_EXIST)
        return result


    def get_group_user(self, user):
        groups_user = [
            {
                "id": g.id,
                "name": g.name,
                "label": g.custom_group.label
            } for g in user.groups.all()
        ]

        return groups_user

    def get_permission_app(self, user):
        permission_app = []
        for g in user.groups.all():
            permission_app.extend([ 
                {
                    'id': p.id,
                    'name': p.name,
                    'codename': p.codename, 
                    'app': ContentType.objects.get(id=p.content_type_id).app_label
                } for p in g.permissions.all() 
            ])
            
        return permission_app