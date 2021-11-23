
from os import error
from adaptation_action.models import ReportOrganization, AdaptationAction
from adaptation_action.serializers import *
from general.helpers.services import ServiceHelper
from general.helpers.serializer import SerializersHelper

class AdaptationActionServices():
    def __init__(self) -> None:

        self._service_helper = ServiceHelper()
        self._serializer_helper = SerializersHelper()
        self.FUNCTION_INSTANCE_ERROR = 'Error Adaptation Action Service does not have {0} function'
        self.ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'


    def _create_sub_record(self, data, sub_record_name):
        
        create_function = f'_create_update_{sub_record_name}'

        if hasattr(self, create_function):
            function = getattr(self, create_function)
            record_status, record_detail = function(data=data)
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(create_function))

        return result
    
    def _update_sub_record(self, sub_record_name, record_for_updating, data):
        
        update_function = f'_create_update_{sub_record_name}'
        
        if hasattr(self, update_function):
          
            function = getattr(self, update_function)
        
            record_status, record_detail = function(data, record_for_updating)
          
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(update_function))

        return result

    def _create_or_update_record(self, instance, field, data):

        result = (False, [])
        if hasattr(instance, field):
            if getattr(instance, field) == None:
                record_status, record_data = self._create_sub_record(data, field) ## field = sub_record_name

            else:
                ## change field(string) to object(model instance)
                record_for_updating = getattr(instance, field) 
                record_status, record_data = self._update_sub_record(field, record_for_updating, data)
            
            result = (record_status, record_data)
        else:

            result = (False, self.ATTRIBUTE_INSTANCE_ERROR)

        return result

    def _get_serialized_adaptation_action(self, data, adaptation_action = False):

        serializer = self._serializer_helper.get_serialized_record(AdaptationActionSerializer, data, record=adaptation_action)

        return serializer
    
    def _get_serialized_report_organization(self, data, report_organization = False):

        serializers = self._serializer_helper.get_serialized_record(ReportOrganizationSerializer, data, record=report_organization)

        return serializers

    def _get_serialized_progress_log(self, data, progress_log = False):

        serializers = self._serializer_helper.get_serialized_record(ProgressLogSerializer, data, record=progress_log)

        return serializers
    
    def _get_serialized_indicator_source(self, data, indicator_source = False):

        serializers = self._serializer_helper.get_serialized_record(IndicatorSourceSerializer, data, record=indicator_source)

        return serializers
    
    def _get_serialized_indicator_monitoring(self, data, indicator_monitoring = False):

        serializers = self._serializer_helper.get_serialized_record(IndicatorMonitoringSerializer, data, record=indicator_monitoring)

        return serializers
    
    def _get_serialized_general_report(self, data, general_report = False):

        serializers = self._serializer_helper.get_serialized_record(GeneralReportSerializer, data, record=general_report)

        return serializers
    
    def _get_serialized_action_impact(self, data, action_impact = False):

        serializers = self._serializer_helper.get_serialized_record(ActionImpactSerializer, data, record=action_impact)

        return serializers
    
    def _create_update_progress_log(self, data, progress_log=False):

        if progress_log:
            serialized_progress_log = self._get_serialized_progress_log(data, progress_log)
        
        else:
            serialized_progress_log = self._get_serialized_progress_log(data)
        
        if serialized_progress_log.is_valid():
            progress_log = serialized_progress_log.save()
            result = (True, progress_log)
        
        else:
            result = (False, serialized_progress_log.errors)

        return result
    
    def _create_update_indicator_monitoring(self, data, indicator_monitoring=False):

        if indicator_monitoring:
            serialized_indicator_monitoring = self._get_serialized_indicator_monitoring(data, indicator_monitoring)
        
        else:
            serialized_indicator_monitoring = self._get_serialized_indicator_monitoring(data)
        
        if serialized_indicator_monitoring.is_valid():
            indicator_monitoring = serialized_indicator_monitoring.save()
            result = (True, indicator_monitoring)
        
        else:
            result = (False, serialized_indicator_monitoring.errors)
        
        return result

    def _create_update_general_report(self, data, general_report=False):

        if general_report:
            serialized_general_report = self._get_serialized_general_report(data, general_report)
        
        else:
            serialized_general_report = self._get_serialized_general_report(data)
        
        if serialized_general_report.is_valid():
            general_report = serialized_general_report.save()
            result = (True, general_report)
        
        else:
            result = (False, serialized_general_report.errors)

        return result
    
    def _create_update_action_impact(self, data, action_impact=False):

        if action_impact:
            serialized_action_impact = self._get_serialized_action_impact(data, action_impact)
        
        else:
            serialized_action_impact = self._get_serialized_action_impact(data)
        
        if serialized_action_impact.is_valid():
            action_impact = serialized_action_impact.save()
            result = (True, action_impact)
        
        else:
            result = (False, serialized_action_impact.errors)

        return result

    def _create_update_report_organization(self, data, report_organization=False):

        if report_organization:
            serialized_report_organization = self._get_serialized_report_organization(data, report_organization)
        
        else:
            serialized_report_organization = self._get_serialized_report_organization(data)
        
        if serialized_report_organization.is_valid():
            report_organization = serialized_report_organization.save()
            result = (True, report_organization)
        
        else:
            result = (False, serialized_report_organization.errors)

        return result

    def get(self, request, adaptation_action_id):
        
        adaptation_action_status, adaptation_action_data = self._service_helper.get_one(AdaptationAction, adaptation_action_id)
        
        if adaptation_action_status:
            result = (adaptation_action_status, AdaptationActionSerializer(adaptation_action_data).data)
        
        else:
            result = (adaptation_action_status, adaptation_action_data) 

        return result
    
    def get_all(self, request):

        adaptation_action_status, adaptation_action_data = self._service_helper.get_all(AdaptationAction)

        if adaptation_action_status:
            result = (adaptation_action_status, AdaptationActionSerializer(adaptation_action_data, many=True).data)
        
        else:
            result = (adaptation_action_status, adaptation_action_data) 

        return result


    def create(self, request):

        errors =[]
        validation_dict = {}
        data = request.data.copy()
        data['user'] = request.user.id

        # fk's of object adaptation_action that have nested fields
        field_list = ['report_organization']

        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field)

                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)
        
        if all(validation_dict):
            serialized_adaptation_action = self._get_serialized_adaptation_action(data)
            if serialized_adaptation_action.is_valid():
                adaptation_action = serialized_adaptation_action.save()
                
                result = (True, AdaptationActionSerializer(adaptation_action).data)
  
            else:
                errors.append(serialized_adaptation_action.errors)
                result = (False, errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result
    
    def update(self, request, adaptation_action_id):

        validation_dict = {}
        data = request.data.copy()
        data['user'] = request.user.id

        field_list = ['report_organization']
        adaptation_action_status, adaptation_action_data = \
            self._service_helper.get_one(AdaptationAction, adaptation_action_id)
        
        if adaptation_action_status:
            adaptation_action = adaptation_action_data
             # fk's of object adaptation that have nested fields
            for field in field_list:
                if data.get(field, False):
                    record_status, record_data = self._create_or_update_record(adaptation_action, field, data.get(field))
                    
                    if record_status:
                        data[field] = record_data.id
                        
                    dict_data = record_data if isinstance(record_data, list) else [record_data]
                    validation_dict.setdefault(record_status,[]).extend(dict_data)

            if all(validation_dict):
                serialized_adaptation_action = self._get_serialized_adaptation_action(data, adaptation_action)
                
                if serialized_adaptation_action.is_valid():
                    adaptation_action = serialized_adaptation_action.save()
                    result = (True, AdaptationActionSerializer(adaptation_action).data)

                else:
                    result = (False, serialized_adaptation_action.errors)
            else:
                result = (False, validation_dict.get(False))
        else:
            result = (adaptation_action_status, adaptation_action_data)


        return result