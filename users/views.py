from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from users.services import UserService
from general.helpers import ViewHelper
from django.http import FileResponse
# Create your views here.

service = UserService()
view_helper = ViewHelper(service)


@api_view(['GET', 'POST'])
@csrf_exempt
def post_get_permissions(request):
    if request.method == 'GET':
        result = view_helper.execute_by_name('get_permissions', request)
    elif request.method == 'POST':
        result = view_helper.execute_by_name('create_permission', request)
    return result

@api_view(['POST', 'GET'])
@csrf_exempt
def post_get_user(request):
    if request.method == 'GET':
        result = view_helper.get_all(request)

    elif request.method == 'POST':
        result = view_helper.post(request)
    return result



@api_view(['GET', 'POST'])
@csrf_exempt
def post_get_all_profile_picture(request, user_id):
    if request.method == 'GET':
        result = view_helper.execute_by_name('get_all_profile_picture', user_id)

    elif request.method == 'POST':
        result = view_helper.execute_by_name('create_profile_picture', request, user_id)

    return result




 ## Review this    
@api_view(['GET', 'POST'])
@csrf_exempt
def post_get_groups(request):
    if request.method == 'GET':
        result = view_helper.execute_by_name('get_all_groups', request)
    elif request.method == 'POST':
        result = view_helper.execute_by_name('create_group', request)
    
    return result

@api_view(['GET', 'PUT'])
@csrf_exempt
def put_get_group(request, group_id):
    if request.method == 'GET':
        result = view_helper.execute_by_name('get_group', request, group_id)
    elif request.method == 'PUT':
        result = view_helper.execute_by_name('update_group', request, group_id)
    
    return result

@api_view(['POST', 'PUT'])
@csrf_exempt
def assign_user_to_group(request, username):
    if request.method == 'POST':
        result = view_helper.execute_by_name('assign_user_to_group', request, username)
    elif request.method == 'PUT':
        result = view_helper.execute_by_name('unassign_user_to_group', request, username)
    return result

@api_view(['POST', 'PUT'])
@csrf_exempt
def assign_user_to_permission(request, username):
    if request.method == 'POST':
        result = view_helper.execute_by_name('assign_user_to_permission', request, username)
    elif request.method == 'PUT':
        result = view_helper.execute_by_name('unassign_user_to_permission', request, username)
    return result

@api_view(['PUT'])
@csrf_exempt
def put_user(request, user_id):
    if request.method == 'PUT':
        result = view_helper.put(request, user_id)
    return result

@api_view(['PUT'])
@csrf_exempt
def put_password(request, user_id):
    if request.method == 'PUT':
        result = view_helper.execute_by_name('update_password', request, user_id)
    return result


@api_view(['GET'])
@csrf_exempt
def get_profile_picture_version(request, image_id, user_id):
    if request.method == 'GET':
        file_name, file_data = view_helper.service.download_profile_picture(image_id, user_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for download_profile_picture view")