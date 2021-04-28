
from mitigation_action.workflow_steps.models import *
from mitigation_action.serializers import *
from mitigation_action.models import MitigationAction, Contact, Status, FinanceSourceType, FinanceStatus, \
    InitiativeType, GeographicScale

from general.storages import S3Storage
from django_fsm import RETURN_VALUE, can_proceed, has_transition_perm
import datetime
import uuid
from io import BytesIO
from django.urls import reverse
import os
from general.services import HandlerErrors
from workflow.services import WorkflowService
from general.helpers.services import ServiceHelper
from general.helpers.serializer import SerializersHelper
from general.services import EmailServices

handler = HandlerErrors()
workflow_service = WorkflowService()


class MitigationActionService():
    
    def __init__(self):
        self.storage = S3Storage()
        self._service_helper = ServiceHelper()
        self._serialize_helper = SerializersHelper()
        self.INVALID_STATUS_TRANSITION = "Invalid mitigation action state transition."
        self.STATE_HAS_NO_AVAILABLE_TRANSITIONS = "State has no available transitions."
        self.INVALID_USER_TRANSITION = "the user doesn´t have permission for this transition"

    

    def _get_serialized_status(self, data, status=False):

        serializer = self._serialize_helper.get_serialized_record(StatusSerializer, data, record=status)

        return serializer


    def get_catalog_data(self, request):
        
        catalog = {
            'initiative_type': (InitiativeType, InitiativeTypeSerializer),
            'status': (Status, StatusSerializer),
            'finance_source_type': (FinanceSourceType, FinanceSourceTypeSerializer),
            'finance_status': (FinanceStatus, FinanceStatusSerializer),
            'geographic_scale': (GeographicScale, GeographicScaleSerializer)
        }

        data = {}
        error = False

        for name , (_model, _serializer) in catalog.items():
            result_status, result_data = self._service_helper.get_all(_model)

            if not result_status:
                result = (False, result_data)
                error = True
                break
            
            data = {**data, **{name: _serializer(result_data, many=True).data}}
        
        if not error:
            result = (True, data)
        
        return result







        result = (True, {})

        return result

    def update_fsm_state(self, next_state, mitigation_action,user):

        result = (False, self.INVALID_STATUS_TRANSITION)
        # --- Transition ---
        # source -> target

        transitions = mitigation_action.get_available_fsm_state_transitions()
        states = {}
        for transition in  transitions:
            states[transition.target] = transition

        states_keys = states.keys()
        if len(states_keys) <= 0: result = (False, self.STATE_HAS_NO_AVAILABLE_TRANSITIONS)

        if next_state in states_keys:
            state_transition= states[next_state]
            transition_function = getattr(mitigation_action ,state_transition.method.__name__)

            if has_transition_perm(transition_function,user):
                transition_function()
                mitigation_action.save()
                result = (True, MitigationSerializer(mitigation_action).data)
            else: result = (False, self.INVALID_USER_TRANSITION)

        return result    







