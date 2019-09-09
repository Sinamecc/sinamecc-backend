from rest_framework import serializers
from users.models import CustomUser, CustomGroup
from django.contrib.auth.models import Group, Permission


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'email', 'is_active', 'is_provider', 'is_administrador_dcc', 'phone')

class NewCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_provider', 'is_administrador_dcc', 'phone')

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename', 'content_type')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class CustomGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGroup
        fields = ('id', 'label', 'group')
