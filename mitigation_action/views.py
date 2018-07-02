from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status

from mitigation_action.services import MitigationActionService
import uuid

service = MitigationActionService()

@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def get_delete_update_patch_mitigation(request, pk):
    if request.method == 'GET':
        result = _get_one(pk)
    elif request.method == 'DELETE':
        result = _delete(pk)
    elif request.method == 'PUT':
        result = _put(pk, request)
    elif request.method == 'PATCH':
        result = _patch(pk, request)
    return result

@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def get_mitigation_change_log(request, pk):
    if request.method == 'GET':
        result = _get_change_log(pk)
    return result

@api_view(['GET'])
def get_mitigations_form(request):
    if request.method == 'GET':
        result = _get_form_data()
    return result

@api_view(['GET'])
def get_mitigations_form_es_en(request, language):
    if request.method == 'GET':
        result = _get_form_data_es_en(language)
    return result

@api_view(['GET', 'POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_mitigations(request):
    if request.method == 'GET':
        result = _get_all()
    elif request.method == 'POST':
        result = _post(request)
    return result

def _get_all():
    get_result, data_result = service.get_all()
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

def _get_one(id):
    result_status, result_data = service.get(id)
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

def _get_form_data_es_en(language):
    get_result, data_result = service.get_form_data_es_en(language)
    if get_result:
        result = Response(data_result)
    else:
        result = Response(data_result, status=status.HTTP_400_BAD_REQUEST)
    return result