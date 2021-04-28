
from mitigation_action.workflow_steps.models import *
from workflow.models import ReviewStatus
from general.storages import S3Storage
from rest_framework.parsers import JSONParser
from django_fsm import can_proceed,has_transition_perm
from mitigation_action.serializers import MitigationSerializer
import datetime
import uuid
from io import BytesIO
from django.urls import reverse
import os
from general.services import HandlerErrors
from workflow.services import WorkflowService
from general.services import EmailServices
handler = HandlerErrors()
workflow_service = WorkflowService()


class MitigationActionService():
    
    def __init__(self):
        self.storage = S3Storage()


    def get_catalog_data(self, request):
    
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







