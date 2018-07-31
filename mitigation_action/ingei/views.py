from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from general.helpers import ViewHelper
from mitigation_action.ingei.services import HarmonizationIngeiService
from django.http import FileResponse

service = HarmonizationIngeiService()
view_helper = ViewHelper(service)

def _post(request):
    save_result, result_detail = service.create(request)
    if save_result:
        result = Response(result_detail, status=status.HTTP_201_CREATED)
    else:
        result = Response(result_detail, status=status.HTTP_400_BAD_REQUEST)
    return result

@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def post(request):
    if request.method == 'POST':
        result = view_helper.post(request)
        return result

@api_view(['GET'])
def get_harmonization_ingei_file_version(request, id, harmonization_ingei_file_id):
    if request.method == 'GET':
        file_name, file_data = service.download_file(id, harmonization_ingei_file_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response
    return view_helper.error_message("Unsupported METHOD for get_Harmonization_ingei_file_version_url view")