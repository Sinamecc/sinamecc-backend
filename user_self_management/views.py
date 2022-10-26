from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from general.helpers.views import ViewHelper
from user_self_management.services import UserSelfManagementServices


service = UserSelfManagementServices()
view_helper = ViewHelper(service)


def post_user_self_management(request):
    result = view_helper.post(request)
    return result


def get_all_user_self_management(request):
    result = view_helper.get_all(request)
    return result


@api_view(['POST', 'GET'])
def get_post_user_self_management(request):
    if request.method == 'POST':
        result = post_user_self_management
        
    elif request.method == 'GET':
        result = get_all_user_self_management(request)
    
    return result


# Create your views here.
