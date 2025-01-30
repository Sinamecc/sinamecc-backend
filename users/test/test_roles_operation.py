from typing import Any
import pytest
from rest_framework.test import APIClient
from users.models import CustomUser as UserModel
from users.test.factories import UserCreationFactory
from core.auth.roles_services import AuthRolesServices

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def user() -> UserModel:
    return UserCreationFactory()


@pytest.mark.users
@pytest.mark.django_db
def test_get_all_roles(user: UserModel, api_client: APIClient) -> None:

    api_client.force_authenticate(user=user)

    response = api_client.get('/api/v1/users/roles')
    assert response.status_code == 200
    assert isinstance(response.data.get('data'), list)

    for role in response.data.get('data'):
        assert 'app' in role
        assert 'role' in role
        assert 'role_name' in role
        assert 'available_permissions' in role

        assert isinstance(role.get('available_permissions'), list)

        for permission in role.get('available_permissions'):
            assert isinstance(permission, dict)


@pytest.mark.users
@pytest.mark.django_db
def test_assign_role_to_user(user: UserModel, api_client: APIClient) -> None:

    api_client.force_authenticate(user=user)
    request_body = {
        'roles': [
            'information_provider_ppcn',
            'information_provider_mitigation_action'
        ]
    }

    response = api_client.post(f'/api/v1/users/{user.id}/roles', data=request_body, format='json')
    assert response.status_code == 200
    roles_from_user = AuthRolesServices.get_roles_from_user(user)
    assert len(roles_from_user) == 2

    codename_role_list = [ x.get('role') for x in roles_from_user]

    assert 'information_provider_ppcn' in codename_role_list
    assert 'information_provider_mitigation_action' in codename_role_list

    ## check the response data
    roles_from_response: list[dict[str, Any]] = response.data.get('data').get('roles')
    assert len(roles_from_response) == 2

    for role in roles_from_response:
        if role.get('role') == 'information_provider_ppcn':
            assert role.get('role_name') == 'Information Provider PPCN'
            assert role.get('app') == 'ppcn'
            assert 'available_permissions' in role
        elif role.get('role') == 'information_provider_mitigation_action':
            assert role.get('role_name') == 'Information Provider Mitigation Action'
            assert role.get('app') == 'ma'
            assert 'available_permissions' in role
        else:
            assert False, 'Role not found in response'

    apps_from_response = response.data.get('data').get('available_apps')

    assert apps_from_response.get('ppcn') == {'reviewer': False, 'provider': True}
    assert apps_from_response.get('ma') == {'reviewer': False, 'provider': True}

