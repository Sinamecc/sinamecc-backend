from rest_framework.test import APITestCase
from rest_framework import status
import pytest 
from .factories import UserCreationFactory
from users.models import CustomUser as UserModel



@pytest.fixture
def user() -> UserModel:
    return UserCreationFactory()


@pytest.mark.users
@pytest.mark.django_db
class UserResourceTests(APITestCase):

    
    def test_get_user_by_username(self, user: UserModel):
        api_client = self.client_class()
        api_client.force_authenticate(user=user)
        response = api_client.get(f'/api/v1/user/{user.username}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('username') == user.username
        assert response.data.get('first_name') == user.first_name
        assert response.data.get('last_name') == user.last_name
        assert response.data.get('is_staff') == user.is_staff
        assert response.data.get('email') == user.email
        assert response.data.get('is_active') == user.is_active
        assert response.data.get('is_provider') == user.is_provider
        assert response.data.get('is_administrador_dcc') == user.is_administrador_dcc
        assert response.data.get('phone') == user.phone

