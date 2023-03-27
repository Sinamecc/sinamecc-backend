from users.serializers import UserRequestSerializer
from general.helpers.services import ServiceHelper
from users.models import UserRequest

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

