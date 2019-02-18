from mccr.workflow_steps.models import MCCRWorkflowStep, MCCRWorkflowStepFile
from mccr.models import MCCRRegistry
from mccr.workflow_steps.serializers import MCCRWorkflowStepFileSerializer, MCCRWorkflowStepSerializer
from mccr.workflow_steps.active_steps import WorkflowActiveSteps
from general.storages import S3Storage
from django_fsm import can_proceed
from django.urls import reverse
from io import BytesIO
import os


class MCCRWorkflowStepService():
    def __init__(self):
        self.storage = S3Storage()
        self.WORKFLOW_STEP_FILE_DOES_NOT_EXIST = "MCCR workflow step file does not exist"
        self.WORKFLOW_STEP_DOES_NOT_EXIST = "MCCR workflow step does not exist"
        self.CANT_UPLOAD = "Can't upload MCCR Detail file"
        self.active_steps = WorkflowActiveSteps()

    def _get_error_message(self, message):
        return {"error": message}

    def _get_serialized_workflow_step(self, request):
        data = {
            'user': request.user.id,
            'mccr': request.data.get('mccr'),
            'name': request.data.get('name'),
            'entry_name': request.data.get('entry_name'),
            'status': request.data.get('step_status'),
        }
        return MCCRWorkflowStepSerializer(data=data)

    def _get_serialized_workflow_step_file(self, request, workflow_step):
        data = {
            'user': request.user.id,
            'workflow_step': workflow_step.id,
            'file': request.data.get('file'),
        }
        return MCCRWorkflowStepFileSerializer(data=data)

    def create(self, request):
        serialized_step = self._get_serialized_workflow_step(request)
        """ Check if the step is enabled for the workflow """
        if serialized_step.is_valid() and \
                self.active_steps.is_enabled(serialized_step.validated_data.get("name")):
            
            mccr_registry = serialized_step.validated_data.get("mccr")
            newly_saved_step = None
            if mccr_registry != None:
                if mccr_registry.can_ovv_upload_evaluation():
                    mccr_registry.ovv_upload_evaluation()
                    mccr_registry.save()
                    newly_saved_step = serialized_step.save()
                
                elif mccr_registry.can_ovv_assign():
                    mccr_registry.ovv_assign()
                    mccr_registry.save()
                    newly_saved_step = serialized_step.save()
                
                elif mccr_registry.can_decision_step_ovv_evaluation_monitoring():
                    mccr_registry.decision_step_ovv_evaluation_monitoring()
                    mccr_registry.save()
                    newly_saved_step = serialized_step.save()
            

            if newly_saved_step != None and newly_saved_step.id:
                self.serialize_and_save_step_file(request, newly_saved_step)
                result = (True, MCCRWorkflowStepSerializer(newly_saved_step).data)
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
        step_file = MCCRWorkflowStepFile.objects.filter(pk=step_file_id).filter(workflow_step=step_id).first()
        path, filename = os.path.split(step_file.file.name)
        return (filename, BytesIO(self.storage.get_file(step_file.file.name)),)

    def get_workflow_step(self, step_id):
        try:
            serialized_step = MCCRWorkflowStepSerializer(MCCRWorkflowStep.objects.get(pk=step_id))
            result = (True, serialized_step.data)
        except MCCRWorkflowStep.DoesNotExist:
            result = (False, self._get_error_message(self.WORKFLOW_STEP_DOES_NOT_EXIST))
        return result

    def get_workflow_step_file(self, step_file_id):
        try:
            serialized_step_file = MCCRWorkflowStepFileSerializer(MCCRWorkflowStepFile.objects.get(pk=step_file_id))
            result = (True, serialized_step_file.data)
        except MCCRWorkflowStepFile.DoesNotExist:
            result = (False, self._get_error_message(self.WORKFLOW_STEP_FILE_DOES_NOT_EXIST))
        return result

    def _get_files_list(self, file_list):
        if len(file_list):
            for q in file_list: file_list[0] = file_list[0].union(q)
            file_list = file_list[0]
            result = [{'name': self._get_filename(f.file.name) ,'file': self._get_file_path(f.workflow_step.name, f.workflow_step.id, f.id)} for f in file_list]
        else:
            result = []
        return result

    def _get_file_path(self, mccr_step_label, mccr_step_id, mccr_step_file_id , ):
        url = reverse("get_workflow_step_file_version", kwargs={'step_label': mccr_step_label, 'step_id': mccr_step_id, 'step_file_id': mccr_step_file_id })
        return url


    def _get_filename(self, filename):
        fpath, fname = os.path.split(filename)
        return fname

    def serialize_and_save_step_file(self, request, workflow_step):
        serialized_step_file = self._get_serialized_workflow_step_file(request, workflow_step)
        if serialized_step_file.is_valid():
            serialized_step_file.save()
