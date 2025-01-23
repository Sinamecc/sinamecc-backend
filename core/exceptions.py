from rest_framework.exceptions import APIException
from rest_framework import status

## raise for query params
class InvalidQueryParamsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid query params'
    default_code = 'invalid_query_params'

## raise for missing required fields in the request body
class MissingRequiredFieldsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Missing required fields'
    default_code = 'missing_required_fields'


## This class is to used when the parameter is invalid (generally used in the service layer validation)
class InvalidParameterException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid parameter'
    default_code = 'invalid_parameter'