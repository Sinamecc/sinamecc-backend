from general.storages import S3Storage
from report_data.models import ReportData, ReportFile
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


    def create(self, request):

        data = request.data
        user = request.user
        data['user'] = user.id

        serialized_report_data = self._get_serialized_report_data(data, partial=True)

        if serialized_report_data.is_valid():
            report_data = serialized_report_data.save()
            result = (True, ReportDataSerializer(report_data).data)

        else:
            result = (False, serialized_report_data.errors)
        
        return result
    

    def update(self, request, report_data_id):
        data = request.data
        user = request.user

        report_data_status, report_data_details= self._service_helper.get_one(ReportData, report_data_id)

        if report_data_status:
            report_data = report_data_details
            serialized_report_data = self._get_serialized_report_data(data, report_data, partial=True)

            if serialized_report_data.is_valid():
                report_data = serialized_report_data.save()
                result = (True, ReportDataSerializer(report_data).data)

            else:
                result = (False, serialized_report_data.errors)
        
        else:
            result = (False, report_data_details)
        
        return result
        


    def upload_file(self, request, report_data_id):
        ...

    


  