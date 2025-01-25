from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from core.exceptions import MissingRequiredFieldsException, InvalidQueryParamsException, InvalidParameterException
from core.serializers.responses import SuccessResponseSerializers
from users.services.password_management import PasswordManagementService

class PasswordManagementViewSet(viewsets.ViewSet):

    service_class = PasswordManagementService

    @action(
        detail=False,
        methods=['post'],
        url_path='change-password-request',
        throttle_classes=[AnonRateThrottle]
    )
    def change_password_request(self, request: Request) -> Response:

        email = request.data.get('email')
        if email is None:
            raise MissingRequiredFieldsException('Email is required')
        
        _service = self.service_class()
        _service.change_password_request(email)

        default_response = {
            'message': 'The request to change the password has been sent to the user email',
        }

        response = SuccessResponseSerializers({'data': default_response}).data

        return Response(response, status=status.HTTP_200_OK,) 
    

    @action(
        detail=False,
        methods=['post'],
        url_path='change-password',
        throttle_classes=[AnonRateThrottle]
    )
    def update_password_by_request(self, request: Request) -> Response:
        
        token = request.query_params.get('token')
        code = request.query_params.get('code')

        if token is None or code is None:
            raise InvalidQueryParamsException('Invalid query params: token and code are required')

        password_data = request.data
        if password_data.get('password') != password_data.get('password_confirmation'):
            raise InvalidParameterException('The password and password confirmation must be the same')
        
        new_password = password_data.get('password')

        _service = self.service_class()

        _service.update_password_by_request(
            token=token, 
            code=code,
            new_password=new_password,
        )
        
        data_for_responding = {'message': 'The password has been changed successfully'}

        response = SuccessResponseSerializers({'data': data_for_responding}).data

        return Response(response, status=status.HTTP_200_OK,)


        

