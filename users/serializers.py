from typing import Any
from rest_framework import serializers
from users.models import CustomUser, ProfilePicture
from django.contrib.auth.models import Group, Permission
from core.auth import roles_services

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
        return roles_services.AuthRolesServices.get_roles_from_user(obj)
    
    def get_available_apps(self, obj):
        return roles_services.AuthRolesServices.get_app_roles_from_user(obj)

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password',
            'first_name', 
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'is_provider',
            'is_administrador_dcc',
            'phone'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict[str, Any]) -> CustomUser:
        """
        Creates a new CustomUser instance with the provided validated data.
        This method creates a new user, sets their password using Django's password hashing,
        and saves the user to the database.
        Args:
            validated_data (dict[str, Any]): A dictionary containing the validated user data
                including a 'password' field that will be hashed.
        Returns:
            CustomUser: The newly created user instance with hashed password.
        """

        password: str = validated_data.pop('password')
        user: CustomUser = super().create(validated_data)

        user.set_password(password)
        user.save()

        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'is_provider',
            'is_administrador_dcc',
            'phone'
        )





## DEPRECATED
## This serializer can not be removed because has a reference in report data
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'email', 'is_active', 'is_provider', 'is_administrador_dcc', 'phone')

