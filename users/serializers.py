from rest_framework import serializers
from users.models import CustomUser, ProfilePicture
from django.contrib.auth.models import Group, Permission
from core.auth import roles

class UserSerializer(serializers.ModelSerializer):

    roles = serializers.SerializerMethodField()
    available_apps = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'email',
            'is_active',
            'is_provider',
            'is_administrador_dcc',
            'phone',
            'roles',
            'available_apps'
        )

    def get_roles(self, obj):
        return roles.AuthRolesServices.get_roles_from_user(obj)
    
    def get_available_apps(self, obj):
        return roles.AuthRolesServices.get_app_roles_from_user(obj)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'email', 'is_active', 'is_provider', 'is_administrador_dcc', 'phone')

class NewCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_provider', 'is_administrador_dcc', 'phone')

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ('id', 'user', 'image', 'current', 'version')



## Review This
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename', 'content_type')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

