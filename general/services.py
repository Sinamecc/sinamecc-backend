import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from general.helpers.services import ServiceHelper
from general.helpers.serializer import SerializersHelper
from general.serializers import ProvinceSerializer, CantonSerializer, DistrictSerializer
from general.models import Province, Canton, District
import json

class EmailServices():

    def __init__(self, sender = "sinamec@grupoincocr.com", base_dir_notification =  settings.FRONTEND_URL):
        self.sender = sender
        self.base_dir_notification = base_dir_notification
        self.AWS_REGION = "us-east-1"
        self.CHARSET = "UTF-8"

    def send_notification(self, recipient_list, subject, message_body):
        
        client = boto3.client('ses', region_name = self.AWS_REGION)
        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': recipient_list
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.CHARSET,
                            'Data': message_body,
                        },
                        'Text': {
                            'Charset': self.CHARSET,
                            'Data': message_body,
                        },
                    },
                    'Subject': {
                        'Charset': self.CHARSET,
                        'Data': subject,
                    },
                },
                Source=self.sender,
                
            )

        except ClientError as e:

            return (False, e.response['Error']['Message'])

        else:

            return (True, f"Email sent from {self.sender} to {' '.join(recipient_list)}")

    def send_status_notification(self, recipient_list, subject, message_body):

        recipient_list = recipient_list if isinstance(recipient_list , list) else [recipient_list]

        result = self.send_notification(recipient_list, subject, message_body)

        return result
    

        

class HandlerErrors():

    def error_400(self, errors):
        result_error = {"error_code": 400, "error_message": errors}
        return (False, result_error)


class GeneralService():

    def __init__(self):
        self._service_helper = ServiceHelper()
        self._serializer_helper = SerializersHelper()
        self.FUNCTION_INSTANCE_ERROR = 'Error General Service does not have {0} function'
        self.ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'
        self.INVALID_STATUS_TRANSITION = "Invalid adaptation action state transition."
        self.STATE_HAS_NO_AVAILABLE_TRANSITIONS = "State has no available transitions."
    
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
    
    def _get_serialized_province(self, data, province = False):

        serializer = self._serializer_helper.get_serialized_record(ProvinceSerializer, data, record=province)

        return serializer
    
    def get_province(self, request, province_id):
        
        province_status, province_data = self._service_helper.get_one(Province, province_id)
        
        if province_status:
            result = (province_status, ProvinceSerializer(province_data).data)
        
        else:
            result = (province_status, province_data) 

        return result
    
    def get_all(self, request=None):

        province_status, province_data = self._service_helper.get_all(Province)

        if province_status:
            result = (province_status, ProvinceSerializer(province_data, many=True).data)
        
        else:
            result = (province_status, province_data) 

        return result
    
    def get_all_canton(self, request=None):

        canton_status, canton_data = self._service_helper.get_all(Canton)

        if canton_status:
            result = (canton_status, CantonSerializer(canton_data, many=True).data)
        
        else:
            result = (canton_status, canton_data) 

        return result

    def get_canton_list(self, request=None):

        body = json.loads(request.body.decode('utf-8'))
        province_list = body.get('province_list', [])
        response = []

        if province_list:
            for _province in province_list:
                code_province = _province.get('code', None)
                canton_status, canton_data = self._service_helper.get_all(Canton, province__code = code_province)           

                if canton_status:
                    result_status, result_data = (canton_status, CantonSerializer(canton_data, many=True).data)
        
                else:
                    result_status, result_data = (canton_status, canton_data) 
                
                response.extend(result_data)

        return (True, response)
    
    def get_canton_by_id(self, request, canton_id):

        
        canton_status, canton_data = self._service_helper.get_all(Canton, province__id = canton_id)

        if canton_status:
            result = (canton_status, CantonSerializer(canton_data, many=True).data)
        
        else:
            result = (canton_status, canton_data) 

        return result
    
    def get_all_district(self, request):

        district_status, district_data = self._service_helper.get_all(District)

        if district_status:
            result = (district_status, DistrictSerializer(district_data, many=True).data)
        
        else:
            result = (district_status, district_data) 

        return result
    
    def get_district_by_id(self, request, district_id):

        district_status, district_data = self._service_helper.get_all(District, canton_id = district_id)

        if district_status:
            result = (district_status, DistrictSerializer(district_data, many=True).data)
        
        else:
            result = (district_status, district_data) 

        return result
    
    def get_district_list(self, request):
            
            body = json.loads(request.body.decode('utf-8'))
            canton_list = body.get('canton_list', [])
            response = []
            if canton_list:
                for _canton in canton_list:
                    code_canton = _canton.get('code_canton', None)
                    code_province = _canton.get('code_province', None)
                    district_status, district_data = self._service_helper.get_all(District, canton__code = code_canton, canton__province__code = code_province)
                    if district_status:
                        result_status, result_data = (district_status, DistrictSerializer(district_data, many=True).data)
            
                    else:
                        result_status, result_data = (district_status, district_data) 
                    
                    response.extend(result_data)
    
            return (True, response)
