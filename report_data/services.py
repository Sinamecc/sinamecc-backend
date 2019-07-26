from general.storages import S3Storage
from report_data.models import ReportFile, ReportFileVersion
from report_data.serializers import ReportFileSerializer, ReportFileVersionSerializer,ReportFileMetadataSerializer
from django.urls import reverse
import datetime
import os
import json
from io import BytesIO

# TODO: Add exception handling
class ReportFileService():
    def __init__(self):
        self.storage = S3Storage()
        self.REPORT_FILE_DOES_NOT_EXIST = "Report File does not exist."
        self.REPORT_FILE_EMPTY_METADATA = "Report file does not have metadata."
        self.REPORT_FILE_METADATA_EMPTY_FIELD = "Metadata does have an empty field."

    def _get_one(self, id):
        return ReportFile.objects.get(pk=id)

    def _get_serialized_report_file(self, request):
        data = {
            'name': request.data.get('name'),
            'user': request.user.id,
        }
        serializer = ReportFileSerializer(data=data)
        return serializer

    def _get_serialized_report_file_version(self, request, report_file):
        version_str_format = 'report_data_%Y%m%d_%H%M%S'
        version_str = datetime.datetime.now().strftime(version_str_format)
        data = {
            'active': True,
            'version': version_str,
            'file': request.data.get('file'),
            'report_file': report_file.id,
            'user': request.user.id,
        }
        serializer = ReportFileVersionSerializer(data=data)
        return serializer

    def _serialize_and_save_files(self, request, report_file_id):
        pass

    def _get_serialized_report_files_metadata(self, data, report_file):
        data = {
            'name':data.get('name'),
            'value':data.get('value'),
            'report_file': report_file.id,
        }

        serializer = ReportFileMetadataSerializer(data=data)
        return serializer

    def _save_metadata(self,request,report_file):
        
        result = (True, report_file)
        if request.data.get('metadata'):
            try:
                metadataList = json.loads(request.data.get('metadata'))
                for metadata in metadataList:
                    meta_serializer = self._get_serialized_report_files_metadata(metadata, report_file)

                    if meta_serializer.is_valid():
                        meta_serializer.save()

                    else:
                        result = (False, self.REPORT_FILE_METADATA_EMPTY_FIELD)

            except Exception as exp:
                result = (False, exp)
                    
        return result


    def create(self, request):
        serialized_report_file = self._get_serialized_report_file(request)
        if serialized_report_file.is_valid():

            report_file = serialized_report_file.save()
            metadata_status , metadata_details=self._save_metadata(request,report_file)

            if not metadata_status :
                return (False, metadata_details)

            version_serializer = self._get_serialized_report_file_version(request, report_file)
            if version_serializer.is_valid():
                
                version = version_serializer.save()
                report_file.reportfileversion_set.add(version)
                return (True, ReportFileSerializer(report_file).data)

        return (False, {"error": serialized_report_file.errors})

    def get(self, id):
        try:
            serialized_report_file = ReportFileSerializer(self._get_one(id))
            result = (True, serialized_report_file.data)
        except ReportFile.DoesNotExist:
            result = (False, {"error": "Report file doesnt exists"})
        return result
    
    def delete(self, id):
        try:
            rp = ReportFile.objects.get(id=id)
            rp.delete()
            result = (True, {"Result":"ReportFile has been delete"})
        except:
            result = (False, {"Result":"ReportFile has not been delete"})
        return result

    def get_all(self):
        # TODO: improve versions management
        try:
            report_file_list = [
                {
                    'id': r.id,
                    'user': r.user.id,
                    'name': r.name,
                    'created': r.created,
                    'updated': r.updated,
                    'last_active_version': r.reportfileversion_set.filter(active=True).first().version if r.reportfileversion_set.all().count() else "---",
                    'versions': r.reportfileversion_set.all().count()
                } for r in ReportFile.objects.all()
            ]
            result = (True, report_file_list)
        except ReportFile.DoesNotExist:
            result = (False, None)
        return result

    def update(self, id, request):
        try:
            report_file_status, report_file_data = self.get(id)
            if report_file_status:
                report_file = self._get_one(report_file_data.get('id'))
                version_str_format = 'report_data_%Y%m%d_%H%M%S'
                version_str = datetime.datetime.now().strftime(version_str_format)
                data = {
                    'name': request.data.get('name'),
                    'user': request.user.id,
                }
                serializer = ReportFileSerializer(report_file, data=data)
                previous_version = report_file.reportfileversion_set.filter(active=True).first()
                previous_version_serializer = ReportFileVersionSerializer(previous_version, data={'active': False},
                                                                          partial=True)
                if serializer.is_valid() and previous_version_serializer.is_valid():
                    previous_version_serializer.save()
                    saved_report_file = serializer.save()
                    version_data = {
                        'active': True,
                        'version': version_str,
                        'file': request.data.get('file'),
                        'report_file': saved_report_file.id,
                        'user': request.user.id,
                    }
                    version_serializer = ReportFileVersionSerializer(data=version_data)
                    if version_serializer.is_valid():
                        version = version_serializer.save()
                        saved_report_file.reportfileversion_set.add(version)
                        result = (True, ReportFileSerializer(saved_report_file).data)
                    else:
                        result = (False, {"error": "Error saving report file or changing previous file version"})
                else:
                    result = (False, {"error": "Error saving report file or changing previous file version"})
            else:
                result = (False, self.REPORT_FILE_DOES_NOT_EXIST)
        except ReportFile.DoesNotExist:
            result = (False, {"errors": [serializer.errors, previous_version_serializer.errors]})
        return result

    def get_all_file_versions(self, report_file_id):
        report = self._get_one(report_file_id)

        versions_array = [
            {
                'version': v.version,
                'file': self._get_file_path(report.id, v.id)
            } for v in report.reportfileversion_set.all()
        ]
        content = {
            'name': report.name,
            'versions': versions_array
        }
        return content

    def _get_file_path(self, report_file_id, report_file_version_id):
        url = reverse("get_report_file_version_url",
                      kwargs={'report_file_id': report_file_id, 'report_file_version_id': report_file_version_id})
        return url

    # TODO: handle errors
    def get_file_content(self, report_file_id, report_file_version_id):
        report_file_version = ReportFileVersion.objects.get(pk=report_file_version_id)
        path, filename = os.path.split(report_file_version.file.name)
        return (filename, BytesIO(self.storage.get_file(report_file_version.file.name)), )

    def download_file(self, report_file_id, report_file_version_id):
        return self.get_file_content(report_file_id, report_file_version_id)