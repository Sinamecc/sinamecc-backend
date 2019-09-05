from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from general.helpers import ViewHelper
from django.shortcuts import redirect
from mitigation_action.services import MitigationActionService
import uuid
from django.http import FileResponse
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404

from django.http import HttpResponseRedirect
service = MitigationActionService()
view_helper = ViewHelper(service)
from mitigation_action.models import Mitigation

@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def get_delete_put_patch_mitigation(request, pk, language):
    if request.method == 'GET':
        result = view_helper.get_one(pk,language)
    elif request.method == 'DELETE':
        result = view_helper.delete(pk)
    elif request.method == 'PUT':
        result = view_helper.put(pk, request, language)
    elif request.method == 'PATCH':
        result = view_helper.patch(pk, request)
    return result

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
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_mitigation(request, language):
    if request.method == 'GET':
        result = view_helper.get_all(language)
        return result

@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def post_mitigations(request):
    if request.method == 'POST':
        result = view_helper.post(request)
        return result

def _get_all(language):
    get_result, data_result = service.get_all(language)
    if get_result:
        result = Response(data_result)
    else:
        result = Response(data_result, status=status.HTTP_404_NOT_FOUND)
    return result

def _post(request):
    save_result, result_detail = service.create(request)
    if save_result:
        result = Response(result_detail, status=status.HTTP_201_CREATED)
    else:
        result = Response(result_detail, status=status.HTTP_400_BAD_REQUEST)
    return result

def _get_one(id, language):
    result_status, result_data = service.get(id,language)
    if result_status:
        result = Response(result_data)
    else:
        result = Response(result_data, status=status.HTTP_404_NOT_FOUND)
    return result

def _get_change_log(id):
    result_status, result_data = service.get_change_log(id)
    if result_data:
        result = Response(result_data)
    else:
        result = Response(result_data, status=status.HTTP_404_NOT_FOUND)
    return result

def _delete(id):
    if service.delete(id):
        result = Response({"id": id}, status=status.HTTP_200_OK)
    else:
        result = Response({"id": id}, status=status.HTTP_404_NOT_FOUND)
    return result

def _put(id, request):
    result_status, result_data = service.update(id, request)
    if result_status:
        result = Response(result_data)
    else:
        result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
    return result

def _patch(id, request):
    result_status, result_data = service.patch(id, request)
    if result_status:
        result = Response(result_data)
    else:
        result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
    return result

def _get_form_data():
    get_result, data_result = service.get_form_data()
    if get_result:
        result = Response(data_result)
    else:
        result = Response(data_result, status=status.HTTP_400_BAD_REQUEST)
    return result

def _get_form_data_es_en(language, option):
    get_result, data_result = service.get_form_data_es_en(language, option)
    if get_result:
        result = Response(data_result)
    else:
        result = Response(data_result, status=status.HTTP_400_BAD_REQUEST)
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

def get_notification_template(request, uuid, lang="en"):
    mitigation_result, mitigation_action = service.get(uuid, lang)
    template = loader.get_template('mitigation_action/index.html')
    if mitigation_result:
        context = {
            'lang':lang,
            'mitigation_action': mitigation_action,
        }
        result = HttpResponse(template.render(context, request))
    else:
        template_error = loader.get_template('general/error.html')
        context={
            'error': mitigation_action
        }
        result = HttpResponse(template_error.render(context, request))
    return  result

@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_mitigation_action_opendata(request, usermane, password):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_mitigation_action_opendata", request, usermane, password)
        return result