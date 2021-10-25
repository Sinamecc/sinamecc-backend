from general.storages import S3Storage
from report_data.models import ReportFile
from django.urls import reverse
from general.helpers.services import ServiceHelper
from general.helpers.serializer import SerializersHelper
from report_data.serializers import ReportDataSerializer
import datetime
import os
import json
from io import BytesIO

# TODO: Add exception handling
class ReportFileService():
    def __init__(self):
        self._service_helper = ServiceHelper()
        self._serializer_helper = SerializersHelper()


    def _get_serialized_report_data(self,  data, report_data=None, partial=None):

        serializer = self._serialize_helper.get_serialized_record(ReportDataSerializer, data, record=report_data, partial=partial)

        return serializer

    def get(self, request, report_data_id):
        ...
    
    def get_all(self, request):
        ...


    def create(self, request, data):
        ...
    

    def update(self, request, data):
        ...


    def upload_file(self, request, report_data_id):
        ...

    


  