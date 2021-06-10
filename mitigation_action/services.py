
from mitigation_action.workflow_steps.models import *
from mitigation_action.serializers import *
from mitigation_action.models import MitigationAction, Contact, Status, FinanceSourceType, FinanceStatus, \
    InitiativeType, GeographicScale, Finance, GHGInformation

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
        self.FUNCTION_INSTANCE_ERROR = 'Error Mitigation Action Service does not have {0} function'
        self.ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'
        self.LIST_ERROR = "Was expected a {0} list into data"

    
    # auxiliary functions
    def _create_sub_record(self, data, sub_record_name):
        
        create_function = f'_create_update_{sub_record_name}'

        if hasattr(self, create_function):
            function = getattr(self, create_function)
            record_status, record_detail = function(data=data)
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(create_function))

        return result


    def _update_sub_record(self, sub_record_name, record_for_updating, data):
        
        update_function = f'_create_update_{sub_record_name}'
        
        if hasattr(self, update_function):
          
            function = getattr(self, update_function)
        
            record_status, record_detail = function(data, record_for_updating)
          
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(update_function))

        return result


    def _create_or_update_record(self, instance, field, data):

        result = (False, [])
        if hasattr(instance, field):
            if getattr(instance, field) == None:
                record_status, record_data = self._create_sub_record(data, field) ## field = sub_record_name

            else:
                ## change field(string) to object(model instance)
                record_for_updating = getattr(instance, field) 
                record_status, record_data = self._update_sub_record(field, record_for_updating, data)
            
            result = (record_status, record_data)
        else:

            result = (False, self.ATTRIBUTE_INSTANCE_ERROR)

        return result


    ## serializers
    def _get_serialized_contact(self, data, contact = False):

        serializer = self._serialize_helper.get_serialized_record(ContactSerializer, data, record=contact)

        return serializer
    

    def _get_serialized_ghg_information(self, data, ghg_information = False):

        serializer = self._serialize_helper.get_serialized_record(GHGInformationSerializer, data, record=ghg_information)

        return serializer


    def _get_serialized_finance(self, data, finance = False):

        serializer = self._serialize_helper.get_serialized_record(FinanceSerializer, data, record=finance)

        return serializer


    def _get_serialized_status_information(self, data, status_information = False):

        serializer = self._serialize_helper.get_serialized_record(MitigationActionStatusSerializer, data, record=status_information)

        return serializer

    
    def _get_serialized_geographic_location(self, data, geographic_location = False):

        serializer = self._serialize_helper.get_serialized_record(GeographicLocationSerializer, data, record=geographic_location)

        return serializer


    def _get_serialized_mitigation_action(self, data, mitigation_action = False):

        serializer = self._serialize_helper.get_serialized_record(MitigationActionSerializer, data, record=mitigation_action)

        return serializer


    def _get_serialized_initiative(self, data, initiative = False):
        
        serializer = self._serialize_helper.get_serialized_record(InitiativeSerializer, data, record=initiative)

        return serializer


    def _get_serialized_impact_documentation(self, data, impact_documentation = False):
        
        serializer = self._serialize_helper.get_serialized_record(ImpactDocumentationSerializer, data, record=impact_documentation)

        return serializer


    def _get_serialized_monitoring_information(self, data, monitoring_information = False):
        
        serializer = self._serialize_helper.get_serialized_record(MonitoringInformationSerializer, data, record=monitoring_information)

        return serializer


    def _get_serialized_initiative_goal(self, data, initiative_goal=False):
        
        serializer = self._serialize_helper.get_serialized_record(InitiativeGoalSerializer, data, record=initiative_goal)

        return serializer


    def _get_serialized_initiative_goal_list(self, data, initiative_goal_list, initiative_id):
        
        data = [{**initiative_goal, 'initiative': initiative_id}  for initiative_goal in data ]
 
        serializer = self._serialize_helper.get_serialized_record(InitiativeGoalSerializer, data, record=initiative_goal_list, many=True,  partial=True)

        return serializer


    def _get_serialized_question_list(self, data, question_list, impact_documentation_id):
        
        data = [{**question, 'impact_documentation': impact_documentation_id}  for question in data ]
 
        serializer = self._serialize_helper.get_serialized_record(QAQCReductionEstimateQuestionSerializer, data, record=question_list, many=True,  partial=True)

        return serializer

    
    def _get_serialized_indicator_list(self, data, indicator_list, monitoring_information_id):
        
        data = [{**indicator, 'monitoring_information': monitoring_information_id}  for indicator in data ]
 
        serializer = self._serialize_helper.get_serialized_record(IndicatorSerializer, data, record=indicator_list, many=True,  partial=True)

        return serializer


    ## update and create function
    def _create_update_contact(self, data, contact=False):
        
        if contact:
            serialized_contact = self._get_serialized_contact(data, contact)

        else:
            serialized_contact = self._get_serialized_contact(data)
        
        if serialized_contact.is_valid():
            contact = serialized_contact.save()
            result = (True, contact)

        else:
            result = (False, serialized_contact.errors)

        return result
    

    ## update and create function

    def _create_update_ghg_information(self, data, ghg_information=False):
        
        if ghg_information:
            serialized_ghg_information= self._get_serialized_ghg_information(data, ghg_information)

        else:
            serialized_ghg_information = self._get_serialized_ghg_information(data)
        
        if serialized_ghg_information.is_valid():
            ghg_information = serialized_ghg_information.save()
            result = (True, ghg_information)

        else:
            result = (False, serialized_ghg_information.errors)

        return result


    def _create_update_finance(self, data, finance=False):
        
        if finance:
            serialized_finance = self._get_serialized_finance(data, finance)

        else:
            serialized_finance = self._get_serialized_finance(data)
        
        if serialized_finance.is_valid():
            finance = serialized_finance.save()
            result = (True, finance)

        else:
            result = (False, serialized_finance.errors)

        return result

    
    def _create_update_geographic_location(self, data, geographic_location=False):
        
        if geographic_location:
            serialized_geographic_location = self._get_serialized_geographic_location(data, geographic_location)

        else:
            serialized_geographic_location = self._get_serialized_geographic_location(data)

        if serialized_geographic_location.is_valid():
            geographic_location = serialized_geographic_location.save()
            result = (True, geographic_location)

        else:
            result = (False, serialized_geographic_location.errors)

        return result


    def _create_update_status_information(self, data, status_information=False):
        
        if status_information:
            serialized_status_information = self._get_serialized_status_information(data, status_information)

        else:
            serialized_status_information = self._get_serialized_status_information(data)
        
        if serialized_status_information.is_valid():
            status_information = serialized_status_information.save()
            result = (True, status_information)

        else:
            result = (False, serialized_status_information.errors)

        return result


    def _create_update_initiative_goal(self, data, initiative):
 
        result = (True, [])
        
        if isinstance(data, list):
            initiative_goal_list = initiative.goal.all() 
            serializer = self._get_serialized_initiative_goal_list(data, initiative_goal_list, initiative.id)
            
            if serializer.is_valid():
                
                serializer.save()

            else: 
                result = (False, serializer.errors)

        else:
            result = (False, self.LIST_ERROR.format('goal'))
            
        return result
    

    def _create_update_question(self, data, impact_documentation):
 
        result = (True, [])
        
        if isinstance(data, list):
            question_list = impact_documentation.question.all() 
            serializer = self._get_serialized_question_list(data, question_list, impact_documentation.id)
            
            if serializer.is_valid():
                
                question = serializer.save()

                result = (True, question)

            else: 
                result = (False, serializer.errors)

        else:
            result = (False, self.LIST_ERROR.format('question'))
            
        return result

    
    def _create_update_indicator(self, data, monitoring_information):

        result = (True, [])
        
        if isinstance(data, list):
            indicator_list = monitoring_information.indicator.all() 
            serializer = self._get_serialized_indicator_list(data, indicator_list, monitoring_information.id)
            
            if serializer.is_valid():
                
                indicator = serializer.save()

                result = (True, indicator)

            else: 
                result = (False, serializer.errors)

        else:
            result = (False, self.LIST_ERROR.format('indicator'))
            
        return result
    

    def _create_update_initiative(self, data, initiative=False):
        
        validation_dict = {}
        if initiative:
            serialized_initiative= self._get_serialized_initiative(data, initiative)
        
        else:
            serialized_initiative = self._get_serialized_initiative(data)

        if serialized_initiative.is_valid():

            initiative = serialized_initiative.save()

            goal_data = data.get("initiative_goal", [])
            serialized_goal_status, serialized_goal_data = self._create_update_initiative_goal(goal_data, initiative)

            if serialized_goal_status:
                result = (True, initiative)
            else:
                result = (serialized_goal_status, serialized_goal_data )

        else:
            errors = serialized_initiative.errors
            result = (False, errors)


        return result


    def _create_update_impact_documentation(self, data, impact_documentation=False):
        
        validation_dict = {}
        if impact_documentation:
            serialized_impact_documentation = self._get_serialized_impact_documentation(data, impact_documentation)
        
        else:
            serialized_impact_documentation = self._get_serialized_impact_documentation(data)

        if serialized_impact_documentation.is_valid():

            impact_documentation = serialized_impact_documentation.save()

            question_data = data.get("question", [])
            serialized_question_status, serialized_question_data = self._create_update_question(question_data, impact_documentation)

            if serialized_question_status:
                result = (True, impact_documentation)

            else:
                result = (serialized_question_status, serialized_question_data )

        else:
            errors = serialized_impact_documentation.errors
            result = (False, errors)


        return result
    

    def _create_update_monitoring_information(self, data, monitoring_information=False):
        
        if monitoring_information:
            serialized_monitoring_information = self._get_serialized_monitoring_information(data, monitoring_information)
        
        else:
            serialized_monitoring_information = self._get_serialized_monitoring_information(data)

        if serialized_monitoring_information.is_valid():

            monitoring_information = serialized_monitoring_information.save()

            indicator_data = data.get("indicator", [])
            serialized_indicator_status, serialized_indicator_data = self._create_update_indicator(indicator_data, monitoring_information)

            if serialized_indicator_status:
                result = (True, monitoring_information)

            else:
                result = (serialized_indicator_status, serialized_indicator_data )

        else:
            errors = serialized_monitoring_information.errors
            result = (False, errors)


        return result


    def get(self, request, mitigation_action_id):
        
        mitigation_action_status, mitigation_action_data = self._service_helper.get_one(MitigationAction, mitigation_action_id)
        
        if mitigation_action_status:
            result = (mitigation_action_status, MitigationActionSerializer(mitigation_action_data).data)
        
        else:
            result = (mitigation_action_status, mitigation_action_data) 

        return result
    

    def get_all(self, request):

        mitigation_action_status, mitigation_action_data = self._service_helper.get_all(MitigationAction)

        if mitigation_action_status:
            result = (mitigation_action_status, MitigationActionSerializer(mitigation_action_data, many=True).data)
        
        else:
            result = (mitigation_action_status, mitigation_action_data) 

        return result


    def create(self, request):

        errors =[]
        validation_dict = {}
        data = request.data.copy()
        data['user'] = request.user.id

        # fk's of object mitigation_action that have nested fields
        field_list = ['contact', 'status_information', 'geographic_location', 'initiative', 'finance',  
            'ghg_information', 'impact_documentation', 'monitoring_information']

        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field)

                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)
        
        if all(validation_dict):
            serialized_mitigation_action = self._get_serialized_mitigation_action(data)
            if serialized_mitigation_action.is_valid():
                mitigation_action = serialized_mitigation_action.save()
                
                result = (True, MitigationActionSerializer(mitigation_action).data)
  
            else:
                errors.append(serialized_mitigation_action.errors)
                result = (False, errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result
    

    def update(self, request, mitigation_action_id):

        validation_dict = {}
        data = request.data.copy()
        data['user'] = request.user.id

        field_list = ['contact', 'status_information', 'geographic_location', 'initiative', 'finance', 
                        'ghg_information', 'impact_documentation', 'monitoring_information'] 

        mitigation_action_status, mitigation_action_data = \
            self._service_helper.get_one(MitigationAction, mitigation_action_id)
        
        if mitigation_action_status:
            mitigation_action = mitigation_action_data
             # fk's of object mitigation that have nested fields
            for field in field_list:
                if data.get(field, False):
                    record_status, record_data = self._create_or_update_record(mitigation_action, field, data.get(field))
                    
                    if record_status:
                        data[field] = record_data.id
                        
                    dict_data = record_data if isinstance(record_data, list) else [record_data]
                    validation_dict.setdefault(record_status,[]).extend(dict_data)

            if all(validation_dict):
                serialized_mitigation_action = self._get_serialized_mitigation_action(data, mitigation_action)
                
                if serialized_mitigation_action.is_valid():
                    mitigation_action = serialized_mitigation_action.save()
                    result = (True, MitigationActionSerializer(mitigation_action).data)

                else:
                    result = (False, serialized_mitigation_action.errors)
            else:
                result = (False, validation_dict.get(False))
        else:
            result = (mitigation_action_status, mitigation_action_data)


        return result


    def get_catalog_data(self, request):
        
        catalog = {
            
            'initiative_type': (InitiativeType, InitiativeTypeSerializer),
            'status': (Status, StatusSerializer),
            'finance_source_type': (FinanceSourceType, FinanceSourceTypeSerializer),
            'finance_status': (FinanceStatus, FinanceStatusSerializer),
            'geographic_scale': (GeographicScale, GeographicScaleSerializer)
        }

        data = {}

        for name , (_model, _serializer) in catalog.items():
            result_status, result_data = self._service_helper.get_all(_model)

            if not result_status:
                result = (False, result_data)
                return result
            
            data = {**data, **{name: _serializer(result_data, many=True).data}}
        
        result = (True, data)
        
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
                result = (True, MitigationActionSerializer(mitigation_action).data)
            else: result = (False, self.INVALID_USER_TRANSITION)

        return result    







