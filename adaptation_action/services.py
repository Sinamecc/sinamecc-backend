
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
        ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'
        pass


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
        print(adaptation_action_id)
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