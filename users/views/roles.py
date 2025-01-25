from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from core.exceptions import MissingRequiredFieldsException
from core.serializers.responses import SuccessResponseSerializers
from users.services.roles import UserRolesServices
from users.serializers import UserSerializer


class UserRolesViewSet(viewsets.ViewSet):
    
    look_up_value_converter = 'int'
    service_class = UserRolesServices

    @action(detail=False, methods=['get'], url_path='roles', url_name='get_roles')
    def get_roles(self, request: Request) -> Response:

        _service = self.service_class()

        roles = _service.get_registered_roles()

        response = SuccessResponseSerializers({'data': roles}).data

        return Response(response, status=status.HTTP_200_OK,)

    @action(detail=True, methods=['post'], url_path='roles', url_name='assign_role_to_user')
    def assign_role_to_user(self, request: Request, pk: int) -> Response:

        roles = request.data.get('roles')

        if roles is None or not isinstance(roles, list):
            raise MissingRequiredFieldsException('roles is required and must be a list')

        _service = self.service_class()

        user = _service.assign_role_to_user(user_id=pk, role_list=roles)

        serialized_user = UserSerializer(user).data

        response = SuccessResponseSerializers({'data': serialized_user}).data

        return Response(response, status=status.HTTP_200_OK,)