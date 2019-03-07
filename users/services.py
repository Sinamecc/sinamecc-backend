from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, CustomGroup
from django.contrib.auth import get_user_model

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

    def get(self, username):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.filter(username=username).get()
            result_user = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "groups": [
                    {
                        "id": g.id,
                        "name": g.name,
                        "label": CustomGroup.objects.get(id=g.id).label
                    } for g in user.groups.all()
                ]
            }
            result = (True, result_user)
        except UserModel.DoesNotExist:
            result = (False, self.USER_DOES_NOT_EXIST)
        return result