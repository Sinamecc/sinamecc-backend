from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from django.http import FileResponse
from general.helpers import ViewHelper
from ppcn.services import PpcnService
import uuid
from django.http import HttpResponse
from django.template import loader
from general.permissions import PermissionsHelper
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from rolepermissions.decorators import has_permission_decorator
from django.utils.decorators import method_decorator
service = PpcnService()
view_helper = ViewHelper(service)
permission = PermissionsHelper()

##
## aux functions endpoint
##

@api_view(['POST'])
@has_permission_decorator('create_ppcn')
def post_ppcn(request):
    if request.method == 'POST':
        result = view_helper.post(request)
    return result

@api_view(['GET'])
##@has_permission_decorator('read_all_ppcn')
def get_ppcn(request,  language = 'en'):
    if request.method == 'GET':
        result = view_helper.get_all(request, language)
    return result

@api_view(['GET'])
@has_permission_decorator('read_ppcn')
def get_one_ppcn(request, id , language = 'en'):
    if request.method == 'GET':
        result = view_helper.get_one(id, language)
    return result

@api_view(['PUT'])
@has_permission_decorator('edit_ppcn')
def put_ppcn(request, id):
    if request.method == 'PUT':
        result = view_helper.put(id, request)
    return result

@api_view(['PATCH'])
@has_permission_decorator('edit_ppcn')
def patch_ppcn(request, id):
    if request.method == 'PATCH':
        result = view_helper.patch(id, request)
    return result


@api_view(['DELETE'])
@has_permission_decorator('delete_ppcn')
def delete_ppcn(request, id):
    if request.method == 'DELETE':
        result = view_helper.delete(id)
    return result

##
## General Endpoints
## 

@api_view(['GET'])
@has_permission_decorator('read_ppcn')
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_geographic_level(request, language = 'en'):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_geographic_level", language)
    return result

@api_view(['GET'])
@has_permission_decorator('read_ppcn')
@parser_classes((MultiPartParser,FormParser, JSONParser,))
def get_required_level(request, language = 'en'):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_required_level", language)
    return result

@api_view(['GET'])
@has_permission_decorator('read_ppcn')
@parser_classes((MultiPartParser,FormParser, JSONParser,))
def get_recognition_type(request, language = 'en'):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_recognition_type", language)
    return result

@api_view(['GET'])
@has_permission_decorator('read_ppcn')
@parser_classes((MultiPartParser,FormParser, JSONParser,))
def get_sector(request, id, language = 'en' ):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_sector", id ,language)
    return result


@api_view(['GET'])
@has_permission_decorator('read_ppcn')
@parser_classes((MultiPartParser,FormParser, JSONParser,))
def get_sub_sector(request, pk, language = "en"):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_sub_sector", pk, language)
    return result

##
## Endpoints
## 
 
@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('create_ppcn')
def post_ppcn_file(request):
    if request.method == 'POST':
        result = view_helper.execute_by_name("post_PPCNFILE", request)

    return result

@api_view(['GET'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('read_ppcn')
def get_form_ppcn(request, geographicLevel_id, language):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_form_ppcn", geographicLevel_id, language)
    return result

@api_view(['GET'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('read_ppcn')
def get_all_ovv(request):
    if request.method == 'GET':
        result = view_helper.get_by_name("get_all_ovv")

    return result

##
## Endpoints with aux views
##

@api_view(['GET','POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('read_ppcn', 'create_ppcn')
def get_post_ppcn(request, language = 'en'):
    if request.method == 'GET':
        result = get_ppcn(request, language)

    elif request.method == 'POST':
        result = post_ppcn(request)

    return result


@api_view(['DELETE', 'PUT', 'PATCH', 'GET'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def put_delete_patch_ppcn(request, id , language = 'en'):

    if request.method == 'GET':
        result = get_one_ppcn(request, id, language)

    elif request.method == 'PUT':
        result = put_ppcn(request, id)

    elif request.method == 'DELETE':
        result = delete_ppcn(request, id)

    elif request.method == 'PATCH':
        result = patch_ppcn(request, id)

    return result





## Review these endpoints ******
@api_view(['GET'])
@has_permission_decorator('read_ppcn')
def get_ppcn_file_version(request, id, ppcn_file_id):
    if request.method == 'GET':
        file_name, file_data = service.download_file(id, ppcn_file_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for get_ppcn_file_version_url view")

@api_view(['GET'])
@has_permission_decorator('read_ppcn')
def get_ppcn_file(request, id, ppcn_file_id):
    if request.method == 'GET':
        file_name, file_data = service.download_ppcn_file(id, ppcn_file_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for get_ppcn_file_version_url view")

@api_view(['GET'])
@has_permission_decorator('read_ppcn')
def get_ppcn_change_log(request, id):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_change_log", id)
    return result


@api_view(['GET'])
@parser_classes((MultiPartParser,FormParser, JSONParser,))
@has_permission_decorator('read_ppcn')
def get_all_ppcn_by_user(request, language = 'en'):
    if request.method == 'GET':
        result = view_helper.get_all(request, language, True)
    return result

@api_view(['GET'])
@parser_classes((MultiPartParser,FormParser, JSONParser,))
@has_permission_decorator('read_ppcn')
def get_all_ppcn(request, language = 'en'):
    if request.method == 'GET':
        result = view_helper.get_all(request, language)
    return result
