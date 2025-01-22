from rest_framework.exceptions import APIException
from rest_framework import status


class UserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'User not found'
    default_code = 'user_not_found'