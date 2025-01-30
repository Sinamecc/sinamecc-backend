from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from core.exceptions import InvalidQueryParamsException
from core.serializers.responses import SuccessResponseSerializers
from users.services.resources import UserResourcesService
from users.serializers import UserSerializer


class UserResourcesViewSet(viewsets.ViewSet):

    lookup_value_converter = 'int'
    service_class = UserResourcesService

    def list(self, request: Request) -> Response:

        offset = request.query_params.get('offset', '0')
        limit = request.query_params.get('limit', '10')

        if not (offset.isdigit() and limit.isdigit()):
            raise InvalidQueryParamsException(detail='Invalid query params: offset and limit must be integers')

        _service = self.service_class()

        users = _service.get_all(
                    int(offset),
                    int(limit)
                )
        
        serialized_users = UserSerializer(users, many=True).data

        response = SuccessResponseSerializers({'data': serialized_users}).data

        return Response(response, status=status.HTTP_200_OK,)

    def create(self, request: Request) -> Response:
        
        _service = self.service_class()

        user = _service.create(request.data)

        serialized_user = UserSerializer(user).data

        response = SuccessResponseSerializers({'data': serialized_user}).data

        return Response(response, status=status.HTTP_201_CREATED,)


    def retrieve(self, request: Request, pk: int) -> Response:

        _service = self.service_class()

        user = _service.get_by_id(pk)

        serialized_user = UserSerializer(user).data
        
        response = SuccessResponseSerializers({'data': serialized_user}).data

        return Response(response, status=status.HTTP_200_OK,)

    def update(self, request: Request, pk: int) -> Response:
        
        _service = self.service_class()

        user = _service.update(pk, request.data)

        serialized_user = UserSerializer(user).data

        response = SuccessResponseSerializers({'data': serialized_user}).data

        return Response(response, status=status.HTTP_200_OK,)

    def destroy(self, request: Request, pk: int) -> Response:
        
        _service = self.service_class()

        serialized_deleted_user = _service.delete(pk)

        response = SuccessResponseSerializers({'data': serialized_deleted_user}).data

        return Response(response, status=status.HTTP_200_OK,)
    
    @action(detail=False, methods=['get'], url_path='me')
    def get_me(self, request: Request) -> Response:

        _service = self.service_class()

        user = _service.get_by_id(request.user.id)

        serialized_user = UserSerializer(user).data

        response = SuccessResponseSerializers({'data': serialized_user}).data

        return Response(response, status=status.HTTP_200_OK,)
    

    @get_me.mapping.put
    def update_me(self, request: Request) -> Response:
        
        _service = self.service_class()

        user = _service.update(request.user.id, request.data)

        serialized_user = UserSerializer(user).data

        response = SuccessResponseSerializers({'data': serialized_user}).data

        return Response(response, status=status.HTTP_200_OK,)