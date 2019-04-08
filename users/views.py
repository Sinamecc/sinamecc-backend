from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from users.services import UserService
from general.helpers import ViewHelper
# Create your views here.

service = UserService()
view_helper = ViewHelper(service)


@api_view(['GET'])
@csrf_exempt
def get_permissions(request):
    if request.method == 'GET':
        result = view_helper.execute_by_name('get_permissions', request)
    return result

@api_view(['GET'])
@csrf_exempt
def get_groups(request):
    if request.method == 'GET':
        result = view_helper.execute_by_name('get_groups', request)
    return result

@api_view(['POST', 'GET'])
@csrf_exempt
def post_get_user(request):
    if request.method == 'GET':
        result = view_helper.get_all(request)

    elif request.method == 'POST':
        result = view_helper.post(request)
    return result

@api_view(['POST'])
@csrf_exempt
def assign_user_to_group(request, username):
    if request.method == 'POST':
        result = view_helper.execute_by_name('assign_user_to_group', request, username)
    return result

@api_view(['POST'])
@csrf_exempt
def assign_user_to_permission(request, username):
    if request.method == 'POST':
        result = view_helper.execute_by_name('assign_user_to_permission', request, username)
    return result
