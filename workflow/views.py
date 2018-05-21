from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status

from workflow.services import WorkflowService

service = WorkflowService()

@api_view(['GET'])
def get_review_status(request):
    if request.method == 'GET':
        result = _get_status_data()
    return result

def _get_status_data():
    get_result, data_result = service.get_status_data()
    if get_result:
        result = Response(data_result)
    else:
        result = Response(data_result, status=status.HTTP_400_BAD_REQUEST)
    return result
