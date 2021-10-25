from general.storages import S3Storage
from report_data.models import ReportData, ReportFile
from django.urls import reverse
from general.helpers.services import ServiceHelper
from general.helpers.serializer import SerializersHelper
from report_data.serializers import ReportDataSerializer
from mitigation_action.serializers import ContactSerializer
import datetime
import os
import json
from io import BytesIO

# TODO: Add exception handling
class ReportDataService():
    def __init__(self):
        self._service_helper = ServiceHelper(self)
        self._serializer_helper = SerializersHelper()
        self.FUNCTION_INSTANCE_ERROR = 'Error Mitigation Action Service does not have {0} function'
        self.ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'


    def _get_serialized_report_data(self,  data, report_data=None, partial=None):

        serializer = self._serializer_helper.get_serialized_record(ReportDataSerializer, data, record=report_data, partial=partial)

        return serializer


    def _get_serialized_contact(self,  data, contact=None, partial=None):
        
        serializer = self._serializer_helper.get_serialized_record(ContactSerializer, data, record=contact, partial=partial)

        return serializer


    def _create_update_contact(self, data, contact=None):
        
        if contact:
            serialized_contact = self._get_serialized_contact(data, contact)

        else:
            serialized_contact = self._get_serialized_contact(data)
        
        if serialized_contact.is_valid():
            contact = serialized_contact.save()
            result = (True, contact)

        else:
            result = (False, serialized_contact.errors)

        return result


    def get(self, request, report_data_id):
        
        report_data_status, report_data_details = self._service_helper.get_one(ReportData, report_data_id)

        if report_data_status:
            result = (True, ReportDataSerializer(report_data_details).data)
        else:
            result = (False, report_data_details)

        return result

    
    def get_all(self, request):
        
        report_data_status, report_data_details = self._service_helper.get_all(ReportData)

        if report_data_status:
            result = (True, ReportDataSerializer(report_data_details, many=True).data)

        else:
            result = (False, report_data_details)

        return result


    def create(self, request):

        validation_dict, errors = {}, []
        data = request.data.copy()
        data['user'] = request.user.id

        field_list = ['contact']

        validation_dict = self._service_helper.create_or_update_record(field_list, data)

        if all(validation_dict):
            serialized_report_data = self._get_serialized_report_data(data, partial=True)

            if serialized_report_data.is_valid():
                report_data = serialized_report_data.save()
                result = (True, ReportDataSerializer(report_data).data)
  
            else:
                errors.append(serialized_report_data.errors)
                result = (False, errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result
    

    def update(self, request, report_data_id):

        validation_dict, errors = {}, []
        data = request.data.copy()
        data['user'] = request.user.id

        field_list = ['contact']
        report_data_status, report_data_details = self._service_helper.get_one(ReportData, report_data_id)

        if report_data_status:
            validation_dict = self._service_helper.create_or_update_record(field_list, data, report_data_details)

            if all(validation_dict):
                serialized_report_data = self._get_serialized_report_data(data, report_data=report_data_details, partial=True)

                if serialized_report_data.is_valid():
                    report_data = serialized_report_data.save()
                    result = (True, ReportDataSerializer(report_data).data)
    
                else:
                    errors.append(serialized_report_data.errors)
                    result = (False, errors)

            else:
                result = (False, validation_dict.get(False))

        else:
            result = (False, report_data_details)
            
        return result
        


    def upload_source_file(self, request, report_data_id):
        ...

    
    def upload_report_file_list(self, request, report_data_id):
        ...

        


  