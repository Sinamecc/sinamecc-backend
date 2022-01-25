from functools import partial
from unittest import result
from general.storages import S3Storage
from mitigation_action.models import Classifier, ThematicCategorizationType
from report_data import serializers
from report_data.models import ReportData, ReportFile
from django.urls import reverse
from general.helpers.services import ServiceHelper
from general.helpers.serializer import SerializersHelper
from report_data.serializers import ReportDataSerializer, ReportDataChangeLogSerializer, ReportFileSerializer
from mitigation_action.serializers import ClassifierSerializer, ContactSerializer, ThematicCategorizationTypeSerializer
import datetime
import os
import json
from io import BytesIO

# TODO: Add exception handling
class ReportDataService():
    def __init__(self):
        self._service_helper = ServiceHelper(self)
        self._serializer_helper = SerializersHelper()
        self._storage = S3Storage()
        self.FUNCTION_INSTANCE_ERROR = 'Error Mitigation Action Service does not have {0} function'
        self.ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'


    def _get_serialized_report_data(self,  data, report_data=None, partial=None):

        serializer = self._serializer_helper.get_serialized_record(ReportDataSerializer, data, record=report_data, partial=partial)

        return serializer
    

    def _get_serialized_report_data_change_log(self, data, report_data_change_log=None, partial=None):

        serializer = self._serializer_helper.get_serialized_record(ReportDataChangeLogSerializer, data, record=report_data_change_log, partial=partial)

        return serializer


    def _get_serialized_contact(self,  data, contact=None, partial=None):
        
        serializer = self._serializer_helper.get_serialized_record(ContactSerializer, data, record=contact, partial=partial)

        return serializer


    def _get_report_data_change_log_data(self, data, user):

        data = {
            'author': user.id,
            'changes': data.get('changes', None),
            'change_description': data.get('change_description', None),
        }

        return data
    
    def _get_report_file_data(self, data, file):
        
        data = {
            'file': file,
            'report_data': data.get('report_data', None),
            'report_type': data.get('report_type', None),
        }

        return data


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


    def _create_update_report_data_change_log(self, data, report_data_change_log=None):
            
        if report_data_change_log:
            serialized_report_data_change_log = self._get_serialized_report_data_change_log(data, report_data_change_log)

        else:
            serialized_report_data_change_log = self._get_serialized_report_data_change_log(data)
        
        if serialized_report_data_change_log.is_valid():
            report_data_change_log = serialized_report_data_change_log.save()
            result = (True, report_data_change_log)

        else:
            result = (False, serialized_report_data_change_log.errors)

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
        data['report_data_change_log'] = self._get_report_data_change_log_data(data.get('report_data_change_log', {}), request.user)
        field_list = ['contact']

        validation_dict = self._service_helper.create_or_update_record(field_list, data)

        if all(validation_dict):
            serialized_report_data_change_log = self._get_serialized_report_data_change_log(data.pop('report_data_change_log'), partial=True)
            serialized_report_data = self._get_serialized_report_data(data, partial=True)

            if serialized_report_data.is_valid() and serialized_report_data_change_log.is_valid():
                report_data = serialized_report_data.save()
                report_data_change_log = serialized_report_data_change_log.save()
                report_data.report_data_change_log.add(report_data_change_log)
                result = (True, ReportDataSerializer(report_data).data)
  
            else:
                errors.append(serialized_report_data.errors.extend(serialized_report_data_change_log.errors))
                result = (False, errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result
    

    def update(self, request, report_data_id):

        validation_dict, errors = {}, []
        data = request.data.copy()
        data['user'] = request.user.id
        data['report_data_change_log'] = self._get_report_data_change_log_data(data.get('report_data_change_log', {}), request.user)

        field_list = ['contact']
        report_data_status, report_data_details = self._service_helper.get_one(ReportData, report_data_id)

        if report_data_status:
            validation_dict = self._service_helper.create_or_update_record(field_list, data, report_data_details)

            if all(validation_dict):
                serialized_report_data_change_log = self._get_serialized_report_data_change_log(data.pop('report_data_change_log'), partial=True)
                serialized_report_data = self._get_serialized_report_data(data, report_data=report_data_details, partial=True)

                if serialized_report_data.is_valid() and serialized_report_data_change_log.is_valid():
                    report_data = serialized_report_data.save()
                    report_data_change_log = serialized_report_data_change_log.save()
                    report_data.report_data_change_log.add(report_data_change_log)
                    
                    result = (True, ReportDataSerializer(report_data).data)
    
                else:
                    errors.append(serialized_report_data.errors)
                    result = (False, errors)

            else:
                result = (False, validation_dict.get(False))

        else:
            result = (False, report_data_details)
            
        return result
        


    def upload_source_file(self, data, report_data, type=None):
        
        serialized_report_data = ReportDataSerializer(report_data, data={'source_file': data}, partial=True)
        
        if serialized_report_data.is_valid():
            saved_report_data = serialized_report_data.save()
            result = (True, ReportDataSerializer(saved_report_data).data)
            
        else:
            result = (False, serialized_report_data.errors)
            
        return result


    
    def upload_report_file(self, file, report_data, type=None):
        data = {'report_data': report_data.id, 'report_type': type}
        data = self._get_report_file_data(data, file)
        report_file = report_data.report_file.filter(report_type=type).first()
        serialized_report_file = ReportFileSerializer(report_file, data=data, partial=True)
        
        if serialized_report_file.is_valid():
            saved_report_file = serialized_report_file.save()
            result = (True, ReportFileSerializer(saved_report_file).data)
            
        else:
            result = (False, serialized_report_file.errors)
            
        return result
        

    ## upload files in the models
    def upload_file_to(self, request, report_data_id):

        files_type = {
            'source_file': self.upload_source_file,
            'report_file': self.upload_report_file,
            'base_line_report': self.upload_report_file
        }
        
        data = request.data
        
        report_status, report_data = self._service_helper.get_one(ReportData, report_data_id)
        
        status_upload_files = {}
        if report_status:
            
            for k, v in data.items():
                
                if k in files_type:
                    result_status, result_data = files_type.get(k)(v, report_data, k)
                    status_upload_files.setdefault(result_status, []).append(result_data)
            
            if all(status_upload_files) and  status_upload_files:
                files_list = status_upload_files.get(True)
                result = (True, ReportDataSerializer(report_data).data)
            
            else:
                error_list = status_upload_files.get(False)
                result = (False, error_list)
            
            
        else:
            
            result = (report_status, report_data)
       
        
        return result
    
    
    
    def _get_content_file(self, path):

        path, filename = os.path.split(path)
        
        result = (filename, BytesIO(self._storage.get_file(path)))
        
        return result
    
    
    def download_report_file(self, request, report_file_id):
        
        report_file_status, report_file_data = self._service_helper.get_one(ReportFile, report_file_id)
        
        if report_file_status:
            
            s3_path = report_file_data.file.name
            
            path, filename = os.path.split(s3_path)
        
            file_content =  BytesIO(self._storage.get_file(s3_path))
            result = (True, (filename, file_content))
            
        else:
            result = (report_file_status, report_file_data)

        return result
    
    
    def download_source_file(self, request, report_data_id):
        
        report_data_status, report_data = self._service_helper.get_one(ReportData, report_data_id)
        
        if report_data_status:
            s3_path = report_data.source_file.name
            
            path, filename = os.path.split(s3_path)
        
            file_content =  BytesIO(self._storage.get_file(s3_path))
            
            result = (True, (filename, file_content))
            
        else:
            result = (report_data_status, report_data)

        return result
    
    
    def get_catalog_data(self, request):
    
        catalog = {
            'classifier': (Classifier, ClassifierSerializer),
            'thematic_categorization_type': (ThematicCategorizationType, ThematicCategorizationTypeSerializer),
        }
        data = {}
        for name , (_model, _serializer) in catalog.items():
            result_status, result_data = self._service_helper.get_all(_model)

            if not result_status:
                result = (False, result_data)
                return result
            
            data = {**data, **{name: _serializer(result_data, many=True).data}}
        
        result = (True, data)
        
        return result
    
    


  