from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.http import FileResponse
from rolepermissions.decorators import has_permission_decorator
from general.helpers.views import ViewHelper
from report_data.services import ReportDataService

service = ReportDataService()
view_helper = ViewHelper(service)

@has_permission_decorator('read_report_data')
def get_one_report_data(request, pk):
    if request.method == 'GET':
        result = view_helper.get_one(pk)
    return result

@has_permission_decorator('edit_report_data')
def put_report_data(request, pk):
    if request.method == 'PUT':
        result = view_helper.put(pk, request)
    return result

@has_permission_decorator('delete_report_data')
def delete_report_data(request, pk):
    if request.method == 'DELETE':
        result = view_helper.delete(pk)
    return result

@has_permission_decorator('edit_report_data')
def patch_report_data(request, pk):
    if request.method == 'PATCH':
        result = view_helper.patch(pk, request)
    return result

@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def get_delete_update_patch_report_data(request, pk):
    if request.method == 'GET':
        result = get_one_report_data(request, pk)

    elif request.method == 'PUT':
        result = put_report_data(request, pk)

    elif request.method == 'DELETE':
        result = delete_report_data(request, pk)
        
    elif request.method == 'PATCH':
        result = patch_report_data(request, pk)
        
    return result


@api_view(['GET'])
def get_report_file_versions(request, pk):
    if request.method == 'GET':
        versions = service.get_all_file_versions(pk)
        return Response(versions)


@api_view(['GET', 'POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_report_data(request):
    if request.method == 'POST':
        result = view_helper.post(request)

    elif request.method == 'GET':
        result = view_helper.get_all(request)

    return result


@api_view(['GET'])
def get_report_file_version_url(request, report_file_id, report_file_version_id):
    if request.method == 'GET':
        file_name, file_data = service.download_file(report_file_id, report_file_version_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream', )
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for get_report_file_version_url view")


@api_view(['GET'])
def get_catalog_data(request): ## We need delete *args this parametes is temp at the moment to refactor MA
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_catalog_data", request)
    
    return result


@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def upload_file_to_report_data(request, report_data_id):
    if request.method == 'POST':
        result = view_helper.execute_by_name('upload_file_to',request, report_data_id)

    return result


@api_view(['GET'])
def get_file_to_report_data(request, report_file_id):
    if request.method == 'GET':
        result = view_helper.call_download_file_method('download_report_file', request, report_file_id)

        return result

@api_view(['GET'])
def get_source_file_to_report_data(request, report_data_id):
    if request.method == 'GET':
        result = view_helper.call_download_file_method('download_source_file', request, report_data_id)

        return result


@api_view(['GET'])
def get_comments(request, report_data_id, fsm_state=None, review_number=None):
    if request.method == 'GET' and not (fsm_state or review_number):
        result = view_helper.execute_by_name('get_current_comments', request, report_data_id)

    elif request.method == 'GET' and (fsm_state or review_number):
        result = view_helper.execute_by_name('get_comments_by_fsm_state_or_review_number', request, report_data_id, fsm_state, review_number)

    return result
