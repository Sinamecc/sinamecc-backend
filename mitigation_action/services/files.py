from typing import Any, TypedDict

from ..constants import MitigationActionFilesType as FileType
from ..exceptions import MitigationActionNotFound
from ..models import MitigationAction
from ..models import MitigationActionFileStorage as FileStorageModel


class FileUploadResult(TypedDict):
    number_of_files: int
    mitigation_action_id: str


class FilesService:
    def __init__(self) -> None:
        pass

    def upload_files(
        self,
        mitigation_action_id: str,
        user_id: str,
        file_type: FileType,
        files: list[bytes],
    ) -> FileUploadResult:
        ma_object = MitigationAction.objects.filter(
            id=mitigation_action_id,
            user=user_id,
        ).first()

        if not ma_object:
            raise MitigationActionNotFound(
                detail='You don\'t have permission to update this mitigation action'
            )
        objects = FileStorageModel.objects.bulk_create(
            [
                FileStorageModel(
                    file=file,
                    type=file_type,
                    metadata={
                        'filename': file.name,
                        'size': file.size,
                        'content_type': file.content_type,
                    },
                    mitigation_action=ma_object,
                )
                for file in files
            ]
        )

        result = FileUploadResult(
            number_of_files=len(objects),
            mitigation_action_id=ma_object.id,
        )

        return result
