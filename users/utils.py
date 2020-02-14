from datetime import datetime
from calendar import timegm
from users.services import UserService
import rest_framework_jwt.utils as utils

service = UserService()

def jwt_payload_handler(user):
    
    payload = utils.jwt_payload_handler(user)
    available_apps_status, available_apps_data = service.get_user_roles(user)
    if available_apps_status:
            payload['available_apps'] = available_apps_data

    return payload
        

def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'token': token,
        'user_id': user.id
    }
