from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from mccr.services import MCCRService

service = MCCRService()

@api_view(['GET', 'DELETE', 'PUT'])
@csrf_exempt
def get_mccr(request, id):
    if request.method == 'GET':
        result = _get_one(id)
    elif request.method == 'PUT':
        result = _put(id, request)
    elif request.method == 'DELETE':
        result = _delete(id)
    return result

@api_view(['GET','POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_mccr(request):
    if request.method == 'POST':
        result = _post(request)
    elif request.method == 'GET':
        result = _get_all()
    return result

@api_view(['GET'])
@csrf_exempt
def get_mccr_form(request):
    if request.method == 'GET':
        result = _get_form_data()
    return result

def _get_all():
    get_result, data_result = service.get_all()
    if get_result:
        result = Response(data_result)
    else:
        result = Response(data_result, status=status.HTTP_404_NOT_FOUND)
    return result

def _get_form_data():
    get_result, data_result = service.get_form_data()
    if get_result:
        result = Response(data_result)
    else:
        result = Response(data_result, status=status.HTTP_400_BAD_REQUEST)
    return result

def _get_one(id):
    result_status, result_data = service.get(id)
    if result_status:
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

def _post(request):
    save_result, result_detail = service.create(request)
    if save_result:
        result = Response(result_detail, status=status.HTTP_201_CREATED)
    else:
        result = Response(result_detail, status=status.HTTP_400_BAD_REQUEST)
    return result

def _put(id, request):
    result_status, result_data = service.update(id, request)
    if result_status:
        result = Response(result_data)
    else:
        result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
    return result
