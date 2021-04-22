from django.urls import reverse
from general.storages import S3Storage
from mitigation_action.models import MitigationAction
from mccr.models import MCCRRegistry, MCCRUserType, MCCRFile, OVV
from mccr.serializers import MCCRRegistrySerializerView, MCCRRegistrySerializerCreate, MCCRFileSerializer, MCCRRegistryOVVRelationSerializer
from mccr.workflow_steps.services import MCCRWorkflowStepService
from rest_framework.parsers import JSONParser
from django_fsm import can_proceed, has_transition_perm
from io import BytesIO
import uuid
import os
from django.contrib.auth.models import *
from general.services import EmailServices
email_sender  = "sinamec@grupoincocr.com" ##change to sinamecc email
ses_service = EmailServices(email_sender)
# TODO: Change is_valid() to exception
class MCCRService():
    def __init__(self):
        self.MCCR_ERROR_CREATE = "MCCR couldn't be created"
        self.MCCR_ERROR_NOT_EXIST = "MCCR does not exists"
        self.MCCR_ERROR_GET_ALL = "Error retrieving all MCCR records"
        self.MCCR_ERROR_EMPTY_MITIGATIONS_LIST = "Empty mitigation actions list"
        self.MCCR_ERROR_EMPTY_OVV_LIST = "Empty OVV list"
        self.MCCR_ERROR_UNKNOWN_MITIGATION_LIST = "Unknown error retrieving mitigation actions list"
        self.INVALID_STATUS_TRANSITION = "Invalid mitigation action state transition."
        self.NO_PATCH_DATA_PROVIDED = "No PATCH data provided."
        self.STATE_HAS_NO_AVAILABLE_TRANSITIONS = "State has no available transitions."
        self.INVALID_USER_TRANSITION = "the user doesn't have permission for this transition"
        self.workflow_step_services = MCCRWorkflowStepService()

        self.storage = S3Storage()

    def get_serialized_mccr(self, request):
        d = {
            "status": request.data.get("status"),
            "user": request.user.id,
            "mitigation": request.data.get("mitigation"),
            "user_type": request.data.get("user_type")
        }
        serialized_mccr = MCCRRegistrySerializerCreate(data=d)
        return serialized_mccr

    def get_serialized_mccr_file(self, mccr_id, user_id, file):
        file_list = {
                "file": file,
                "user": user_id,
                "mccr": mccr_id
            }
        serializer = MCCRFileSerializer(data=file_list)
        return serializer

    def get_serialized_mccr_ovv_relation(self, mccr_id, ovv_id):
        mccr_ovv_relation = {"ovv": ovv_id, "mccr": mccr_id, "status": "ovv_assigned_first_review"}
        serializer = MCCRRegistryOVVRelationSerializer(data=mccr_ovv_relation)
        return serializer

    def get_serialized_for_existent(self, request, mccr_registry):
        data = JSONParser().parse(request)
        serialized_mccr = MCCRRegistrySerializerCreate(mccr_registry, data=data)
        return serialized_mccr

    def get_one(self, str_uuid):
        f_uuid = uuid.UUID(str_uuid)
        return MCCRRegistry.objects.get(pk=f_uuid)

    def next_action(self, mccr_registry):
        result = None
        result = {'states': False, 'required_comments': False}
        transitions = mccr_registry.get_available_fsm_state_transitions()
        states = []
        for transition in  transitions:
            states.append(transition.target)
        result['states'] = states if len(states) else False

        #change here , only some states can have comments
        result['required_comments'] = True if len(states) > 0 else False
            
        return result

    def serialize_and_save_files(self, request, mccr_id):
        for f in request.data.getlist("files[]"):
            serialized_file = self.get_serialized_mccr_file(mccr_id, request.user.id, f)
            if serialized_file.is_valid():
                serialized_file.save()

    # TODO: Handle exception
    def create(self, request):
        errors = []
        serialized_mccr = self.get_serialized_mccr(request)
        result = (False, self.MCCR_ERROR_CREATE)
        if serialized_mccr.is_valid():
            new_mccr = serialized_mccr.save()
            if new_mccr.id:
                # TODO: check operation to revert
                self.serialize_and_save_files(request, new_mccr.id)
                mccr_previous_status = new_mccr.fsm_state
                if not has_transition_perm(new_mccr.submit, request.user):
                    errors.append(self.INVALID_USER_TRANSITION)
                    result = (False, errors)
                else:
                    new_mccr.submit()
                    new_mccr.save()
                    #self.create_change_log_entry(new_mccr, mccr_previous_status, new_mccr.fsm_state, request.data.get('user'))  
                    result = (True, MCCRRegistrySerializerCreate(new_mccr).data)

            
        return result

    def get(self, id):
        try:
            mccr = self.get_one(id)
            serialized_mccr = MCCRRegistrySerializerView(mccr)
            content = serialized_mccr.data
            content['files'] = self._get_files_list(mccr.files)
            content['workflow_step_files'] = self.workflow_step_services._get_files_list([f.workflow_step_file.all() for f in mccr.workflow_step.all()])
            content['next_state'] = self.next_action(mccr)
            result = (True, content)
        except MCCRRegistry.DoesNotExist:
            result = (False, {"error": self.MCCR_ERROR_NOT_EXIST})
        return result

    def get_all(self, request):
        try:
            m_list = [
                {
                    'id': m.id,
                    'status': m.status,
                    'user_id': m.user.id,
                    'user': m.user.username,
                    'mitigation_id': m.mitigation.id,
                    'mitigation': m.mitigation.name,
                    'user_type_id': m.user_type.id,
                    'user_type': m.user_type.name,
                    'files': MCCRFile.objects.filter(mccr_id=m.id).count(),
                    'fsm_state': m.fsm_state,
                    'next_state': self.next_action(m)
                } for m in MCCRRegistry.objects.all()
            ]
            result = (True, m_list)
        except MCCRRegistry.DoesNotExist:
            result = (False, self.MCCR_ERROR_GET_ALL)
        return result

    def get_form_data(self):
        try:
            mitigation_list = [
                {
                    "id": str(m.id),
                    "name": m.name,
                } for m in MitigationAction.objects.all()
            ]
            user_types_list = [
                {
                    "id": str(u.id),
                    "name": u.name,
                } for u in MCCRUserType.objects.all()
            ]
            final_result = {
                "mitigations": mitigation_list,
                "user_types": user_types_list,
            }
            result = (True, final_result)
        except MitigationAction.DoesNotExist:
            result = (False, {"error": self.MCCR_ERROR_EMPTY_MITIGATIONS_LIST})
        except:
            result = (False, {"error": self.MCCR_ERROR_UNKNOWN_MITIGATION_LIST})
        return result

    def get_all_ovv(self):
        try:
            ovv_list = [
                {
                    "id": o.id,
                    "name": o.name,
                    "email": o.email,
                    "phone": o.phone
                } for o in OVV.objects.all()
            ]
            result = (True, ovv_list)
        except OVV.DoesNotExist:
            result = (False, {"error": self.MCCR_ERROR_EMPTY_OVV_LIST})
        except:
            result = (False, {"error": self.MCCR_ERROR_UNKNOWN_MITIGATION_LIST})
        return result

    # TODO: handle exception when id not exist
    def update(self, id, request):
        mccr_registry = self.get_one(id)
        serialized_mccr = self.get_serialized_for_existent(request, mccr_registry)
        if serialized_mccr.is_valid():
            result = (True, MCCRRegistrySerializerCreate(serialized_mccr.save()).data)
            # we update the fsm state machine
        else:
            result = (False, serialized_mccr.errors)
        return result

    def update_fsm_state(self, next_state, mccr_registry,user):
        result = (False, self.INVALID_STATUS_TRANSITION)
        # --- Transition ---
        # source -> target
        transitions = mccr_registry.get_available_fsm_state_transitions()
        states = {}
        for transition in  transitions:
            states[transition.target] = transition

        states_keys = states.keys()
        if len(states_keys) <= 0: result = (False, self.STATE_HAS_NO_AVAILABLE_TRANSITIONS)

        if next_state in states_keys:
            state_transition= states[next_state]
            transition_function = getattr(mccr_registry ,state_transition.method.__name__)

            if has_transition_perm(transition_function,user):
                transition_function()
                mccr_registry.save()
                result = (True, MCCRRegistrySerializerCreate(mccr_registry).data)
            else: result = (False, self.INVALID_STATUS_TRANSITION)
            
        
        return result

    def patch(self, id, request):
        mccr = self.get_one(id)
        if (request.data.get('fsm_state')):
            patch_data = {
                # 'review_count': mccr.review_count + 1
            }
            serialized_mccr_registry = MCCRRegistrySerializerCreate(mccr, data=patch_data, partial=True)
            if serialized_mccr_registry.is_valid():
                mccr_registry_previous_state = mccr.fsm_state
                mccr_registry = serialized_mccr_registry.save()
                update_state_status, update_state_data = self.update_fsm_state(request.data.get('fsm_state'), mccr_registry,request.user)
                if update_state_status:
                    # self.create_change_log_entry(mccr_registry, mccr_registry_previous_state, mccr_registry.fsm_state, request.data.get('user'))
                    result = (True, update_state_data)
                else:
                    result = (False, update_state_data)
            if (request.data.get('comment')):
                # asign comment to status change
                result = (True, MCCRRegistrySerializerCreate(mccr_registry).data)
        else:
            result = (False, self.NO_PATCH_DATA_PROVIDED)
        return result

    def update_mccr_ovv_relation(self, mccr_id, ovv_id):
        mccr = self.get_one(mccr_id)
        serialized_mccr_ovv_relation = self.get_serialized_mccr_ovv_relation(mccr_id, ovv_id)
        if serialized_mccr_ovv_relation.is_valid():
            # TODO: should check if we have a previous registered status for the tuple mccr,ovv
            serialized_mccr_ovv_relation.save()
            ## we need to pass ovv_id to send notification 
            mccr.assigned_send_notification()
            mccr.save()
            result = (True, serialized_mccr_ovv_relation.data)
        else:
            result = (False, serialized_mccr_ovv_relation.errors)
        return result

    def delete(self, id):
        try:
            mccr = self.get_one(id)
            mccr.delete()
            result = (True, {"Result":"MCCR has been delete"})
        except MCCRRegistry.DoesNotExist:
            result = (False, {"Result":"MMCR has been delete"})
        return result

    def get_file_content(self, mccr_id, mccr_file_id):
        mccr_file = MCCRFile.objects.get(pk=mccr_file_id)
        path, filename = os.path.split(mccr_file.file.name)
        return (filename, BytesIO(self.storage.get_file(mccr_file.file.name)),)

    def download_file(self, mccr_id, mccr_file_id):
        return self.get_file_content(mccr_id, mccr_file_id)

    def _get_files_list(self, file_list):
        return [{'name': self._get_filename(f.file.name), 'file': self._get_file_path(str(f.mccr.id), str(f.id))} for f in file_list.all() ]

    def _get_file_path(self, mccr_id, mccr_file_id):
        url = reverse("get_mccr_file_version", kwargs={'id': mccr_id, 'mccr_file_id': mccr_file_id})
        return url

    def _get_filename(self, filename):
        fpath, fname = os.path.split(filename)
        return fname