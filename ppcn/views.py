from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from django.http import FileResponse
from general.helpers import ViewHelper
from ppcn.services import PpcnService
import uuid

service = PpcnService()
view_helper = ViewHelper(service)

@api_view(['GET'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_geographic_level(request, language = 'en'):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_geographic_level", language)
    return result

@api_view(['GET'])
@parser_classes((MultiPartParser,FormParser, JSONParser,))
def get_required_level(request, language = 'en'):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_required_level", language)
    return result

@api_view(['GET'])
@parser_classes((MultiPartParser,FormParser, JSONParser,))
def get_recognition_type(request, language = 'en'):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_recognition_type", language)
    return result

@api_view(['GET'])
@parser_classes((MultiPartParser,FormParser, JSONParser,))
def get_sector(request, id, language = 'en' ):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_sector", id ,language)
    return result


@api_view(['GET'])
@parser_classes((MultiPartParser,FormParser, JSONParser,))
def get_sub_sector(request, pk, language = "en"):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_all_sub_sector", pk, language)
    return result


@api_view(['GET','POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_ppcn(request, language = 'en'):
    if request.method == 'GET':
        result = view_helper.get_all(language)

    elif request.method == 'POST':
        result = view_helper.post(request)

    return result

@api_view(['GET'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_one_ppcn(request, id , language = 'en'):
    if request.method == 'GET':
        result = view_helper.get_one(id, language)
    return result

@api_view(['DELETE', 'PUT'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def put_delete_ppcn(request, id , language = 'en'):
    if request.method == 'PUT':
        result = view_helper.put(id, request)
    elif request.method == 'DELETE':
        result = view_helper.delete(id)
    return result


@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def post_ppcn_file(request):
    if request.method == 'POST':
        result = view_helper.execute_by_name("post_PPCNFILE", request)
    return result

@api_view(['GET'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_form_ppcn(request, geographicLevel_id, language):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_form_ppcn", geographicLevel_id, language)
    return result

@api_view(['GET'])
def get_ppcn_file_version(request, id, ppcn_file_id):
    if request.method == 'GET':
        file_name, file_data = service.download_file(id, ppcn_file_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for get_ppcn_file_version_url view")
