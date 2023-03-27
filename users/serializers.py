from rest_framework import serializers
from users.models import CustomUser, ProfilePicture, UserRequest, Module
from django.contrib.auth.models import Group, Permission


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



class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name', 'code', 'active')


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = ('id', 'email', 'first_name', 'last_name', 'institution', 
                  'phone', 'module', 'created', 'updated', 'active')
