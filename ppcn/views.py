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

from django.http import HttpResponseRedirect
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

@api_view(['DELETE', 'PUT', 'PATCH'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def put_delete_patch_ppcn(request, id , language = 'en'):
    if request.method == 'PUT':
        result = view_helper.put(id, request)
    elif request.method == 'DELETE':
        result = view_helper.delete(id)
    elif request.method == 'PATCH':
        result = view_helper.patch(id, request)
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
def get_all_ovv(request):
    if request.method == 'GET':
        result = view_helper.get_by_name("get_all_ovv")
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

@api_view(['GET'])
def get_ppcn_file(request, id, ppcn_file_id):
    if request.method == 'GET':
        file_name, file_data = service.download_ppcn_file(id, ppcn_file_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for get_ppcn_file_version_url view")

@api_view(['GET'])
def get_ppcn_change_log(request, id):
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_change_log", id)
    return result

def get_notification_template(request, id, lang="en"):
    ppcn_result, ppcn = service.get(id, 'en')
    template = loader.get_template('ppcn/index.html')
    if ppcn_result:
        context = {
            'lang': lang,
            'ppcn': ppcn,
        }
        result = HttpResponse(template.render(context, request))
    else:
        template_error = loader.get_template('general/error.html')
        context={
            'error': ppcn
        }
        result = HttpResponse(template_error.render(context, request))
    return  result
    
def redirect_notification(request, id):
    path = '/'.join(request.META['HTTP_REFERER'].split('/')[:3])
    url_frontend = '{0}/ppcn/{1}'.format(path, id) #change me in development
    return HttpResponseRedirect(url_frontend)
