from rest_framework import viewsets

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
