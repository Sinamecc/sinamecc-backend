
from typing import Any
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from users.services import UserService

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        _service = UserService()
        payload = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        available_apps_status, available_apps_data = _service.get_user_roles(user)
        payload['email'] = user.email
        payload['username'] = user.username
        if available_apps_status:
                payload['available_apps'] = available_apps_data
        
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

