from cgi import parse_multipart
from users.serializers import CustomUserSerializer, UserRequestSerializer
from general.helpers.services import ServiceHelper
from users.models import UserRequest
from unidecode import unidecode

class UserRequestService():
    
    def __init__(self):
        
        self._service_helper = ServiceHelper()

    def get_all(self, request):

        user_self_management_status, user_self_management_data = \
            self._service_helper.get_all(UserRequest)

        if user_self_management_status:
            result = (user_self_management_status, UserRequestSerializer(user_self_management_data, many=True).data)
        
        else:
            result = (user_self_management_status, user_self_management_data) 

        return result


    def create(self, request):

        data = request.data
        serialized_request_user = UserRequestSerializer(data=data)
        if serialized_request_user.is_valid():
            user_self_management = serialized_request_user.save()
            result = (True, UserRequestSerializer(user_self_management).data)
    
        else:
            result = (False, serialized_request_user.errors)
            
        return result

    
    def create_user_from_user_request(self, request, user_request_id):
        """
        this method is used to create a user from a user request
        with the respective permissions
        """
        user_request_status, user_request = self._service_helper.get_one(UserRequest, user_request_id)
        
        if not user_request_status:
            return (False, user_request)
        
        username = '{first_name}.{last_name}'
        username = username.format(
            first_name=unidecode(user_request.first_name).lower().replace(' ', '_'),
            last_name=unidecode(user_request.last_name).lower().replace(' ', '_')
        )        
        serialized_user = {
            'username': username,
            'first_name': user_request.first_name,
            'last_name': user_request.last_name,
            'institution': user_request.institution,
            'position': user_request.position,
            'email': user_request.email,
            'phone': user_request.phone,
        }

        serialized_user = CustomUserSerializer(data=serialized_user, partial=True)

        if serialized_user.is_valid():
            user = serialized_user.save()
            result = (True, CustomUserSerializer(user).data)
    
        else:
            result = (False, serialized_user.errors)
            
        return result

