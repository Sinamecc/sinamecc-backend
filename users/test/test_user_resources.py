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

@pytest.mark.users
@pytest.mark.django_db
def test_create_user(api_client: APIClient, user: UserModel):
    admin_user = UserModel.objects.get_by_natural_key('admin')
    api_client.force_authenticate(user=admin_user)
    test_user = UserCreationFactory.build()
    
    new_user_data = {
        "username": test_user.username,
        "password": "testpass123",  # Keep a static password for testing
        "first_name": test_user.first_name,
        "last_name": test_user.last_name,
        "email": test_user.email,
        "is_staff": test_user.is_staff,
        "is_active": test_user.is_active,
        "is_provider": test_user.is_provider,
        "is_administrador_dcc": test_user.is_administrador_dcc,
        "phone": test_user.phone
    }
    
    response = api_client.post('/api/v1/users', new_user_data, format='json')
    response_data = response.data.get('data')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data.get('username') == new_user_data['username']
    assert response_data.get('first_name') == new_user_data['first_name']
    assert response_data.get('email') == new_user_data['email']
    assert response_data.get('is_staff') == new_user_data['is_staff']
    assert response_data.get('is_active') == new_user_data['is_active']
    assert response_data.get('is_provider') == new_user_data['is_provider']
    assert response_data.get('is_administrador_dcc') == new_user_data['is_administrador_dcc']
    assert response_data.get('phone') == new_user_data['phone']
    assert 'roles' in response_data
    assert 'available_apps' in response_data
    assert 'password' not in response_data

@pytest.mark.users
@pytest.mark.django_db
def test_update_user(api_client: APIClient, user: UserModel):
    admin_user = UserModel.objects.get_by_natural_key('admin')
    api_client.force_authenticate(user=admin_user)
    
    updated_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "email": "updated@test.com",
        "phone": "999999999"
    }
    
    response = api_client.put(f'/api/v1/users/{user.id}', updated_data, format='json')
    response_data = response.data.get('data')
    
    assert response.status_code == status.HTTP_200_OK
    assert response_data.get('first_name') == updated_data['first_name']
    assert response_data.get('last_name') == updated_data['last_name'] 
    assert response_data.get('email') == updated_data['email']
    assert response_data.get('phone') == updated_data['phone']
    assert response_data.get('is_staff') == user.is_staff
    assert response_data.get('is_active') == user.is_active
    assert response_data.get('is_provider') == user.is_provider
    assert response_data.get('is_administrador_dcc') == user.is_administrador_dcc
    assert 'roles' in response_data
    assert 'available_apps' in response_data

@pytest.mark.users
@pytest.mark.django_db
def test_delete_user(api_client: APIClient, user: UserModel):
    admin_user = UserModel.objects.get_by_natural_key('admin')
    api_client.force_authenticate(user=admin_user)
    
    test_user_dict = {
        "username": user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'is_provider': user.is_provider,
        'is_administrador_dcc': user.is_administrador_dcc,
        'phone': user.phone
    }

    response = api_client.delete(f'/api/v1/users/{user.id}')
    response_data = response.data.get('data')
    
    assert response.status_code == status.HTTP_200_OK
    assert not UserModel.objects.filter(id=user.id).exists()
    
    assert response_data.get('username') == test_user_dict['username']
    assert response_data.get('first_name') == test_user_dict['first_name']
    assert response_data.get('last_name') == test_user_dict['last_name']
    assert response_data.get('email') == test_user_dict['email']
    assert response_data.get('is_staff') == test_user_dict['is_staff']
    assert response_data.get('is_active') == test_user_dict['is_active']
    assert response_data.get('is_provider') == test_user_dict['is_provider']
    assert response_data.get('is_administrador_dcc') == test_user_dict['is_administrador_dcc']
    assert response_data.get('phone') == test_user_dict['phone']
    assert 'roles' in response_data
    assert 'available_apps' in response_data



  



# @pytest.mark.users
# @pytest.mark.django_db
# def test_unauthorized_user_operations(api_client: APIClient, user: UserModel):
#     # Unauthenticated requests
#     response = api_client.get(f'/api/v1/users/{user.id}')
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
#     response = api_client.get('/api/v1/users')
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
#     # Non-admin user trying to access admin-only endpoints
#     api_client.force_authenticate(user=user)
#     response = api_client.get('/api/v1/users')
#     assert response.status_code == status.HTTP_403_FORBIDDEN
