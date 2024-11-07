from rest_framework import viewsets
from rest_framework.decorators import action
from general.helpers.views import ViewHelper
from users.services.user_request import UserRequestService


class UserRequestViewSet(viewsets.ViewSet):

    view_helper = ViewHelper(UserRequestService())

    def list(self, request, pk=None):
        result =  self.view_helper.get_all(request)

        return result
    
    
    def create(self, request, pk=None):
        result = self.view_helper.post(request)
        
        return result
    
    
    @action(detail=True, methods=['put'], url_path='approve')
    def approve_create_user(self, request, pk=None):
        """
        Create a user from a user request
        """
        result = self.view_helper.execute_by_name('create_user_from_user_request',request, pk)
        
        return result
