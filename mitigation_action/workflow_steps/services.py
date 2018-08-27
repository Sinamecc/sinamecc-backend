from mitigation_action.workflow_steps.models import MAWorkflowStep, MAWorkflowStepFile
from mitigation_action.models import Mitigation
from mitigation_action.workflow_steps.serializers import MAWorkflowStepFileSerializer, MAWorkflowStepSerializer
from mitigation_action.workflow_steps.active_steps import WorkflowActiveSteps
from general.storages import S3Storage
from io import BytesIO
import os


class MitigationActionWorkflowStepService():
    def __init__(self):
        self.storage = S3Storage()
        self.WORKFLOW_STEP_FILE_DOES_NOT_EXIST = "Mitigation Action workflow step file does not exist"
        self.WORKFLOW_STEP_DOES_NOT_EXIST = "Mitigation Action workflow step does not exist"
        self.CANT_UPLOAD = "Can't upload Harmonization Ingei file"
        self.active_steps = WorkflowActiveSteps()

    def _get_error_message(self, message):
        return {"error": message}

    def _get_serialized_workflow_step(self, request):
        data = {
            'user': request.user.id,
            'mitigation_action': request.data.get('mitigation'),
            'name': request.data.get('name'),
            'entry_name': request.data.get('entry_name'),
            'status': request.data.get('step_status'),
        }
        return MAWorkflowStepSerializer(data=data)

    def _get_serialized_workflow_step_file(self, request, workflow_step):
        data = {
            'user': request.user.id,
            'workflow_step': workflow_step.id,
            'file': request.data.get('file'),
        }
        return MAWorkflowStepFileSerializer(data=data)

    def create(self, request):
        serialized_step = self._get_serialized_workflow_step(request)
        """ Check if the step is enabled for the workflow """
        if serialized_step.is_valid() and \
                self.active_steps.is_enabled(serialized_step.validated_data.get("name")):
            newly_saved_step = serialized_step.save()
            if newly_saved_step.id:
                self.serialize_and_save_step_file(request, newly_saved_step)
                result = (True, MAWorkflowStepSerializer(newly_saved_step).data)
            else:
                result = (False, self._get_error_message("Error checking id of newly saved workflow step"))
        else:
            if len(serialized_step.errors.keys()) == 0:
                error_message = "Invalid step_label {}".format(serialized_step.validated_data.get("name"))
            else:
                error_message = "Invalid serialized workflow step, errors: {}".format(serialized_step.errors)
            result = (False, self._get_error_message(error_message))
        return result

    def download_file(self, step_id, step_file_id):
        step_file = MAWorkflowStepFile.objects.filter(pk=step_file_id).filter(workflow_step=step_id).first()
        path, filename = os.path.split(step_file.file.name)
        return (filename, BytesIO(self.storage.get_file(step_file.file.name)),)

    def get_workflow_step(self, step_id):
        try:
            serialized_step = MAWorkflowStepSerializer(MAWorkflowStep.objects.get(pk=step_id))
            result = (True, serialized_step.data)
        except MAWorkflowStep.DoesNotExist:
            result = (False, self._get_error_message(self.WORKFLOW_STEP_DOES_NOT_EXIST))
        return result

    def get_workflow_step_file(self, step_file_id):
        try:
            serialized_step_file = MAWorkflowStepFileSerializer(MAWorkflowStepFile.objects.get(pk=step_file_id))
            result = (True, serialized_step_file.data)
        except MAWorkflowStepFile.DoesNotExist:
            result = (False, self._get_error_message(self.WORKFLOW_STEP_FILE_DOES_NOT_EXIST))
        return result

    def serialize_and_save_step_file(self, request, workflow_step):
        serialized_step_file = self._get_serialized_workflow_step_file(request, workflow_step)
        if serialized_step_file.is_valid():
            serialized_step_file.save()
