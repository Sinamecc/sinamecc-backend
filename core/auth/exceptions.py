from rest_framework.exceptions import  APIException


class RoleGenericException(APIException):
    status_code = 400
    default_detail = 'Role error'
    default_code = 'role_error'