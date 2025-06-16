from typing import Any, TypedDict

from ..constants import MitigationActionFilesType as FileType
from ..exceptions import MitigationActionNotFound
from ..models import MitigationAction
from ..models import MitigationActionFileStorage as FileStorageModel
from ..serializers import MitigationActionFileStorageSerializer


class FileUploadResult(TypedDict):
    number_of_files: int
    mitigation_action_id: str
class FileDeleteResult(TypedDict):
    number_of_files: int
    mitigation_action_id: str
class FilesService:
    def __init__(self) -> None:
        pass


    def get_files(
        self,
        mitigation_action_id: str,
        user_id: str,
    ) -> list[FileStorageModel]:
        ma_object = MitigationAction.objects.filter(id=mitigation_action_id, user=user_id).first()

        if not ma_object:
            raise MitigationActionNotFound(detail='You don\'t have permission to access this mitigation action')

        files = FileStorageModel.objects.filter(mitigation_action=ma_object)

        return list(files)
    
    def upload_files(
        self,
        mitigation_action_id: str,
        user_id: str,
        file_type: FileType,
        files: list[bytes],
    ) -> FileUploadResult:
        
        ma_object = MitigationAction.objects.filter(id=mitigation_action_id, user=user_id,).first()

        if not ma_object:
            raise MitigationActionNotFound(detail='You don\'t have permission to update this mitigation action')
        
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

        result = FileUploadResult(number_of_files=len(objects), mitigation_action_id=ma_object.id)

        return result

    def delete_files(
        self,
        mitigation_action_id: str,
        user_id: str,
        file_ids: list[str],
    ) -> FileUploadResult:
        
        ## NOTE: We need to manage permissions in different ways depending on the context.
        ma_object = MitigationAction.objects.filter(id=mitigation_action_id, user=user_id).first()

        if not ma_object:
            raise MitigationActionNotFound(detail='You don\'t have permission to delete files from this mitigation action')

        number_of_files, _ = FileStorageModel.objects.filter(id__in=file_ids, mitigation_action=ma_object).delete()

        return FileDeleteResult(
            number_of_files=number_of_files,
            mitigation_action_id=ma_object.id
        )