from general.helpers.serializer import SerializersHelper
from general.helpers.services import ServiceHelper
from user_self_management.serializers import *
from user_self_management.models import *

class UserSelfManagementServices():
    def __init__(self):
        
        self._service_helper = ServiceHelper()
        self._serializer_helper = SerializersHelper()
        self.FUNCTION_INSTANCE_ERROR = 'Error User Self Management Service does not have {0} function'
    
    def _create_sub_record(self, data, sub_record_name):
        
        create_function = f'_create_update_{sub_record_name}'

        if hasattr(self, create_function):
            function = getattr(self, create_function)
            record_status, record_detail = function(data=data)
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(create_function))

        return result
    
    def _get_serialized_module(self, data, module = False):

        serializer = self._serializer_helper.get_serialized_record(ModuleSerializer, data, record=module)

        return serializer

    def _create_update_module(self, data, module = False):

        if module:
            serialized_module = self._get_serialized_module(data, module)
        
        else:
            serialized_module = self._get_serialized_module(data)

        if serialized_module.is_valid():
            module = serialized_module.save()
            result = (True, module)

        else:
            result = (False, serialized_module.errors)
        
        return result

    def _get_serialized_user_self_management(self, data, user_self_management = False):

        serializer = self._serializer_helper.get_serialized_record(UserSerializer, data, record=user_self_management)

        return serializer


    def get_all(self, request):

        user_self_management_status, user_self_management_data = self._service_helper.get_all(User)

        if user_self_management_status:
            result = (user_self_management_status, UserSerializer(user_self_management_data, many=True).data)
        
        else:
            result = (user_self_management_status, user_self_management_data) 

        return result


    def create(self, request):

        errors =[]
        validation_dict = {}
        data = request.data.copy()
        data['user'] = request.user.id

        # fk's of object user_self_management that have nested fields
        field_list = []

        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field)
                
                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)
        
        if all(validation_dict):
            serialized_user_self_management = self._get_serialized_user_self_management(data)
            if serialized_user_self_management.is_valid():
                user_self_management = serialized_user_self_management.save()
                
                result = (True, UserSerializer(user_self_management).data)
  
            else:
                errors.append(serialized_user_self_management.errors)
                result = (False, errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result