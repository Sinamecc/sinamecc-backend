from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from core.exceptions import InvalidQueryParamsException
from core.serializers.responses import SuccessResponseSerializers
from users._services.resources import UserResourcesService


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

        response = SuccessResponseSerializers({'data': users}).data

        return Response(response, status=status.HTTP_200_OK,)

    def create(self, request: Request) -> Response:
        
        _service = self.service_class()

        user = _service.create(request.data)

        response = SuccessResponseSerializers({'data': user}).data

        return Response(response, status=status.HTTP_201_CREATED,)


    def retrieve(self, request: Request, pk: int) -> Response:

        _service = self.service_class()

        user = _service.get_by_id(pk)
        
        response = SuccessResponseSerializers({'data': user}).data

        return Response(response, status=status.HTTP_200_OK,)

    def update(self, request: Request, pk: int) -> Response:
        
        _service = self.service_class()

        user = _service.update(pk, request.data)

        response = SuccessResponseSerializers({'data': user}).data

        return Response(response, status=status.HTTP_200_OK,)

    def destroy(self, request: Request, pk: int) -> Response:
        
        _service = self.service_class()

        user = _service.delete(pk)

        response = SuccessResponseSerializers({'data': user}).data

        return Response(response, status=status.HTTP_200_OK,)
    
