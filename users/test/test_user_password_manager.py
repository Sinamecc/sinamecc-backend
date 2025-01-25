import pytest
from pytest_mock import MockFixture
from rest_framework.test import APIClient
from users.models import CustomUser as UserModel
from users.test.factories import UserCreationFactory
from core.auth.password_recovery import AuthPasswordServices

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def user() -> UserModel:
    return UserCreationFactory()

@pytest.mark.users
@pytest.mark.django_db
def test_reset_password_without_email(user: UserModel, api_client: APIClient, mocker: MockFixture):

    mocker.patch('users.services.email.UserEmailServices.notify_for_requesting_password_change', return_value=None)
    NEW_PASSWORD = 'new_password'
    CURRENT_PASSWORD = 'current_password'

    user.set_password(CURRENT_PASSWORD)
    user.save()

    request_body_for_requesting_reset_password = {
        'email': user.email
    }
    
    response = api_client.post('/api/v1/users/change-password-request', request_body_for_requesting_reset_password)

    assert response.status_code == 200
    assert response.data.get('data').get('message') == ('The request to change the password '
                                                         'has been sent to the user email')

    _password_recovery_url = AuthPasswordServices.get_password_recovery_url(user)
    
    code, token = _password_recovery_url.removeprefix('changePassword?').split('&')

    code =  code.removeprefix('code=')
    token = token.removeprefix('token=')

    request_params = {
        'token': token,
        'code': code
    }

    request_body_reset_password = {
        'password': NEW_PASSWORD,
        'password_confirmation': NEW_PASSWORD
    }

    response = api_client.post('/api/v1/users/change-password', request_body_reset_password, query_params=request_params)
    
    user.refresh_from_db()

    assert response.status_code == 200
    assert response.data.get('data').get('message') == 'The password has been changed successfully'
    assert user.check_password(NEW_PASSWORD)






                               

    




