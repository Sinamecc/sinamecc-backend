
from typing import Any
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from core.auth.roles_services import AuthRolesServices
from django.contrib.auth.models import AbstractUser
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: AbstractUser) -> dict[str, Any]:
        
        payload = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        payload['email'] = user.email
        payload['username'] = user.username
        payload['available_apps'] = AuthRolesServices.get_roles_from_user(user)
        
        return payload
    
    def validate(self, attrs: dict[str, Any] ) -> dict[str, Any]:
        data = super().validate(attrs)

        data['token'] = data['access']
        data['user_id'] = self.user.id

        del data['access']
        del data['refresh']

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

