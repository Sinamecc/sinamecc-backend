from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidQueryParamsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid query params'
    default_code = 'invalid_query_params'