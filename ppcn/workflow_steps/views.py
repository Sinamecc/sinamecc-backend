from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from general.helpers.views import ViewHelper
from django.http import FileResponse
from ppcn.workflow_steps.services import PPCNWorkflowStepService


service = PPCNWorkflowStepService()
view_helper = ViewHelper(service)
 
@api_view(['POST'])
def post(request, step_label):
    if request.method == 'POST':
        result = view_helper.post(request)
    return result

@api_view(['GET'])
def get(request, step_label, step_id):
    if request.method == 'GET':
        result = view_helper.get_by_name("get_workflow_step", step_id)
    return result

@api_view(['GET'])
def get_workflow_step_file(request, step_label, step_id, step_file_id):
    if request.method == 'GET':
        result = view_helper.download_file(step_id, step_file_id)
    else:
        result = view_helper.error_message("Unsupported METHOD for get_workflow_step_file_version view")
    return result