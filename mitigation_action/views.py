from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from general.helpers.views import ViewHelper
from django.shortcuts import redirect
from mitigation_action.services import MitigationActionService
import uuid
from django.http import FileResponse
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from rolepermissions.decorators import has_permission_decorator
from mitigation_action.models import Mitigation
from django.http import HttpResponseRedirect
service = MitigationActionService()
view_helper = ViewHelper(service)



## Auxialar Endpoint
@api_view(['GET'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('read_all_mitigation_action')
def get_mitigation(request, language='en'):
    if request.method == 'GET':
        result = view_helper.get_all(language)
        return result

@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('create_mitigation_action')
def post_mitigation(request):
    if request.method == 'POST':
        result = view_helper.post(request)
        return result


@api_view(['GET'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('edit_mitigation_action')
def get_one_mitigation(request, pk, language='en'):
    if request.method == 'GET':
        result = view_helper.get_one(pk, language)
        return result


@api_view(['PUT'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('edit_mitigation_action')
def put_mitigation(request, pk, language='en'):
    if request.method == 'PUT':
        result = view_helper.put(request, pk, language='en')
        return result


@api_view(['PATCH'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('edit_mitigation_action')
def patch_mitigation(request, pk, language='en'):
    if request.method == 'PATCH':
        result = view_helper.patch(pk, request)
        return result


@api_view(['DELETE'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
@has_permission_decorator('delte_mitigation_action')
def delete_mitigation(request, pk):
    if request.method == 'DELETE':
        result = view_helper.patch(pk)
        return result

##
## Endpoint
##
 
@api_view(['GET', 'POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_mitigation(request, language='en'):
    if request.method == 'GET':
        result = get_mitigation(request, language)

    elif request.method == 'POST':
        result = post_mitigation(request)

    return result


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_delete_put_patch_mitigation(request, pk, language='en'):
    if request.method == 'GET':
        result = get_one_mitigation(request, pk,language)
    elif request.method == 'DELETE':
        result = delete_mitigation(request, pk)
    elif request.method == 'PUT':
        result = put_mitigation(request, pk, language)
    elif request.method == 'PATCH':
        result = patch_mitigation(request, pk, language)
    return result




## review those endpoints
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def get_mitigation_change_log(request, pk):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_change_log", pk)
    return result

@api_view(['GET'])
def get_mitigations_form(request):
    if request.method == 'GET':
        result = view_helper.get_form_data()
    return result

@api_view(['GET'])
def get_mitigations_form_es_en(request, language, option):
    if request.method == 'GET':
        result = view_helper.execute_by_name( "get_form_data_es_en", language, option)
    return result

@api_view(['GET'])
def get_mitigation_action_file(request, id, file_id):
    if request.method == 'GET':
        file_name, file_data = service.download_file(id, file_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for get_mitigation_action_file_version_url view")

