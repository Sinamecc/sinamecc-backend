
from functools import partial
from mitigation_action.workflow_steps.models import *
from mitigation_action.serializers import *
from mitigation_action.models import MitigationAction, Contact, Status, FinanceSourceType, FinanceStatus, \
    InitiativeType, GeographicScale, Finance, GHGInformation, ActionAreas, DescarbonizationAxis,Topics, \
    ImpactCategory, SustainableDevelopmentGoals, GHGImpactSector, Classifier, ThematicCategorizationType, InformationSourceType

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
        self.MITIGATION_ACTION_NO_INDICATOR = 'Mitigation action {0} does not have indicators related'
        self.SECTION_MODEL_DOES_NOT_EXIST = 'Section Model does not exist {0}'
        self.CATALOG_DOES_NOT_EXIST = "The catalog does not exist:  {0} --> {1}"
        self.INDICATOR_CHANGE_LOG_ERROR = "Error creating indicator change log"
        self.INDICATOR_NOT_FOUND = "The indicator with ID {0} does not exist"
        self.INDICATOR_ERROR = "The  indicator could not be saved"


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
    
    def _get_serialized_indicator_change_log(self, data, indicator_change_log=None, partial=None):
        
        serializer = self._serialize_helper.get_serialized_record(IndicatorChangeLogSerializer, data, record=indicator_change_log, partial=partial)

        return serializer
    
    def _get_serialized_information_source(self, data, information_source=None, partial=None):

        serializer = self._serialize_helper.get_serialized_record(InformationSourceSerializer, data, record=information_source, partial=True)

        return serializer
    

    def _get_serialized_ghg_information(self, data, ghg_information = False, partial=False):

        serializer = self._serialize_helper.get_serialized_record(GHGInformationSerializer, data, record=ghg_information, partial=partial)

        return serializer


    def _get_serialized_finance(self, data, finance = False):

        serializer = self._serialize_helper.get_serialized_record(FinanceSerializer, data, record=finance)

        return serializer


    def _get_serialized_status_information(self, data, status_information = False):

        serializer = self._serialize_helper.get_serialized_record(MitigationActionStatusSerializer, data, record=status_information)

        return serializer

    
    def _get_serialized_geographic_location(self, data, geographic_location = False, partial=False):

        serializer = self._serialize_helper.get_serialized_record(GeographicLocationSerializer, data, record=geographic_location, partial=partial)

        return serializer


    def _get_serialized_mitigation_action(self, data, mitigation_action = False):

        serializer = self._serialize_helper.get_serialized_record(MitigationActionSerializer, data, record=mitigation_action)

        return serializer


    def _get_serialized_initiative(self, data, initiative = False,  partial=False):
        
        serializer = self._serialize_helper.get_serialized_record(InitiativeSerializer, data, record=initiative, partial=partial)

        return serializer


    def _get_serialized_impact_documentation(self, data, impact_documentation = False, partial=False):
        
        serializer = self._serialize_helper.get_serialized_record(ImpactDocumentationSerializer, data, record=impact_documentation, partial=partial)

        return serializer


    def _get_serialized_monitoring_reporting_indicator(self, data, monitoring_reporting_indicator = False):
        
        serializer = self._serialize_helper.get_serialized_record(MonitoringReportingIndicatorSerializer, data, record=monitoring_reporting_indicator)

        return serializer


    def _get_serialized_monitoring_information(self, data, monitoring_information = False):
        
        serializer = self._serialize_helper.get_serialized_record(MonitoringInformationSerializer, data, record=monitoring_information)

        return serializer


    def _get_serialized_initiative_goal(self, data, initiative_goal=False):
        
        serializer = self._serialize_helper.get_serialized_record(InitiativeGoalSerializer, data, record=initiative_goal)

        return serializer


    def _get_serialized_categorization(self, data, categorization = False):
        
        serializer = self._serialize_helper.get_serialized_record(CategorizationSerializer, data, record=categorization, partial=True)

        return serializer
    
    def _get_serialized_indicator(self, data, indicator = False):
      
        serializer = self._serialize_helper.get_serialized_record(IndicatorSerializer, data, record=indicator, partial=True)

        return serializer


    def _get_serialized_initiative_goal_list(self, data, initiative_goal_list, initiative_id):
        
        data = [{**initiative_goal, 'initiative': initiative_id}  for initiative_goal in data ]
 
        serializer = self._serialize_helper.get_serialized_record(InitiativeGoalSerializer, data, record=initiative_goal_list, many=True,  partial=True)

        return serializer

    
    def _get_serialized_action_area_selection_list(self, data, action_area_selection_list, categorization_id):
        
        data = [{**action_area_selection, 'categorization': categorization_id}  for action_area_selection in data ]
        
        serializer = self._serialize_helper.get_serialized_record(ActionAreasSelectionSerializer, data, record=action_area_selection_list, many=True,  partial=True)
        
        return serializer
    

    def _get_serialized_question_list(self, data, question_list, impact_documentation_id):
        
        data = [{**question, 'impact_documentation': impact_documentation_id}  for question in data ]
 
        serializer = self._serialize_helper.get_serialized_record(QAQCReductionEstimateQuestionSerializer, data, record=question_list, many=True,  partial=True)

        return serializer

    
    def _get_serialized_finance_information_list(self, data, finance_information_list, finance_id):
        
        data = [{**finance_information, 'finance': finance_id}  for finance_information in data ]
 
        serializer = self._serialize_helper.get_serialized_record(FinanceInformationSerializer, data, record=finance_information_list, many=True,  partial=True)

        return serializer
    
    
    def _get_serialized_monitoring_indicator_list(self, data, monitoring_indicator_list, monitoring_reporting_indicator_id):
        
        data = [{**monitoring_indicator, 'monitoring_reporting_indicator': monitoring_reporting_indicator_id}  for monitoring_indicator in data ]
 
        serializer = self._serialize_helper.get_serialized_record(MonitoringIndicatorSerializer, data, record=monitoring_indicator_list, many=True,  partial=True)

        return serializer


    ## auxiliar function for create and update record
    def _get_indicators_for_updating_creating(self, indicator_list, indicator_data_list, monitoring_information):
        ## added object attribute if the indicator data has an indicator id
        for indicator_data in indicator_data_list:
            indicator_data_id = indicator_data.get('id', None)
            if indicator_data_id:
                obj = next(filter(lambda x: x.id == indicator_data_id, indicator_list), None)
                if obj: indicator_data['object'] = obj
                else:
                    result = (False, 'Indicator with id {} not found'.format(indicator_data_id))
            else:
                indicator_data['monitoring_information'] =  monitoring_information.id

        result = (True, indicator_data_list)

        return result        


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
    
    def _create_update_indicator_change_log(self, data, indicator_change_log=None):
        
        if indicator_change_log:
            serialized_indicator_change_log = self._get_serialized_indicator_change_log(data, indicator_change_log, partial=True)

        else:
            serialized_indicator_change_log = self._get_serialized_indicator_change_log(data, partial=True)
            
        if serialized_indicator_change_log.is_valid():

            indicator_change_log = serialized_indicator_change_log.save()
            result = (True, indicator_change_log)

        else:
            result = (False, serialized_indicator_change_log.errors)
            
        return result

    
    def _create_update_information_source(self, data, information_source=None):
        
        if information_source:
            serialized_information_source = self._get_serialized_information_source(data, information_source)
            
        else:
            serialized_information_source = self._get_serialized_information_source(data, partial=True)
        
        if serialized_information_source.is_valid():
            information_source = serialized_information_source.save()
            result = (True, information_source)

        else:
            result = (False, serialized_information_source.errors)

        return result

    def _create_update_ghg_information(self, data, ghg_information=None):
        
        if ghg_information:
            serialized_ghg_information = self._get_serialized_ghg_information(data, ghg_information)

        else:
            serialized_ghg_information = self._get_serialized_ghg_information(data)
        
        if serialized_ghg_information.is_valid():
            ghg_information = serialized_ghg_information.save()
            result = (True, ghg_information)

        else:
            result = (False, serialized_ghg_information.errors)

        return result

    

    ## update and create function

    def _create_update_ghg_information(self, data, ghg_information=False):
        
        if ghg_information:
            serialized_ghg_information= self._get_serialized_ghg_information(data, ghg_information, partial=True)

        else:
            serialized_ghg_information = self._get_serialized_ghg_information(data, partial=True)
        
        
        if serialized_ghg_information.is_valid():
            ghg_information = serialized_ghg_information.save()
            result = (True, ghg_information)

        else:
            result = (False, serialized_ghg_information.errors)

        return result


    def _create_update_finance(self, data, finance=None):
        
        if finance:
            serialized_finance = self._get_serialized_finance(data, finance)

        else:
            serialized_finance = self._get_serialized_finance(data)
        
        if serialized_finance.is_valid():
            finance = serialized_finance.save()
            finance_information_data = data.get("finance_information", [])
            serialized_fi_status, serialized_fi_data = self._create_update_finance_information(finance_information_data, finance)

            if serialized_fi_status:
                result = (True, finance)
            else:
                result = (serialized_fi_status, serialized_fi_data)


        else:
            result = (False, serialized_finance.errors)

        return result

    
    def _create_update_geographic_location(self, data, geographic_location=False):
        
        if geographic_location:
            serialized_geographic_location = self._get_serialized_geographic_location(data, geographic_location, partial=True)

        else:
            serialized_geographic_location = self._get_serialized_geographic_location(data, partial=True)

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

    
    
    
    def _create_update_categorization(self, data, categorization=False):
        
        action_area_selection = data.pop('action_area_selection', [])
        topic_selection = data.pop('topic_selection', [])
        
        if categorization:
            serialized_categorization = self._get_serialized_categorization(data, categorization)

        else:
            serialized_categorization = self._get_serialized_categorization(data)
        
        if serialized_categorization.is_valid():
            categorization = serialized_categorization.save()
            serialized_action_area_selection_status, serialized_action_area_selection_data = self._create_update_action_area_selection(action_area_selection, categorization)
            ## review this topic_selection

            if serialized_action_area_selection_status:
                result = (True, categorization)
            else:
                result = (serialized_action_area_selection_status, serialized_action_area_selection_data)

        else:
            result = (False, serialized_categorization.errors)

        return result

    
    def _create_update_action_area_selection(self, data, categorization):
 
        result = (True, [])
        
        if isinstance(data, list):
            action_area_selection_list = categorization.action_area_selection.all() 
            serializer = self._get_serialized_action_area_selection_list(data, action_area_selection_list, categorization.id)
            
            if serializer.is_valid():
                
                serializer.save()
                result = (True, categorization)
                
            else: 
                result = (False, serializer.errors)

        else:
            result = (False, self.LIST_ERROR.format('action_area_selection'))
            
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
    
    
    def _create_update_finance_information(self, data, finance):
 
        result = (True, [])
        
        if isinstance(data, list):
            finance_information_list = finance.finance_information.all() 
            serializer = self._get_serialized_finance_information_list(data, finance_information_list, finance.id)
            
            if serializer.is_valid():
                
                serializer.save()
                result = (True, serializer.data)
            else: 
                result = (False, serializer.errors)

        else:
            result = (False, self.LIST_ERROR.format('Finance Information'))
            
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

    
    def _create_update_indicator_list(self, data, monitoring_information):

        indicator_list = monitoring_information.indicator.all()

        ## in this part we are going to get the indicators to update or create
        ## retrun the object to update into the json data -->[ {'id': 2, ..., 'object': <indicator_obj_from_DB_with_id_2> }, {...}, ... ]
        ## and if the indicator json data has not id, we are going to create it , not update it
        indicator_list_status, indicator_list_data = self._get_indicators_for_updating_creating(indicator_list, data, monitoring_information)
        indicator_list = []
        if indicator_list_status:
            for indicator_data in indicator_list_data:
                indicator = indicator_data.pop('object', None)
                indicator_status, indicator_data = self._create_update_indicator(indicator_data, indicator)
                if not indicator_status:
                    result = (indicator_status, indicator_data) 
                    break
                indicator_list.append(indicator_data)

            else:
                result = (True, indicator_list)

        else:
            result = (False, indicator_list_data)
        
        return result

        


    def _create_update_monitoring_indicator(self, data, monitoring_reporting_indicator):

        result = (True, [])
        
        if isinstance(data, list):
            monitoring_indicator_list = monitoring_reporting_indicator.monitoring_indicator.all()
            serializer = self._get_serialized_monitoring_indicator_list(data, monitoring_indicator_list, monitoring_reporting_indicator.id)
            
            if serializer.is_valid():
                monitoring_indicator = serializer.save()

                result = (True, monitoring_indicator)

            else: 
                result = (False, serializer.errors)

        else:
            result = (False, self.LIST_ERROR.format('monitoring_indicator'))
            
        return result
    

    def _create_update_initiative(self, data, initiative=False):
        
        validation_dict = {}
        if initiative:
            serialized_initiative= self._get_serialized_initiative(data, initiative, partial=True)
        
        else:
            serialized_initiative = self._get_serialized_initiative(data, partial=True)

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
            serialized_impact_documentation = self._get_serialized_impact_documentation(data, impact_documentation, partial=True)
        
        else:
            serialized_impact_documentation = self._get_serialized_impact_documentation(data, partial=True)

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
            serialized_indicator_status, serialized_indicator_data = self._create_update_indicator_list(indicator_data, monitoring_information)

            if serialized_indicator_status:
                result = (True, monitoring_information)

            else:
                result = (serialized_indicator_status, serialized_indicator_data )

        else:
            errors = serialized_monitoring_information.errors
            result = (False, errors)


        return result

    
    def _create_update_monitoring_reporting_indicator(self, data, monitoring_reporting_indicator=False):
        
        if monitoring_reporting_indicator:
            serialized_monitoring_reporting_indicator = self._get_serialized_monitoring_reporting_indicator(data, monitoring_reporting_indicator)
        
        else:
            serialized_monitoring_reporting_indicator = self._get_serialized_monitoring_reporting_indicator(data)

        if serialized_monitoring_reporting_indicator.is_valid():

            monitoring_reporting_indicator = serialized_monitoring_reporting_indicator.save()

            monitoring_indicator_data = data.get("monitoring_indicator", [])
            serialized_monitoring_indicator_status, serialized_monitoring_indicator_data = self._create_update_monitoring_indicator(monitoring_indicator_data, monitoring_reporting_indicator)

            if serialized_monitoring_indicator_status:
                result = (True, monitoring_reporting_indicator)

            else:
                result = (serialized_monitoring_indicator_status, serialized_monitoring_indicator_data)

        else:
            errors = serialized_monitoring_reporting_indicator.errors
            result = (False, errors)


        return result

    def _create_update_indicator_from_validation_dict(self, data, indicator=None):

        change_log = data.get('change_log', None)

        serialized_indicator = self._get_serialized_indicator(data, indicator)
        if serialized_indicator.is_valid():
            indicator = serialized_indicator.save()
            if change_log:
                change_log['indicator'] = indicator.id
                change_log_status, change_log_data = self._create_update_indicator_change_log(change_log)
                if change_log_status:
                    indicator.indicator_change_log.add(change_log_data)
                    indicator.save()
                    result = (True, indicator)

                else:
                    result = (change_log_status, change_log_data)
            else:
                result = (False, self.INDICATOR_CHANGE_LOG_ERROR)

        else:
            result = (False, serialized_indicator.errors)
        
        return result


    def _create_update_indicator(self, data, indicator=None):

        validation_dict = {}
        field_list = ['contact', 'information_source'] 
        try:
            for field in field_list:
                if data.get(field, False):
                    record_status, record_data = self._create_sub_record(data.get(field), field) if not indicator \
                                                else self._create_or_update_record(indicator, field, data.get(field))
                    if record_status:
                        data[field] = record_data.id
                        
                    dict_data = record_data if isinstance(record_data, list) else [record_data]
                    validation_dict.setdefault(record_status,[]).extend(dict_data)

            if all(validation_dict):
                indicator_status, indicator_data = self._create_update_indicator_from_validation_dict(data, indicator)
                result = ( indicator_status, indicator_data)

            else:
                result = (False, validation_dict.get(False))
        
        ## we need to define a specific error message for this
        except Exception as e:
            result = (False, self.INDICATOR_ERROR)
        
        finally:

            return result


    ## helpers functions for uploading files
    #     
    def _upload_file_to_initiative(self, data, mitigation_action):
        ## This function uploads to description files to the initiative
        file_data = {"description_file": data.get("file", None)}

        initiative = mitigation_action.initiative
        initiative_status, initiative_data = self._create_update_initiative(file_data, initiative) 

        if initiative_status:

            if initiative == None:
                mitigation_action.initiative = initiative_data
                mitigation_action.save()

            result = (True, mitigation_action)

        else:
            result = (initiative_status, initiative_data)

        return result
    

    def _upload_file_to_geographic_location(self, data, mitigation_action):
        ## This function uploads to location_file to the geographic location
        file_data = {"location_file": data.get("file", None)}

        geographic_location = mitigation_action.geographic_location
        geographic_location_status, geographic_location_data = self._create_update_geographic_location(file_data, geographic_location) 

        if geographic_location_status:

            if geographic_location == None:
                mitigation_action.geographic_location = geographic_location_data
                mitigation_action.save()

            result = (True, mitigation_action)

        else:
            result = (geographic_location_status, geographic_location_data)

        return result


    def _upload_file_to_ghg_information(self, data, mitigation_action):

        ## This function uploads to graphic_description_file to the ghg information
        file_data = {"graphic_description_file": data.get("file", None)}

        ghg_information = mitigation_action.ghg_information
        ghg_information_status, ghg_information_data = self._create_update_ghg_information(file_data, ghg_information)

        if ghg_information_status:
            if ghg_information == None:
                mitigation_action.ghg_information = ghg_information_data
                mitigation_action.save()
            result = (True, mitigation_action)
        
        else:
            result = (ghg_information_status, ghg_information_data)
            
        return result
    
    def _upload_file_to_impact_documentation(self, data, mitigation_action):
        ## This function uploads to estimate_calculation_documentation_file to the impact documentation
        file_data = {"estimate_calculation_documentation_file": data.get("file", None)}

        impact_documentation = mitigation_action.impact_documentation
        impact_documentation_status, impact_documentation_data = self._create_update_impact_documentation(file_data, impact_documentation)

        if impact_documentation_status:
            if impact_documentation == None:
                mitigation_action.impact_documentation = impact_documentation_data
                mitigation_action.save()
            result = (True, mitigation_action)
        
        else:
            result = (impact_documentation_status, impact_documentation_data)
            
        return result
        


    ## upload files in the models
    def upload_file_from_mitigation_action(self, request, mitigation_action_id, model_type):

        model_type_options = {
            'initiative': self._upload_file_to_initiative, 
            'geographic-location': self._upload_file_to_geographic_location,
            'ghg-information': self._upload_file_to_ghg_information,
            'impact-documentation': self._upload_file_to_impact_documentation
        }    
    
        data = request.data

        mitigation_action_status, mitigation_action_data = self._service_helper.get_one(MitigationAction, mitigation_action_id)

        if mitigation_action_status:
            method = model_type_options.get(model_type, False)
            
            if method:
                response_status, response_data = method(data, mitigation_action_data)
                
                if response_status:
                    result = (response_status, MitigationActionSerializer(mitigation_action_data).data)
                    
                else:
                    result = (response_status, response_data)

            else:
                result = (False, self.SECTION_MODEL_DOES_NOT_EXIST.format(model_type))

        else:
            result = (mitigation_action_status, mitigation_action_data)
        
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
        field_list = ['contact', 'status_information', 'geographic_location', 'initiative', 'finance', 'categorization', 
            'ghg_information', 'impact_documentation', 'monitoring_information', 'monitoring_reporting_indicator']

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
                mitigation_action.create_code()    
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

        field_list = ['contact', 'status_information', 'geographic_location', 'initiative', 'finance', 'categorization',
                        'ghg_information', 'impact_documentation', 'monitoring_information', 'monitoring_reporting_indicator'] 

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


    def get_indicator_from_mitigation_action(self, request, mitigation_action_id):

        mitigation_action_status, mitigation_action_data = self._service_helper.get_one(MitigationAction, mitigation_action_id)
        
        if mitigation_action_status:
            monitoring_information = mitigation_action_data.monitoring_information
            
            if monitoring_information:
                indicator_list = monitoring_information.indicator.all()
                result = (True, IndicatorSerializer(indicator_list, many=True).data)

            else:
                result = (False, self.MITIGATION_ACTION_NO_INDICATOR.format(mitigation_action_data.id))
        
        else:
            result = (mitigation_action_status, mitigation_action_data)

        return result

    def delete_indicator_from_mitigation_action(self, request, mitigation_action_id, indicator_id):

        mitigation_action_status, mitigation_action_data = self._service_helper.get_one(MitigationAction, mitigation_action_id)
        result = (False, self.INDICATOR_NOT_FOUND.format(indicator_id))
        if mitigation_action_status:
            monitoring_information = mitigation_action_data.monitoring_information
            
            if monitoring_information:
                indicator_list = monitoring_information.indicator.filter(id=indicator_id)
                if indicator_list:
                    indicator = indicator_list.first()
                    indicator.delete()
                    result = (True, {"id": indicator_id})
                else:
                    result = (False, self.INDICATOR_NOT_FOUND.format(indicator_id))

            else:
                result = (False, self.MITIGATION_ACTION_NO_INDICATOR.format(mitigation_action_data.id))
        
        else:
            result = (mitigation_action_status, mitigation_action_data)

        return result





    def get_catalog_data(self, request):
        
        catalog = {

            'initiative_type': (InitiativeType, InitiativeTypeSerializer),
            'status': (Status, StatusSerializer),
            'finance_source_type': (FinanceSourceType, FinanceSourceTypeSerializer),
            'finance_status': (FinanceStatus, FinanceStatusSerializer),
            'geographic_scale': (GeographicScale, GeographicScaleSerializer),
            'action_areas': (ActionAreas, ActionAreasSerializer),
            'descarbonization_axis': (DescarbonizationAxis, DescarbonizationAxisSerializer),
            'topics': (Topics, TopicsSerializer),
            'impact_category': (ImpactCategory, ImpactCategorySerializer),
            'sustainable_development_goals': (SustainableDevelopmentGoals, SustainableDevelopmentGoalsSerializer),
            'ghg_impact_sector': (GHGImpactSector, GHGImpactSectorSerializer),
            'carbon_deposit': (CarbonDeposit, CarbonDepositSerializer),
            'standard': (Standard, StandardSerializer),
            'classifier': (Classifier, ClassifierSerializer),
            'information_source_type': (InformationSourceType, InformationSourceTypeSerializer),
            'thematic_categorization_type': (ThematicCategorizationType, ThematicCategorizationTypeSerializer),
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

    
    def  get_child_data_from_parent_id_catalogs(self, request, parent, parent_id, child):

        catalogs_by_parent = {
            'action-areas':{'action-goal': (ActionGoals, ActionGoalsSerializer, 'area')},
            'descarbonization-axis':{'transformational-visions': (TransformationalVisions, TransformationalVisionsSerializer, 'axis')},
            'topics': {'sub-topics': (SubTopics, SubTopicsSerializer, 'topic')},
            'sub-topics':{'activities': (Activity, ActivitySerializer, 'sub_topic')},
        }
        result = (False, self.CATALOG_DOES_NOT_EXIST.format(parent, child))

        if catalogs_by_parent.get(parent, None):
            child_data_class = catalogs_by_parent.get(parent)
            child_model, child_serializer, field_parent_search = child_data_class.get(child, (None, None, None))

            if child_model:
                filter_query = {field_parent_search: parent_id}
                catalog_status, catalog_data = self._service_helper.get_all(child_model, **filter_query)
                
                result = (catalog_status, child_serializer(catalog_data, many=True).data) if catalog_status else (catalog_status, catalog_data)
            
            else:
                result = (False, self.CATALOG_DOES_NOT_EXIST.format(parent, child))

        else:
            result = (False, self.CATALOG_DOES_NOT_EXIST.format(parent, child))
        
        return result


    def update_fsm_state(self, next_state, mitigation_action, user):

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

    
    def sent_to_review(self, request, mitigation_action_id):
        
        mitigation_action_status, mitigation_action_data = self._service_helper.get_one(MitigationAction, mitigation_action_id)
        SUBMITTED_STATE = 'submitted'
        if mitigation_action_status:
            user = request.user
            result = self.update_fsm_state(SUBMITTED_STATE, mitigation_action_data, user)
        
        else:
            result = (mitigation_action_status, mitigation_action_data)
        
        return result







