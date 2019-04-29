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
from general.permissions import PermissionsHelper

permission = PermissionsHelper()
service = MCCRService()
view_helper = ViewHelper(service)


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@csrf_exempt
def get_mccr(request, id):

    if request.method == 'GET':
        result = view_helper.get_one(id)
    elif request.method == 'PUT':
        result = view_helper.put(id, request)
    elif request.method == 'DELETE':
        result = view_helper.delete(id)
    elif request.method == 'PATCH':
        result = view_helper.patch(id, request)
    return result


@api_view(['GET','POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_mccr(request):
    if request.method == 'POST':
        result = view_helper.post(request)
    elif request.method == 'GET':
        result = view_helper.get_all()
    return result

@api_view(['GET'])
@csrf_exempt
def get_mccr_form(request):
    if request.method == 'GET':
        result = view_helper.get_form_data()
    return result

@api_view(['GET'])
def get_mccr_file_version(request, id, mccr_file_id):
    if request.method == 'GET':
        file_name, file_data = service.download_file(id, mccr_file_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for get_report_file_version_url view")

@api_view(['GET'])
@csrf_exempt
def get_all_ovv(request):
    if request.method == 'GET':
        result = view_helper.get_by_name("get_all_ovv")
    return result

@api_view(['PATCH'])
@csrf_exempt
def patch_mccr_ovv(request, mccr_id, ovv_id):
    if request.method == 'PATCH':
        result = view_helper.execute_by_name("update_mccr_ovv_relation", mccr_id, ovv_id)
    return result

def get_notification_template(request, mccr_id, lang="en"):
    mccr_result, mccr = service.get(mccr_id)
    template = loader.get_template('mccr/index.html')
    if mccr_result:
        context = {
            'lang': lang,
            'mccr': mccr
        }
        result = HttpResponse(template.render(context, request))
    else:
        template_error = loader.get_template('general/error.html')
        context={
            'error': mccr['error']
        }
        result = HttpResponse(template_error.render(context, request))
    return  result
    
def redirect_notification(request, mccr_id):
    path = '/'.join(request.META['HTTP_REFERER'].split('/')[:3])
    url_frontend = '{0}/mccr/registries/{1}'.format(path, mccr_id) #change me in development
    return HttpResponseRedirect(url_frontend)
