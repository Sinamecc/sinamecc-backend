from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from core.exceptions import MissingRequiredFieldsException, InvalidQueryParamsException, InvalidParameterException
from core.serializers.responses import SuccessResponseSerializers
from users._services.password_management import PasswordManagementService

class PasswordManagementViewSet(viewsets.ViewSet):

    service_class = PasswordManagementService

    @action(
        detail=False,
        methods=['POST'],
        url_path='change-password-request',
        throttle_classes=[AnonRateThrottle]
    )
    def change_password_request(self, request: Request) -> Response:

        email = request.data.get('email')
        if email is None:
            raise MissingRequiredFieldsException('Email is required')
        
        _service = self.service_class()

        returned_data = _service.change_password_request(email)

        response = SuccessResponseSerializers({'data': returned_data}).data

        return Response(response, status=status.HTTP_200_OK,) 
    

    @action(
        detail=False,
        methods=['POST'],
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

        returned_data = _service.update_password_by_request(
                            token=token, 
                            code=code,
                            new_password=new_password,
                        )

        response = SuccessResponseSerializers({'data': returned_data}).data

        return Response(response, status=status.HTTP_200_OK,)


        

