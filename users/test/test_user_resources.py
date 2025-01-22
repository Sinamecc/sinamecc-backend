from typing import Any, List
from rest_framework.test import APIClient
from rest_framework import status
import pytest 
from .factories import UserCreationFactory
from users.models import CustomUser as UserModel


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def user() -> UserModel:
    return UserCreationFactory()

@pytest.fixture
def user_list() -> List[UserModel]:
    return UserCreationFactory.create_batch(5)

@pytest.mark.users
@pytest.mark.django_db
def test_get_user_by_username(api_client: APIClient,  user: UserModel):
    
    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/v1/users/{user.id}')

    response_user_data = response.data.get('data')

    assert response.status_code == status.HTTP_200_OK
    assert response_user_data.get('username') == user.username
    assert response_user_data.get('first_name') == user.first_name
    assert response_user_data.get('last_name') == user.last_name
    assert response_user_data.get('is_staff') == user.is_staff
    assert response_user_data.get('email') == user.email
    assert response_user_data.get('is_active') == user.is_active
    assert response_user_data.get('is_provider') == user.is_provider
    assert response_user_data.get('is_administrador_dcc') == user.is_administrador_dcc
    assert response_user_data.get('phone') == user.phone
    assert 'roles' in response_user_data
    assert 'available_apps' in response_user_data

@pytest.mark.users
@pytest.mark.django_db
def test_get_all_users(api_client: APIClient, user_list: List[UserModel]):
    admin_user = UserModel.objects.get_by_natural_key('admin')

    api_client.force_authenticate(user=admin_user)
    response = api_client.get(f'/api/v1/users?offset=0&limit=10')

    response_user_list_data: list[dict[str, Any]] = response.data.get('data')

    response_user_list_data = list(
                                filter(
                                    lambda user: user.get('username') not in ['admin', 'general_dcc', 'information_provider'],
                                    response_user_list_data)
                                )

    assert response.status_code == status.HTTP_200_OK
    assert len(response_user_list_data) == len(user_list)

    for i, user in enumerate(user_list):
        assert response_user_list_data[i].get('username') == user.username
        assert response_user_list_data[i].get('first_name') == user.first_name
        assert response_user_list_data[i].get('last_name') == user.last_name
        assert response_user_list_data[i].get('is_staff') == user.is_staff
        assert response_user_list_data[i].get('email') == user.email
        assert response_user_list_data[i].get('is_active') == user.is_active
        assert response_user_list_data[i].get('is_provider') == user.is_provider
        assert response_user_list_data[i].get('is_administrador_dcc') == user.is_administrador_dcc
        assert response_user_list_data[i].get('phone') == user.phone

        assert 'roles' in response_user_list_data[i]
        assert 'available_apps' in response_user_list_data[i]

