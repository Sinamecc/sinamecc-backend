from mitigation_action.ingei.models import HarmonizationIngei, HarmonizationIngeiFile
from mitigation_action.models import Mitigation
from mitigation_action.ingei.serializers import HarmonizationIngeiSerializer, HarmonizationIngeiFileSerializer, HarmonizationSerializerView
from general.storages import S3Storage
from io import BytesIO
import datetime
import os

import pdb

class HarmonizationIngeiService():
    def __init__(self):
        self.storage = S3Storage()
        self.HARMONIZATION_INGE_DOES_NOT_EXIST = "Harmonization Ingei does not exist."
        self.CANT_UPLOAD = "Can't upload Harmonization Ingei file"

    def get_one_harmonization_ingei_file(self,id):
        pdb.set_trace()
        return HarmonizationIngeiFile.objects.get(pk=id)

    def get_harmonization_ingei_file(self,id):
        pdb.set_trace()
        try:
            serialized_harmonization_ingei_file = HarmonizationIngeiSerializer(self.get_one_harmonization_ingei_file(id))
            result = (True, serialized_harmonization_ingei_file.data)

        except HarmonizationIngeiFile.DoesNotExist:
            result = (False, {"error": self.HARMONIZATION_INGE_DOES_NOT_EXIST})
        return result

    def _get_serialized_harmonization_ingei(self, request):
        data = {
            'name': request.data.get('name'),
            'user': request.user.id,
        }
        serializer = HarmonizationIngeiSerializer(data=data)
        return serializer

    def _get_serialized_harmonization_ingei_file(self, request, harmonization_ingei):
        data = {
            'user': request.user.id,
            'mitigation_action':request.data.get('mitigation'),
            'file': request.data.get('file'),
            'harmonization_ingei': harmonization_ingei.id,
        }
        serializer = HarmonizationIngeiFileSerializer(data=data)
        return serializer

    def serialize_and_save_files(self, request, harmonization):
        serialized_file = self._get_serialized_harmonization_ingei_file(request,harmonization)
        if serialized_file.is_valid():
            serialized_file.save()

    def create(self, request):
        serialized_harmonization_ingei = self._get_serialized_harmonization_ingei(request)
        if serialized_harmonization_ingei.is_valid():
            harmonization_ingei_file = serialized_harmonization_ingei.save()
            if harmonization_ingei_file.id:
                self.serialize_and_save_files(request,harmonization_ingei_file)
            return (True, HarmonizationIngeiSerializer(harmonization_ingei_file).data)
        return (False, {"error": self.CANT_UPLOAD})

    def get_one(self, pk):
        return HarmonizationIngei.objects.get(pk=pk)

    def get(self, id):
        try:
            serialized_harmonization = HarmonizationSerializerView(self.get_one(id))
            result = (True, serialized_harmonization.data)

        except HarmonizationIngei.DoesNotExist:
            result = (False, {"error": self.HARMONIZATION_INGE_DOES_NOT_EXIST})
        return result

    def get_file_content(self, harmonization_id, harmonization_file_id):
        harmonization_file = HarmonizationIngeiFile.objects.get(pk=harmonization_file_id)
        path, filename = os.path.split(harmonization_file.file.name)
        return (filename, BytesIO(self.storage.get_file(harmonization_file.file.name)),)

    def download_file(self, harmonization_id, harmonization_file_id):
        return self.get_file_content(harmonization_id,harmonization_file_id)
