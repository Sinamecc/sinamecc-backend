from typing import TypedDict

from django.contrib.contenttypes.models import ContentType

from ..constants import MitigationActionFilesType as FileType
from ..exceptions import MitigationActionNotFound
from ..models import GenericFileStorage as FileStorageModel
from ..models import (
    Indicator,
    MitigationAction,
    MonitoringIndicator,
    MonitoringInformation,
    MonitoringReportingIndicator,
)


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
        type_file: FileType | None,
        object_id: str | None,
        user_id: str,
    ) -> list[FileStorageModel]:
        ma_object = (
            MitigationAction.objects.filter(
                id=mitigation_action_id,
                user=user_id,
            )
            .prefetch_related("files")
            .first()
        )

        if not ma_object:
            raise MitigationActionNotFound(
                detail="You don't have permission to access this mitigation action"
            )



        ModelClass = FileType.get_models().get(type_file)
        if not ModelClass and not object_id:
            return list(ma_object.files.all())


        elif ModelClass == MitigationAction:
            return list(ma_object.files.all())

        elif ModelClass == Indicator:
            indicator = (
                Indicator.objects.filter(
                    id=object_id,
                    monitoring_information=ma_object.monitoring_information,
                )
                .prefetch_related("files")
                .first()
            )
            if not indicator:
                raise MitigationActionNotFound(
                    detail="You don't have permission to access this Indicator"
                )
            return list(indicator.files.all())
        elif ModelClass == MonitoringIndicator:
            monitoring_indicator = monitoring_indicator = (
                MonitoringIndicator.objects.filter(
                    id=object_id,
                    monitoring_reporting_indicator=ma_object.monitoring_reporting_indicator,
                )
                .prefetch_related("files")
                .first()
            )
            if not monitoring_indicator:
                raise MitigationActionNotFound(
                    detail="You don't have permission to access this Monitoring Indicator"
                )
            return list(monitoring_indicator.files.all())
        else:
            raise ValueError(f"Unsupported file type: {type_file}")

    def upload_files(
        self,
        mitigation_action_id: str,
        user_id: str,
        file_type: FileType,
        files: list[bytes],
        object_id: str | None = None,
    ) -> FileUploadResult:
        ma_object = MitigationAction.objects.filter(
            id=mitigation_action_id,
            user=user_id,
        ).first()

        if not ma_object:
            raise MitigationActionNotFound(
                detail="You don't have permission to update this mitigation action"
            )
        
        ModelClass = FileType.get_models().get(file_type)()
        if not ModelClass:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        if ModelClass == MitigationAction:
            object_id = ma_object.id


        # If the object_id is provided, we need to check if the user has permission to access it.
        elif ModelClass == Indicator:
            indicator = (
                Indicator.objects.filter(
                    id=object_id,
                    monitoring_information=ma_object.monitoring_information,
                )
                .exists()
            )
            if not indicator:
                raise MitigationActionNotFound(
                    detail="You don't have permission to access this Indicator"
                )
        elif ModelClass == MonitoringIndicator:
            monitoring_indicator = (
                MonitoringIndicator.objects.filter(
                    id=object_id,
                    monitoring_reporting_indicator=ma_object.monitoring_reporting_indicator,
                )
                .exists()
            )
            if not monitoring_indicator:
                raise MitigationActionNotFound(
                    detail="You don't have permission to access this Monitoring Indicator"
                )
            
        ## for associating files with the right model, we need to get the content type
        content_type = ContentType.objects.get_for_model(ModelClass)
        objects = FileStorageModel.objects.bulk_create(
            [
                FileStorageModel(
                    file=file,
                    type=file_type,
                    metadata={
                        "filename": file.name,
                        "size": file.size,
                        "content_type": file.content_type,
                    },
                    mitigation_action=ma_object,
                    content_type=content_type,
                    object_id=object_id,
                )
                for file in files
            ]
        )

        result = FileUploadResult(
            number_of_files=len(objects), mitigation_action_id=ma_object.id
        )

        return result

    def delete_files(
        self,
        mitigation_action_id: str,
        user_id: str,
        file_ids: list[str],
    ) -> FileUploadResult:
        ## NOTE: We need to manage permissions in different ways depending on the context.
        ma_object = MitigationAction.objects.filter(
            id=mitigation_action_id, user=user_id
        ).first()

        if not ma_object:
            raise MitigationActionNotFound(
                detail="You don't have permission to delete files from this mitigation action"
            )

        number_of_files, _ = FileStorageModel.objects.filter(
            id__in=file_ids, mitigation_action=ma_object
        ).delete()

        return FileDeleteResult(
            number_of_files=number_of_files, mitigation_action_id=ma_object.id
        )
