from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from core import constants

from ..serializers import FileListRequestBodySerializer
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
        )

        return Response(result, status=status.HTTP_201_CREATED)
