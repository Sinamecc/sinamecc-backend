from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from core import constants

from ..serializers import (
    FileListRequestBodySerializer,
    GetFilesListRequestBodySerializer,
)
from ..serializers import (
    FileStorageSerializer as MitigationActionFileStorageSerializer,
)
from ..services.files import FilesService


class AttachmentViewSet(viewsets.ViewSet):
    lookup_value_regex = constants.UUID_REGEX
    _service_class = FilesService

    def create(self, request: Request, pk: str) -> Response:
        request_body = FileListRequestBodySerializer(data=request.data)
        request_body.is_valid(raise_exception=True)
        serialized_body = request_body.validated_data
        user_id = request.user.id
        service = self._service_class()
        result = service.upload_files(
            mitigation_action_id=pk,
            user_id=user_id,
            file_type=serialized_body.get('type'),
            files=serialized_body.get('files', []),
            object_id=serialized_body.get('entity_id', None),

        )

        return Response(result, status=status.HTTP_201_CREATED)
    
    ## We use this because is a workaround for the fact that the `ViewSet` 
    ## does not support `DELETE` method without `pk` in the URL.
    def delete(self, request: Request, pk: str) -> Response:
        file_ids = request.data.get('file_ids', [])
        user_id = request.user.id
        service = self._service_class()
        result = service.delete_files(
            mitigation_action_id=pk,
            user_id=user_id,
            file_ids=file_ids,
        )

        return Response(result, status=status.HTTP_200_OK)

    def list(self, request: Request, pk: str) -> Response:
        """
        This method lists the files. If no record ID and file type are provided,
        it returns all files associated with the mitigation action.

        Returns:
            Response: List of files associated with the mitigation action.
        """

        user_id = request.user.id
        query_params = GetFilesListRequestBodySerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)
        serialized_query_params = query_params.validated_data

        service = self._service_class()
        files = service.get_files(
            mitigation_action_id=pk,
            user_id=user_id,
            type_file=serialized_query_params.get('entity_type'),
            object_id= serialized_query_params.get('entity_id')
        )
        serialized_files = MitigationActionFileStorageSerializer(files, many=True).data
        return Response(serialized_files, status=status.HTTP_200_OK)
