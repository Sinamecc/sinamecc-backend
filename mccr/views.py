from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from rest_framework import status
from mccr.services import MCCRService
from general.helpers import ViewHelper
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from rolepermissions.decorators import has_permission_decorator
service = MCCRService()
view_helper = ViewHelper(service)

##
## aux function endpoint
##

@api_view(['GET'])
@has_permission_decorator('read_all_mccr')
def get_mccr(request):
    if request.method == 'GET':
        result = view_helper.get_all(request)
    return result

@api_view(['GET'])
@has_permission_decorator('read_mccr')
def get_one_mccr(request, id):
    if request.method == 'GET':
        result = view_helper.get_one(id)
    return result

@api_view(['POST'])
@has_permission_decorator('create_mccr')
def post_mccr(request):
    if request.method == 'POST':
        result = view_helper.post(request)
    return result

@api_view(['PUT'])
@has_permission_decorator('edit_mccr')
def put_mccr(request, id):
    if request.method == 'PUT':
        result = view_helper.put(id, request)
    return result

@api_view(['PATCH'])
@has_permission_decorator('edit_mccr')
def patch_mccr(request, id):
    if request.method == 'PATCH':
        result = view_helper.patch(id, request)
    return result

@api_view(['DELETE'])
@has_permission_decorator('delete_mccr')
def delete_mccr(request, id):
    if request.method == 'DELETE':
        result = view_helper.delete(id)
    return result





##
## General Endpoints
## 
@csrf_exempt
@api_view(['GET'])
@has_permission_decorator('read_mccr')
def get_mccr_form(request):
    if request.method == 'GET':
        result = view_helper.get_form_data()
    return result

@csrf_exempt
@api_view(['GET'])
@has_permission_decorator('read_mccr')
def get_mccr_file_version(request, id, mccr_file_id):
    if request.method == 'GET':
        file_name, file_data = service.download_file(id, mccr_file_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for get_report_file_version_url view")

@csrf_exempt
@api_view(['GET'])
@has_permission_decorator('read_mccr')
def get_all_ovv(request):
    if request.method == 'GET':
        result = view_helper.get_by_name("get_all_ovv")
    return result

@csrf_exempt
@api_view(['PATCH'])
@has_permission_decorator('edit_mccr')
def patch_mccr_ovv(request, mccr_id, ovv_id):
    if request.method == 'PATCH':
        result = view_helper.execute_by_name("update_mccr_ovv_relation", mccr_id, ovv_id)
    return result


##
## Endpoints with aux views
##

@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@csrf_exempt
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_put_patch_delete_mccr(request, id):
    if request.method == 'GET':
        result = get_one_mccr(request, id)
    elif request.method == 'PUT':
        result = put_mccr(request, id)
    elif request.method == 'DELETE':
        result = delete_mccr(request ,id)
    elif request.method == 'PATCH':
        result = patch_mccr(request, id)
    return result


@api_view(['GET','POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_mccr(request):
    if request.method == 'POST':
        result = post_mccr(request)
    elif request.method == 'GET':
        result = get_mccr(request)
    return result



