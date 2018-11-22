from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, FinanceSourceType, Finance, \
IngeiCompliance, GeographicScale, Location, Mitigation, ChangeLog, Initiative, InitiativeType, FinanceStatus, InitiativeFinance
from mitigation_action.workflow_steps.models import * 
from mitigation_action.serializers import InitiaveSerializer, InitiativeFinanceSerializer, FinanceSerializer, LocationSerializer, ProgressIndicatorSerializer, ContactSerializer, MitigationSerializer, ChangeLogSerializer
from workflow.models import ReviewStatus
from general.storages import S3Storage
from rest_framework.parsers import JSONParser
from django_fsm import can_proceed
import datetime
import uuid
from io import BytesIO
from django.urls import reverse
import os

from workflow.services import WorkflowService
from general.services import EmailServices

workflow_service = WorkflowService()


class MitigationActionService():
    def __init__(self):
        self.storage = S3Storage()
        self.MITIGATION_ACTION_DOES_NOT_EXIST = "Mitigation Action does not exist."
        self.MITIGATION_ACTION_ERROR_GET_ALL = "Error retrieving all Mitigation Action records."
        self.INGEI_COMPLIANCE_DOES_NOT_EXIST = "INGEI compliance does not exist."
        self.COMMENT_NOT_ASSIGNED = "The provided comment could not be assigned correctly."
        self.NO_PATCH_DATA_PROVIDED = "No PATCH data provided."
        self.CHANGE_LOG_DOES_NOT_EXIST = "Mitigation Action change log does not exist."
        self.INVALID_STATUS_TRANSITION = "Invalid mitigation action state transition."
        self.MITIGATION_ACTION_NOT_INSERTED = "Mitigation action cannot be inserted"
        self.INITIATIVE_RELATIONS = "contact_id or finance_id is not related with initiative"
        self.RELATED_MITIGATION_ACTION = " is not related with MA"

    def get_all(self, language):
        try:
            mitigations_list = [
                {
                    'id': m.id,
                    'strategy_name': m.strategy_name,
                    'name': m.name,
                    'purpose': m.purpose,
                    'quantitative_purpose': m.quantitative_purpose,
                    'start_date': m.start_date,
                    'end_date': m.end_date,
                    'gas_inventory': m.gas_inventory,
                    'emissions_source': m.emissions_source,
                    'carbon_sinks': m.carbon_sinks,
                    'impact_plan': m.impact_plan,
                    'impact': m.impact,
                    'bibliographic_sources': m.bibliographic_sources,
                    'is_international': m.is_international,
                    'international_participation': m.international_participation,
                    'sustainability': m.sustainability,
                    'question_ucc': m.question_ucc,
                    'question_ovv': m.question_ovv,
                    'user': {
                        'id': m.user.id,
                        'username': m.user.username,
                        'email': m.user.email
                    },
                    'initiative':{
                        'id' : m.initiative.id,
                        'name': m.initiative.name,
                        'objective' : m.initiative.objective,
                        'description': m.initiative.description,
                        'goal' : m.initiative.goal,
                        'initiative_type': {
                            "id": m.initiative.initiative_type.id,
                            "initiative_type" : m.initiative.initiative_type.initiative_type_es if language=="es" else m.initiative.initiative_type.initiative_type_en
                            },
                        'entity_responsible': m.initiative.entity_responsible,
                        'budget': m.initiative.budget,
                        'status' : {
                            'id': m.initiative.status.id,
                            'status': m.initiative.status.status_es if language=="es" else m.initiative.status.status_en
                        },
                        'contact': {
                            'id': m.initiative.contact.id,
                            'full_name': m.initiative.contact.full_name,
                            'job_title': m.initiative.contact.job_title,
                            'email': m.initiative.contact.email,
                            'phone': m.initiative.contact.phone
                        },

                        'finance': {
                            'id': m.initiative.finance.id,
                            'finance_source_type': {
                                'id': m.initiative.finance.finance_source_type.id,
                                'name': m.initiative.finance.finance_source_type.name_es if language=="es" else m.initiative.finance.finance_source_type.name_en,
                            },
                            'status':{
                                'id' : m.initiative.finance.status.id,
                                'name' : m.initiative.finance.status.name_es if language=="es" else m.initiative.finance.status.name_en
                            } 
                        },
                    } if m.initiative else {},
                    'registration_type': {
                        'id': m.registration_type.id,
                        'type': m.registration_type.type_es if language=="es" else m.registration_type.type_en,
                    } if m.registration_type else {},
                    'institution': {
                        'id': m.institution.id,
                        'name': m.institution.name
                    } if m.institution else {},
                    'contact': {
                        'id': m.contact.id,
                        'full_name': m.contact.full_name,
                        'job_title': m.contact.job_title,
                        'email': m.contact.email,
                        'phone': m.contact.phone
                    } if m.contact else {},
                    'status': {
                        'id': m.status.id,
                        'status': m.status.status_es if language=="es" else m.status.status_en
                    } if m.status else {},
                    'progress_indicator': {
                        'id': m.progress_indicator.id,
                        'name': m.progress_indicator.name,
                        'type': m.progress_indicator.type,
                        'unit': m.progress_indicator.unit,
                        'start_date': m.progress_indicator.start_date
                    } if m.progress_indicator else {},
                    'finance': {
                        'id': m.finance.id,
                        'status':{
                                'id' : m.finance.status.id,
                                'name' : m.finance.status.name_es if language=="es" else m.initiative.finance.status.name_en
                            },
                        'source': m.finance.source

                    } if m.finance else {},
                    'ingei_compliances': [
                        {
                            'id': ingei.id,
                            'name': ingei.name_es if language=="es" else ingei.name_en,
                        } for ingei in m.ingei_compliances.all()
                    ],
                    'geographic_scale': {
                        'id': m.geographic_scale.id,
                        'name': m.geographic_scale.name_es if language=="es" else m.geographic_scale.name_en
                    } if m.geographic_scale else {},
                    'location': {
                        'id': m.location.id,
                        'geographical_site': m.location.geographical_site,
                        'is_gis_annexed': m.location.is_gis_annexed
                    } if m.location else {},
                    # Workflow
                    'review_count': m.review_count,
                    'comments': [
                        {
                            'id': comment.id,
                            'comment': comment.comment
                        } for comment in m.comments.all()
                    ],
                    'fsm_state': m.fsm_state,
                    'next_state': self.next_action(m.fsm_state),
                    'created': m.created,
                    'updated': m.updated 
                } for m in Mitigation.objects.all()
            ]
            result = (True, mitigations_list)
        except Mitigation.DoesNotExist:
            result (False, self.MITIGATION_ACTION_ERROR_GET_ALL)
        return result

    def get_serialized_contact(self, request):
        contact_data = {
            'full_name': request.get('contact').get('full_name'),
            'job_title': request.get('contact').get('job_title'),
            'email': request.get('contact').get('email'),
            'phone': request.get('contact').get('phone'),
        }
      
        serializer = ContactSerializer(data=contact_data)
        return serializer

    def get_serialized_contact_for_existing(self, request, contact):
        contact_data = {
            'full_name': request.get('contact').get('full_name'),
            'job_title': request.get('contact').get('job_title'),
            'email': request.get('contact').get('email'),
            'phone': request.get('contact').get('phone'),
        }
        serializer = ContactSerializer(contact, data=contact_data)
        return serializer

    def get_serialized_progress_indicator(self, request):
        progress_indicator_data = {
            'name': request.get('progress_indicator').get('name'),
            'type': request.get('progress_indicator').get('type'),
            'unit': request.get('progress_indicator').get('unit'),
            'start_date': request.get('progress_indicator').get('start_date')
        }
        serializer = ProgressIndicatorSerializer(data=progress_indicator_data)
        return serializer

    def get_serialized_progress_indicator_for_existing(self, request, progress_indicator):
        progress_indicator_data = {
            'name': request.get('progress_indicator').get('name'),
            'type': request.get('progress_indicator').get('type'),
            'unit': request.get('progress_indicator').get('unit'),
            'start_date': request.get('progress_indicator').get('start_date')
        }
        serializer = ProgressIndicatorSerializer(progress_indicator, data=progress_indicator_data)
        return serializer

    def get_serialized_location(self, request):
        location_data = {
            'geographical_site': request.get('location').get('geographical_site'),
            'is_gis_annexed': request.get('location').get('is_gis_annexed')
        }
        serializer = LocationSerializer(data=location_data)
        return serializer

    def get_serialized_location_for_existing(self, request, location):
        location_data = {
            'geographical_site': request.get('location').get('geographical_site'),
            'is_gis_annexed': request.get('location').get('is_gis_annexed')
        }
        serializer = LocationSerializer(location, data=location_data)
        return serializer

    def get_serialized_finance(self, request):
        finance_data = {
            'status': request.get('finance').get('status'),
            'source': request.get('finance').get('source'),
        }
        serializer = FinanceSerializer(data=finance_data)
        return serializer

    def get_serialized_finance_for_existing(self, request, finance):
        finance_data = {
            'status': request.get('finance').get('status'),
            'source': request.get('finance').get('source'),
        }
        serializer = FinanceSerializer(finance, data=finance_data)
        return serializer

    def get_serialized_initiative_finance(self, request):
        finance_data = {
            'finance_source_type': request.get('finance').get('finance_source_type'),
            'status': request.get('finance').get('status'),
        }
        serializer = InitiativeFinanceSerializer(data=finance_data)
        return serializer

    def get_serialized_initiative_finance_for_existing(self, request, finance):
        finance_data =  {
            'finance_source_type': request.get('finance').get('finance_source_type'),
            'status': request.get('finance').get('status'),
        }
        serializer = InitiativeFinanceSerializer(finance, data=finance_data)
        return serializer

    def get_review_status_id(self, status):
        review_status_id_result, review_status_id_data = workflow_service.get_review_status_id(status)
        return review_status_id_data

    def get_serialized_initiative(self, request, contact_id, finance_id, initiative = False):
        
        initiative_data = {
            'name': request.get('initiative').get('name'),
            'objective': request.get('initiative').get('objective'),
            'description': request.get('initiative').get('description'),
            'goal': request.get('initiative').get('goal'),
            'initiative_type': request.get('initiative').get('initiative_type'),
            'entity_responsible': request.get('initiative').get('entity_responsible'),
            'contact': contact_id,
            'budget': request.get('initiative').get('budget'),
            'finance': finance_id,
            'status': request.get('initiative').get('status'),
        }
        
        if initiative:
            serializer = InitiaveSerializer(initiative, data = initiative_data)

        else:
            serializer = InitiaveSerializer(data = initiative_data)

        return serializer

    def get_serialized_mitigation_action(self, request, contact_id = None, progress_indicator_id = None, location_id = None, finance_id = None, initiative_id = None):

        mitigation_data = {
            'id': str(uuid.uuid4()),
            'contact' : contact_id,
            'progress_indicator' : progress_indicator_id,
            'location': location_id,
            'finance':finance_id,
            'initiative' : initiative_id,

            #Workflow
            'review_count': 0 # By default when creating
        }
        fk_field = ['contact', 'progress_indicator', 'location', 'finance', 'initiative']

        for field in MitigationSerializer.Meta.fields:
            if field in request and not field in fk_field:
                mitigation_data[field] = request.get(field)
            
        
        serializer = MitigationSerializer(data = mitigation_data)
        return serializer
            
        

    def get_serialized_mitigation_action_for_existing(self, request, mitigation, contact_id = None, progress_indicator_id = None, location_id = None, finance_id = None, initiative_id = None, review_count = None):
        mitigation_data =  {}
        fk_field = ['contact', 'progress_indicator', 'location', 'finance', 'initiative', 'review_count']
        for field in MitigationSerializer.Meta.fields:
            if field in request and not field in fk_field:
                mitigation_data[field] = request.get(field)
        
        if review_count : mitigation_data['review_count'] = review_count
        if contact_id: mitigation_data['contact'] = contact_id
        if progress_indicator_id: mitigation_data['progress_indicator'] = progress_indicator_id
        if location_id: mitigation_data['location'] = location_id
        if finance_id: mitigation_data['finance'] = finance_id
        if initiative_id: mitigation_data['initiative'] = initiative_id
        
        serializer = MitigationSerializer(mitigation, data=mitigation_data)
        return serializer

    def assign_ingei_compliances(self, request, mitigation_action):
        ingei_ids_str = request.data.get('ingei_compliances')
        ingei_ids_array = list(map(int, ingei_ids_str.split(',')))
        for id in ingei_ids_array:
            try:
                ingei = IngeiCompliance.objects.get(pk=id)
                mitigation_action.ingei_compliances.add(ingei)
                
                result = (True, mitigation_action)
            except IngeiCompliance.DoesNotExist:
                result = (False, self.INGEI_COMPLIANCE_DOES_NOT_EXIST)
        return result

    def assign_comment(self, request, mitigation_action):
        comment_result_status, comment_result_data = workflow_service.create_comment(request)
        if comment_result_status:
            comment = comment_result_data
            mitigation_action.comments.add(comment)
        return comment_result_status

    def get_serialized_change_log(self, mitigation_id, previous_status_id, current_status_id, user):
        change_log_data = {
            'mitigation_action': mitigation_id,
            'previous_status': previous_status_id,
            'current_status': current_status_id,
            'user': user
        }
        serializer = ChangeLogSerializer(data=change_log_data)
        return serializer

    def create_change_log_entry(self, mitigation, previous_status, current_status, user):
        serialized_change_log = self.get_serialized_change_log(mitigation.id, previous_status, current_status, user)
        if serialized_change_log.is_valid():
            serialized_change_log.save()
            result = (True, serialized_change_log.data)
        else:
            result = (False, serialized_change_log.errors)
        return result


    def getReviewStatus(self, id):
        return ReviewStatus.objects.get(pk=id)

    def get_change_log(self, id):
        try:
            mitigation = self.get_one(id)
            change_log_content = []
            for log in ChangeLog.objects.filter(mitigation_action=mitigation.id):
                change_log_data = {
                    'date': log.date,
                    'mitigation_action': log.mitigation_action.id,
                    'previous_state': log.previous_status,
                    'current_status': log.current_status,
                    'user': log.user.id
                }
                change_log_content.append(change_log_data)
            result = (True, change_log_content)
        except Mitigation.DoesNotExist:
            result = (False, self.MITIGATION_ACTION_DOES_NOT_EXIST)
        return result


    def create_initiative(self, request):

        errors = []
        result = (False, None)

        initiative = request.data.get('initiative')
        serialized_contact = self.get_serialized_contact(initiative)
        serialized_finance = self.get_serialized_initiative_finance(initiative)

        valid_relations = [serialized_contact.is_valid(), serialized_finance.is_valid()]

        if not valid_relations.count(False):
            contact = serialized_contact.save()
            finance = serialized_finance.save()
            serialized_initiative = self.get_serialized_initiative(request.data, contact.id, finance.id)

            if serialized_initiative.is_valid():
                initiative = serialized_initiative.save()
                result = (True, initiative)

            else:
                errors.append(serialized_initiative.errors)
                result = (False, errors)

        else:
            errors.append(serialized_contact.errors)
            errors.append(serialized_finance.errors)
            result = (False, errors)

        return result
    
    def update_initiative(self, request, initiative):
        errors = []
        result = (False, None)
        
        contact_id = request.get('initiative').get('contact').get('id')
        finance_id = request.get('initiative').get('finance').get('id')

        if initiative.contact.id == int(contact_id) and initiative.finance.id == int(finance_id): 
            contact = Contact.objects.get(pk = contact_id)
            finance = InitiativeFinance.objects.get(pk = finance_id)

            serialized_contact = self.get_serialized_contact_for_existing(request.get('initiative'), contact)
            serialized_finance = self.get_serialized_initiative_finance_for_existing(request.get('initiative'), finance)
            
            valid_relations = [serialized_contact.is_valid(), serialized_finance.is_valid()]
            
            if not valid_relations.count(False):
                contact = serialized_contact.save()
                finance = serialized_finance.save()
                serialized_initiative = self.get_serialized_initiative(request, contact.id, finance.id, initiative)

                if serialized_initiative.is_valid():
                    initiative = serialized_initiative.save()
                    result = (True, initiative)
                
                else:
                    errors.append(serialized_initiative.errors)
                    result = (False, errors)
            
            else:
                errors.append(serialized_contact.errors)
                errors.append(serialized_finance.errors)
                result = (False, errors)
        else:
            result = (False, self.INITIATIVE_RELATIONS)


        return result


    def update_mitigation_action(self, request, mitigation_action):
        errors = []
        valid_relations = []
        if "initiative" in request.data:
            if request.data.get('initiative').get('id'):
                initiative_id = request.data.get('initiative').get('id')
                if mitigation_action.initiative.id != int(initiative_id):
                    return (False, "initiative_id" + self.RELATED_MITIGATION_ACTION)
                initiative = Initiative.objects.get(pk = initiative_id)
                is_valid, initiative  = self.update_initiative(request.data, initiative)
            else:

                is_valid, initiative = self.create_initiative(request)

            if is_valid: 
                serialized_mitigation_action = self.get_serialized_mitigation_action_for_existing(request.data,mitigation_action, initiative_id = initiative.id )
                if serialized_mitigation_action.is_valid(): mitigation_action = serialized_mitigation_action.save()
                else:
                    result = (False, serialized_mitigation_action.errors)
                    return result
            else:
                result = (False, initiative)
                return result

        if "contact" in request.data:
            if request.data.get('contact').get('id'):
                contact_id = request.data.get('contact').get('id')
                if mitigation_action.contact.id != int(contact_id):
                    return (False, "contact_id" + self.RELATED_MITIGATION_ACTION)
                contact = Contact.objects.get(pk=contact_id)
                serialized_contact = self.get_serialized_contact_for_existing(request.data, contact)

            else:
                serialized_contact = self.get_serialized_contact(request.data)

            is_valid = serialized_contact.is_valid()
            if is_valid: 
                contact = serialized_contact.save()
                serialized_mitigation_action = self.get_serialized_mitigation_action_for_existing(request.data,mitigation_action, contact_id=contact.id )
                if serialized_mitigation_action.is_valid(): mitigation_action = serialized_mitigation_action.save()
                else:
                    result = (False, serialized_mitigation_action.errors)
                    return result
            else:
                valid_relations.append(is_valid)
                errors.append(serialized_contact.errors)
        
        if "location" in request.data:
            if request.data.get('location').get('id'):
                location_id = request.data.get('location').get('id')
                
                if mitigation_action.location.id != int(location_id):
                    return (False, "location_id" + self.RELATED_MITIGATION_ACTION)

                location = Location.objects.get(pk = location_id)
                serialized_location = self.get_serialized_location_for_existing(request.data, location)

            else:
                serialized_location = self.get_serialized_location(request.data)
            is_valid = serialized_location.is_valid()
            if is_valid: 
                location = serialized_location.save()
                serialized_mitigation_action = self.get_serialized_mitigation_action_for_existing(request.data,mitigation_action, location_id=location.id )
                if serialized_mitigation_action.is_valid(): mitigation_action = serialized_mitigation_action.save()
                else:
                    result = (False, serialized_mitigation_action.errors)
                    return result
            else:
                valid_relations.append(is_valid)
                errors.append(serialized_location.errors)
        
        if "finance" in request.data:
            if request.data.get('finance').get('id'):
                finance_id = request.data.get('finance').get('id')
                if mitigation_action.finance.id != int(finance_id):
                    return (False, "finance_id" + self.RELATED_MITIGATION_ACTION)
                finance = Finance.objects.get(pk = finance_id)
                serialized_finance = self.get_serialized_finance_for_existing(request.data, finance)

            else:
                serialized_finance = self.get_serialized_finance(request.data)

            is_valid = serialized_finance.is_valid()
            if is_valid:
                finance = serialized_finance.save() 
                serialized_mitigation_action = self.get_serialized_mitigation_action_for_existing(request.data,mitigation_action, finance_id=finance.id )
                if serialized_mitigation_action.is_valid(): mitigation_action = serialized_mitigation_action.save()
                else:
                    result = (False, serialized_mitigation_action.errors)
                    return result
            else:
                valid_relations.append(is_valid)
                errors.append(serialized_finance.errors)
        
        if "progress_indicator" in request.data:
            if request.data.get('progress_indicator').get('id'):
                progress_indicator_id = request.data.get('progress_indicator').get('id')
                progress_indicator = ProgressIndicator.objects.get(pk = progress_indicator_id)
                serialized_progress_indicator = self.get_serialized_progress_indicator_for_existing(request.data, progress_indicator)

            else:
                serialized_progress_indicator = self.get_serialized_progress_indicator(request.data)

            is_valid = serialized_progress_indicator.is_valid()
            if is_valid:
                progress_indicator = serialized_progress_indicator.save() 
                serialized_mitigation_action = self.get_serialized_mitigation_action_for_existing(request.data,mitigation_action, progress_indicator_id=progress_indicator.id )
                if serialized_mitigation_action.is_valid(): mitigation_action = serialized_mitigation_action.save()
                else:
                    result = (False, serialized_mitigation_action.errors)
                    return result
            else:
                valid_relations.append(is_valid)
                errors.append(serialized_progress_indicator.errors)

        if 'ingei_compliances' in request.data:
            mitigation_action.ingei_compliances.clear()
            get_ingei_result, data_ingei_result = self.assign_ingei_compliances(request, mitigation_action)
            if not get_ingei_result:
                errors.append(data_ingei_result)
                valid_relations.append(get_ingei_result)

        valid_relations = not valid_relations.count(False) 
        result = (valid_relations, [ MitigationSerializer(mitigation_action).data ] + errors)

        return result

    def create(self, request):
        result = (False, None)
        serialized_mitigation_action = self.get_serialized_mitigation_action(request.data)

        if serialized_mitigation_action.is_valid():
            mitigation_action = serialized_mitigation_action.save()
            result_status, mitigation_action_data  = self.update_mitigation_action(request, mitigation_action)
            result = (result_status, mitigation_action_data)
            if result_status and self.checkAllFieldComplete(mitigation_action_data):
                mitigation_previous_status = mitigation_action.fsm_state
                if not can_proceed(mitigation_action.submit):
                    errors.append(self.INVALID_STATUS_TRANSITION)
                
                mitigation_action.submit()
                mitigation_action.save()
                self.create_change_log_entry(mitigation_action, mitigation_previous_status, mitigation_action.fsm_state, request.data.get('user'))  
        else:
            
            result = (False, serialized_mitigation_action.errors)

        return result
    
    def checkAllFieldComplete(self, mitigation_action_data):

        result = True
        field_list = dict(mitigation_action_data[0].items())

        for field in field_list.keys():
            if field_list[field] == None and field != "progress_indicator": 

                if field != "international_participation":
                    result = False 

                # international_participation -> None and is_international -> True ==> not valid
                elif field_list['is_international']:
                    result = False

        return result

    def get_one(self, str_uuid):
        f_uuid = uuid.UUID(str_uuid)
        return Mitigation.objects.get(pk=f_uuid)

    def next_action(self, current_fsm_state):
        result = None
        if current_fsm_state == 'new':
            result = 'submitted'
        elif current_fsm_state == 'submitted' or current_fsm_state == 'updating_by_request':
            result = 'in_evaluation_by_DCC'
        elif current_fsm_state == 'in_evaluation_by_DCC':
            # Transitory step (FE input)
            result = 'decision_step_DCC'
        elif current_fsm_state == 'decision_step_DCC':
            result = False
        elif current_fsm_state == 'changes_requested_by_DCC':
            result = 'updating_by_request'
        elif current_fsm_state == 'rejected_by_DCC':
            result = 'end'
        elif current_fsm_state == 'registering' or current_fsm_state == 'updating_INGEI_changes_proposal_by_request_of_DCC_IMN':
            result = 'in_evaluation_INGEI_by_DCC_IMN'
        elif current_fsm_state == 'in_evaluation_INGEI_by_DCC_IMN':
            # Transitory step (FE input)
            result = 'submit_INGEI_harmonization_required'
        elif current_fsm_state == 'submit_INGEI_harmonization_required':
            result = False
        elif current_fsm_state == 'INGEI_harmonization_required':
            result = False
        elif current_fsm_state == 'updating_INGEI_changes_proposal':
            result = 'submitted_INGEI_changes_proposal_evaluation'
        elif current_fsm_state == 'submitted_INGEI_changes_proposal_evaluation':
            result = 'in_evaluation_INGEI_changes_proposal_by_DCC_IMN'
        elif current_fsm_state == 'in_evaluation_INGEI_changes_proposal_by_DCC_IMN':
            # Transitory step (FE input)
            result = 'submit_INGEI_changes_proposal_evaluation_result'
        elif current_fsm_state == 'submit_INGEI_changes_proposal_evaluation_result':
            result = False
        elif current_fsm_state == 'INGEI_changes_proposal_changes_requested_by_DCC_IMN':
            result = 'updating_INGEI_changes_proposal_by_request_of_DCC_IMN'
        elif current_fsm_state == 'INGEI_changes_proposal_rejected_by_DCC_IMN':
            result = 'submitted_SINAMECC_conceptual_proposal_integration'
        elif current_fsm_state == 'INGEI_changes_proposal_accepted_by_DCC_IMN':
            result = 'implementing_INGEI_changes'  
        elif current_fsm_state == 'updating_INGEI_changes_proposal_by_request_of_DCC_IMN':
            result = 'in_evaluation_INGEI_changes_proposal_by_DCC_IMN'
        elif current_fsm_state == 'implementing_INGEI_changes':
            result = 'submitted_SINAMECC_conceptual_proposal_integration'
        elif current_fsm_state == 'submitted_SINAMECC_conceptual_proposal_integration':
            result = 'in_evaluation_conceptual_proposal_by_DCC'
        elif current_fsm_state == 'in_evaluation_conceptual_proposal_by_DCC':
            # Transitory step (FE input)
            result = 'decision_step_DCC_proposal'
        elif current_fsm_state == 'decision_step_DCC_proposal':
            result = False
        elif current_fsm_state == 'conceptual_proposal_approved':
            result = 'planning_integration_with_SINAMECC'
        elif current_fsm_state == 'changes_requested_to_conceptual_proposal':
            result = 'submitted_conceptual_proposal_changes'
        elif current_fsm_state == 'submitted_conceptual_proposal_changes':
            result = 'submitted_SINAMECC_conceptual_proposal_integration'
        elif current_fsm_state == 'planning_integration_with_SINAMECC':
            # Transitory step (FE input)
            result = 'decision_step_SINAMEC'
        elif current_fsm_state == 'decision_step_SINAMEC':
            result = False
        elif current_fsm_state == 'SINAMECC_integration_approved':
            result = 'implementing_SINAMECC_changes'
        elif current_fsm_state == 'SINAMECC_integration_changes_requested':
            result = 'submitted_SINAMECC_integration_changes'
        elif current_fsm_state == 'submitted_SINAMECC_integration_changes':
            result = 'planning_integration_with_SINAMECC'
        elif current_fsm_state == 'implementing_SINAMECC_changes':
            result = 'end'
        return result  

    def get(self, id, language):

        try:
            mitigation = self.get_one(id)
            content = {
                'id': mitigation.id,
                'strategy_name': mitigation.strategy_name,
                'name': mitigation.name,
                'purpose': mitigation.purpose,
                'quantitative_purpose': mitigation.quantitative_purpose,
                'start_date': mitigation.start_date,
                'end_date': mitigation.end_date,
                'gas_inventory': mitigation.gas_inventory,
                'emissions_source': mitigation.emissions_source,
                'carbon_sinks': mitigation.carbon_sinks,
                'impact_plan': mitigation.impact_plan,
                'impact': mitigation.impact,
                'bibliographic_sources': mitigation.bibliographic_sources,
                'is_international': mitigation.is_international,
                'international_participation': mitigation.international_participation,
                'sustainability': mitigation.sustainability,
                'question_ucc': mitigation.question_ucc,
                'question_ovv': mitigation.question_ovv,
                'user': {
                    'id': mitigation.user.id,
                    'username': mitigation.user.username,
                    'email': mitigation.user.email
                },
                'initiative':{
                    'id' : mitigation.initiative.id,
                    'name': mitigation.initiative.name,
                    'objective' : mitigation.initiative.objective,
                    'description': mitigation.initiative.description,
                    'goal' : mitigation.initiative.goal,
                    'initiative_type': {
                            "id": mitigation.initiative.initiative_type.id,
                            "initiative_type" : mitigation.initiative.initiative_type.initiative_type_es if language=="es" else mitigation.initiative.initiative_type.initiative_type_en,
                    }, 
                    'entity_responsible': mitigation.initiative.entity_responsible,
                    'budget': mitigation.initiative.budget,
                    'status' : {
                        'id': mitigation.initiative.status.id,
                        'status': mitigation.initiative.status.status_es if language=="es" else mitigation.initiative.status.status_en
                    },
                    'contact': {
                        'id': mitigation.initiative.contact.id,
                        'full_name': mitigation.initiative.contact.full_name,
                        'job_title': mitigation.initiative.contact.job_title,
                        'email': mitigation.initiative.contact.email,
                        'phone': mitigation.initiative.contact.phone
                    },

                    'finance': {
                        'id': mitigation.initiative.finance.id,
                        'status':{
                                'id' : mitigation.initiative.finance.status.id,
                                'name' : mitigation.initiative.finance.status.name_es if language=="es" else mitigation.initiative.finance.status.name_en
                        } ,
                        'finance_source_type': {
                            'id': mitigation.initiative.finance.finance_source_type.id,
                            'name': mitigation.initiative.finance.finance_source_type.name_es if language=="es" else mitigation.initiative.finance.finance_source_type.name_en,
                        }
                    },
                } if mitigation.initiative else {},
                'registration_type': {
                    'id': mitigation.registration_type.id,
                    'type': mitigation.registration_type.type_es if language=="es" else mitigation.registration_type.type_en,
                } if mitigation.registration_type else {},
                'institution': {
                    'id': mitigation.institution.id,
                    'name': mitigation.institution.name
                } if mitigation.institution else {},
                'contact': {
                    'id': mitigation.contact.id,
                    'full_name': mitigation.contact.full_name,
                    'job_title': mitigation.contact.job_title,
                    'email': mitigation.contact.email,
                    'phone': mitigation.contact.phone
                } if mitigation.contact else {},
                'status': {
                    'id': mitigation.status.id,
                    'status': mitigation.status.status_es if language=="es" else mitigation.status.status_en
                } if mitigation.status else {},
                'progress_indicator': {
                    'id': mitigation.progress_indicator.id,
                    'name': mitigation.progress_indicator.name,
                    'type': mitigation.progress_indicator.type,
                    'unit': mitigation.progress_indicator.unit,
                    'start_date': mitigation.progress_indicator.start_date
                } if mitigation.progress_indicator else {},
                'finance': {
                    'id': mitigation.finance.id,
                    'status':{
                        'id' : mitigation.finance.status.id,
                        'name' : mitigation.finance.status.name_es if language=="es" else mitigation.finance.status.name_en
                    } ,
                    'source': mitigation.finance.source
                } if mitigation.finance else {},
                'ingei_compliances': [
                    {
                      'id': ingei.id,
                      'name': ingei.name_es if language=="es" else ingei.name_en
                    } for ingei in mitigation.ingei_compliances.all()
                ],
                'geographic_scale': {
                    'id': mitigation.geographic_scale.id,
                    'name': mitigation.geographic_scale.name_es if language=="es" else mitigation.geographic_scale.name_en
                } if mitigation.geographic_scale else {},
                'location': {
                    'id': mitigation.location.id,
                    'geographical_site': mitigation.location.geographical_site,
                    'is_gis_annexed': mitigation.location.is_gis_annexed
                } if mitigation.location else {},
                # Workflow
                'review_count': mitigation.review_count,
                'comments': [
                    {
                        'id': comment.id,
                        'comment': comment.comment
                    } for comment in mitigation.comments.all()
                ],
                'fsm_state': mitigation.fsm_state,
                'next_state': self.next_action(mitigation.fsm_state),
                'files': self._get_files_list([f.workflow_step_file.all() for f in mitigation.workflow_step.all()]),
                'created': mitigation.created,
                'updated': mitigation.updated
            }
            result = (True, content)
        except Mitigation.DoesNotExist:
            result = (False, self.MITIGATION_ACTION_DOES_NOT_EXIST)
        return result

    def delete(self, id):
        try:
            mitigation = self.get_one(id)
            mitigation.ingei_compliances.clear()
            mitigation.delete()
            result = True
        except:
            result = False
        return result

    def update(self, id, request, language):

        errors = []
        mitigation = self.get_one(id)
        serialized_mitigation_action = self.get_serialized_mitigation_action_for_existing(request.data, mitigation)

        update_existing= request.data.get('update_existing_mitigation_action')
        update_new = request.data.get('update_new_mitigation_action')

        if serialized_mitigation_action.is_valid():
            mitigation_action = serialized_mitigation_action.save()
            result_status, mitigation_action_data  = self.update_mitigation_action(request, mitigation_action)
            result = (result_status, mitigation_action_data)
            if update_new :
                if self.checkAllFieldComplete(mitigation_action_data):
                    mitigation_previous_status = mitigation_action.fsm_state
                    if not can_proceed(mitigation_action.submit):
                        errors.append(self.INVALID_STATUS_TRANSITION)
                    mitigation_action.submit()

                    mitigation_action.save()
                    self.create_change_log_entry(mitigation_action, mitigation_previous_status, mitigation_action.fsm_state, request.data.get('user'))

            if update_existing :
                if self.checkAllFieldComplete(mitigation_action_data):
                    mitigation_previous_status = mitigation_action.fsm_state
                    if not can_proceed(mitigation_action.update_by_request):
                        errors.append(self.INVALID_STATUS_TRANSITION)
                    mitigation_action.update_by_request()
                    mitigation_action.save()
                    self.create_change_log_entry(mitigation_action, mitigation_previous_status, mitigation_action.fsm_state, request.data.get('user'))

            if result_status:

                result_status, mitigation_action_data = self.get(str(mitigation_action.id), language)
                result = (result_status, [mitigation_action_data])

            else:
                result = (False, errors)
        
        else:

            result = (False, serialized_mitigation_action.errors)

        return result

    def update_fsm_state(self, next_state, mitigation_action):
        # --- Transition ---
        # updating_by_request -> in_evaluation_by_DCC
        if next_state == 'in_evaluation_by_DCC' and mitigation_action.fsm_state == 'updating_by_request':
            if not can_proceed(mitigation_action.update_evaluate_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.update_evaluate_DCC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submitted -> in_evaluation_by_DCC
        elif next_state == 'in_evaluation_by_DCC':
            if not can_proceed(mitigation_action.evaluate_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.evaluate_DCC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # in_evaluation_by_DCC -> decision_step_DCC
        elif next_state == 'decision_step_DCC':
            if not can_proceed(mitigation_action.submit_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_DCC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # decision_step_DCC -> changes_requested_by_DCC
        elif next_state == 'changes_requested_by_DCC' and mitigation_action.fsm_state == 'decision_step_DCC':
            if not can_proceed(mitigation_action.request_changes_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.request_changes_DCC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # decision_step_DCC -> rejected_by_DCC
        elif next_state == 'rejected_by_DCC':
            if not can_proceed(mitigation_action.reject_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.reject_DCC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # decision_step_DCC -> registering
        elif next_state == 'registering':
            if not can_proceed(mitigation_action.register):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.register()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # in_evaluation_by_DCC -> changes_requested_by_DCC
        elif next_state == 'changes_requested_by_DCC' and mitigation_action.fsm_state == 'in_evaluation_by_DCC':
            if not can_proceed(mitigation_action.evaluate_request_changes_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.evaluate_request_changes_DCC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # changes_requested_by_DCC -> updating_by_request
        elif next_state == 'updating_by_request':
            if not can_proceed(mitigation_action.update_by_request):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.update_by_request()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # in_evaluation_by_DCC -> rejected_by_DCC
        elif next_state == 'rejected_by_DCC':
            if not can_proceed(mitigation_action.evaluate_reject_by_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.evaluate_reject_by_DCC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # rejected_by_DCC -> end
        elif next_state == 'end':
            if not can_proceed(mitigation_action.end):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.end()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # in_evaluation_by_DCC -> registering
        elif next_state == 'registering':
            if not can_proceed(mitigation_action.evaluate_register):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.evaluate_register()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # registering -> in_evaluation_INGEI_by_DCC_IMN
        elif next_state == 'in_evaluation_INGEI_by_DCC_IMN':
            if not can_proceed(mitigation_action.evaluate_INGEI):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.evaluate_INGEI()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # in_evaluation_INGEI_by_DCC_IMN -> submit_INGEI_harmonization_required
        elif next_state == 'submit_INGEI_harmonization_required':
            if not can_proceed(mitigation_action.submit_INGEI):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_INGEI()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submit_INGEI_harmonization_required -> INGEI_harmonization_required
        elif next_state == 'INGEI_harmonization_required':
            if not can_proceed(mitigation_action.require_INGEI_harmonization):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.require_INGEI_harmonization()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submit_INGEI_harmonization_required -> submitted_SINAMECC_conceptual_proposal_integration
        elif next_state == 'submitted_SINAMECC_conceptual_proposal_integration' and mitigation_action.fsm_state == 'submit_INGEI_harmonization_required':
            if not can_proceed(mitigation_action.submit_INGEI_SINAMECC_conceptual_proposal):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_INGEI_SINAMECC_conceptual_proposal()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # in_evaluation_INGEI_by_DCC_IMN -> INGEI_harmonization_required
        elif next_state == 'INGEI_harmonization_required':
            if not can_proceed(mitigation_action.evaluate_require_INGEI_harmonization):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.evaluate_require_INGEI_harmonization()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # INGEI_harmonization_required -> updating_INGEI_changes_proposal
        elif next_state == 'updating_INGEI_changes_proposal':
            if not can_proceed(mitigation_action.update_INGEI_changes_proposal):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.update_INGEI_changes_proposal()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # INGEI_harmonization_required -> submitted_SINAMECC_conceptual_proposal_integration
        elif next_state == 'submitted_SINAMECC_conceptual_proposal_integration'  and mitigation_action.fsm_state == 'INGEI_harmonization_required':
            if not can_proceed(mitigation_action.submit_SINAMECC_conceptual_proposal):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_SINAMECC_conceptual_proposal()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # INGEI_harmonization_required -> updating_INGEI_changes_proposal
        elif next_state == 'updating_INGEI_changes_proposal':
            if not can_proceed(mitigation_action.update_INGEI_changes_proposal):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.update_INGEI_changes_proposal()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # updating_INGEI_changes_proposal -> submitted_INGEI_changes_proposal_evaluation
        elif next_state == 'submitted_INGEI_changes_proposal_evaluation':
            if not can_proceed(mitigation_action.submit_INGEI_changes_evaluation):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_INGEI_changes_evaluation()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submitted_INGEI_changes_proposal_evaluation -> in_evaluation_INGEI_changes_proposal_by_DCC_IMN
        elif next_state == 'in_evaluation_INGEI_changes_proposal_by_DCC_IMN':
            if not can_proceed(mitigation_action.evaluate_DCC_IMN):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.evaluate_DCC_IMN()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # in_evaluation_INGEI_changes_proposal_by_DCC_IMN -> submit_INGEI_changes_proposal_evaluation_result
        elif next_state == 'submit_INGEI_changes_proposal_evaluation_result':
            if not can_proceed(mitigation_action.submit_INGEI_changes_proposal_evaluation_result):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_INGEI_changes_proposal_evaluation_result()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submit_INGEI_changes_proposal_evaluation_result -> INGEI_changes_proposal_changes_requested_by_DCC_IMN
        elif next_state == 'INGEI_changes_proposal_changes_requested_by_DCC_IMN':
            if not can_proceed(mitigation_action.request_changes_DCC_IMN):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.request_changes_DCC_IMN()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submit_INGEI_changes_proposal_evaluation_result -> INGEI_changes_proposal_rejected_by_DCC_IMN
        elif next_state == 'INGEI_changes_proposal_rejected_by_DCC_IMN':
            if not can_proceed(mitigation_action.reject_changes_proposal_by_DCC_IMN):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.reject_changes_proposal_by_DCC_IMN()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submit_INGEI_changes_proposal_evaluation_result -> INGEI_changes_proposal_accepted_by_DCC_IMN
        elif next_state == 'INGEI_changes_proposal_accepted_by_DCC_IMN':
            if not can_proceed(mitigation_action.accept_changes_proposal_by_DCC_IMN):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.accept_changes_proposal_by_DCC_IMN()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # INGEI_changes_proposal_changes_requested_by_DCC_IMN -> updating_INGEI_changes_proposal_by_request_of_DCC_IMN
        elif next_state == 'updating_INGEI_changes_proposal_by_request_of_DCC_IMN':
            if not can_proceed(mitigation_action.update_changes_proposal_by_DCC_IMN):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.update_changes_proposal_by_DCC_IMN()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # INGEI_changes_proposal_rejected_by_DCC_IMN -> submitted_SINAMECC_conceptual_proposal_integration
        elif next_state == 'submitted_SINAMECC_conceptual_proposal_integration':
            if not can_proceed(mitigation_action.submit_SINAMECC_conceptual_proposal_integration):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_SINAMECC_conceptual_proposal_integration()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # INGEI_changes_proposal_accepted_by_DCC_IMN -> implementing_INGEI_changes
        elif next_state == 'implementing_INGEI_changes':
            if not can_proceed(mitigation_action.implement_INGEI_changes):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.implement_INGEI_changes()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # updating_INGEI_changes_proposal_by_request_of_DCC_IMN -> in_evaluation_INGEI_changes_proposal_by_DCC_IMN
        elif next_state == 'in_evaluation_INGEI_changes_proposal_by_DCC_IMN':
            if not can_proceed(mitigation_action.update_evaluate_DCC_IMN):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.update_evaluate_DCC_IMN()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # implementing_INGEI_changes -> submitted_SINAMECC_conceptual_proposal_integration
        elif next_state == 'submitted_SINAMECC_conceptual_proposal_integration':
            if not can_proceed(mitigation_action.implement_submit_SINAMECC_conceptual_proposal_integration):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.implement_submit_SINAMECC_conceptual_proposal_integration()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submitted_SINAMECC_conceptual_proposal_integration -> in_evaluation_conceptual_proposal_by_DCC
        elif next_state == 'in_evaluation_conceptual_proposal_by_DCC':
            if not can_proceed(mitigation_action.evaluate_conceptual_proposal_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.evaluate_conceptual_proposal_DCC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # decision_step_DCC_proposal -> conceptual_proposal_approved
        elif next_state == 'conceptual_proposal_approved':
            if not can_proceed(mitigation_action.approve_conceptual_proposal):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.approve_conceptual_proposal()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # decision_step_DCC_proposal -> changes_requested_to_conceptual_proposal
        elif next_state == 'changes_requested_to_conceptual_proposal':
            if not can_proceed(mitigation_action.request_changes_conceptual_proposal):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.request_changes_conceptual_proposal()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # conceptual_proposal_approved -> planning_integration_with_SINAMECC
        elif next_state == 'planning_integration_with_SINAMECC':
            if not can_proceed(mitigation_action.plan_integration_SINAMECC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.plan_integration_SINAMECC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # changes_requested_to_conceptual_proposal -> submitted_conceptual_proposal_changes
        elif next_state == 'submitted_conceptual_proposal_changes':
            if not can_proceed(mitigation_action.submit_conceptual_proposal_changes):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_conceptual_proposal_changes()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submitted_conceptual_proposal_changes -> submitted_SINAMECC_conceptual_proposal_integration
        elif next_state == 'submitted_SINAMECC_conceptual_proposal_integration':
            if not can_proceed(mitigation_action.submit_SINAMECC_conceptual_proposal_changes):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_SINAMECC_conceptual_proposal_changes()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # decision_step_SINAMEC -> SINAMECC_integration_approved
        elif next_state == 'SINAMECC_integration_approved':
            if not can_proceed(mitigation_action.approve_SINAMECC_integration):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.approve_SINAMECC_integration()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # decision_step_SINAMEC -> SINAMECC_integration_changes_requested
        elif next_state == 'SINAMECC_integration_changes_requested':
            if not can_proceed(mitigation_action.request_changes_SINAMECC_integration):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.request_changes_SINAMECC_integration()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # SINAMECC_integration_approved -> implementing_SINAMECC_changes
        elif next_state == 'implementing_SINAMECC_changes':
            if not can_proceed(mitigation_action.implement_SINAMECC_changes):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.implement_SINAMECC_changes()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # SINAMECC_integration_changes_requested -> submitted_SINAMECC_integration_changes
        elif next_state == 'submitted_SINAMECC_integration_changes':
            if not can_proceed(mitigation_action.submit_SINAMECC_integration_changes):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_SINAMECC_integration_changes()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # submitted_SINAMECC_integration_changes -> planning_integration_with_SINAMECC
        elif next_state == 'planning_integration_with_SINAMECC':
            if not can_proceed(mitigation_action.submit_plan_integration_SINAMECC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.submit_plan_integration_SINAMECC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # in_evaluation_conceptual_proposal_by_DCC -> decision_step_DCC_proposal
        elif next_state == 'decision_step_DCC_proposal':
            if not can_proceed(mitigation_action.decide_DCC_proposal):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.decide_DCC_proposal()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # planning_integration_with_SINAMECC -> decision_step_SINAMEC
        elif next_state == 'decision_step_SINAMEC':
            if not can_proceed(mitigation_action.decide_SINAMECC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.decide_SINAMECC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        # --- Transition ---
        # implementing_SINAMECC_changes -> end
        elif next_state == 'end':
            if not can_proceed(mitigation_action.end_SINAMECC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            mitigation_action.end_SINAMECC()
            mitigation_action.save()
            result = (True, MitigationSerializer(mitigation_action).data)
        return result
            
    def patch(self, id, request):
        mitigation = self.get_one(id)
        if (request.data.get('fsm_state')):
            patch_data = {
                'review_count': mitigation.review_count + 1
            }
            serialized_mitigation_action = MitigationSerializer(mitigation, data=patch_data, partial=True)
            if serialized_mitigation_action.is_valid():
                mitigation_previous_status = mitigation.fsm_state
                mitigation_action = serialized_mitigation_action.save()
                update_state_status, update_state_data = self.update_fsm_state(request.data.get('fsm_state'), mitigation_action)
                if update_state_status:
                    self.create_change_log_entry(mitigation_action, mitigation_previous_status, mitigation_action.fsm_state, request.data.get('user'))
                    result = (True, update_state_data)
                else:
                    result = (False, update_state_data)
            if (request.data.get('comment')):
                comment_status = self.assign_comment(request, mitigation_action)
                if comment_status:
                    result = (True, MitigationSerializer(mitigation_action).data)
                else:
                    result = (False, self.COMMENT_NOT_ASSIGNED)
        else:
            result = (False, self.NO_PATCH_DATA_PROVIDED)
        return result

    def get_form_data(self):       
        try:
            registration_types_list = [
                {
                    'id': rt.id,
                    'type_es': rt.type_es,
                    'type_en':rt.type_en
                } for rt in RegistrationType.objects.all()
            ]
            institutions_list = [
                {
                    'id': i.id,
                    'name': i.name
                } for i in Institution.objects.all()
            ]
            statuses_list = [
                {
                    'id': st.id,
                    'status_en': st.status_en,
                    'status_es': st.status_es
                } for st in Status.objects.all()
            ]
            finance_source_types_list = [
                {
                    'id': fst.id,
                    'name_es': fst.name_es,
                    'name_en': fst.name_en,
                } for fst in FinanceSourceType.objects.all()
            ]
            ingei_compliances_list = [
                {
                    'id': i.id,
                    'name_es': i.name_es,
                    'name_en': i.name_en,
                } for i in IngeiCompliance.objects.all()
            ]
            geographic_scales_list = [
                {
                    'id': g.id,
                    'name_es': g.name_es,
                    'name_en': g.name_en
                } for g in GeographicScale.objects.all()
            ]
            form_list = {
              'registration_types': registration_types_list,
              'institutions': institutions_list,
              'statuses': statuses_list,
              'finance_source_types': finance_source_types_list,
              'ingei_compliances': ingei_compliances_list,
              'geographic_scales': geographic_scales_list
            }
            result = (True, form_list)
        except Mitigation.DoesNotExist:
            result = (False, {'error': self.MITIGATION_ACTION_DOES_NOT_EXIST})
        return result

    # TODO Fix this multi-return method
    def get_form_data_es_en(self, language, option):
        Registration_Type = []

        if (option == "new" or option == "update"):
            Registration_Type.append(RegistrationType.objects.filter(type_key=option).get())
        else:
            return (False, {'error': "Parameter is not valid"})

        try:
            registration_types_list = [
                {
                    'id': rg.id,
                    'type': rg.type_es if language=="es" else rg.type_en
                } for rg in Registration_Type
            ]
            institutions_list = [
                {
                    'id': i.id,
                    'name': i.name 
                } for i in Institution.objects.all()
            ]
            statuses_list = [
                {
                    'id': st.id, 
                    'status': st.status_es if language=="es" else st.status_en
                  } for st in Status.objects.all()
            ]
            finance_source_types_list = [
                {
                    'id': fst.id,
                    'name': fst.name_es if language=="es" else fst.name_en
                } for fst in FinanceSourceType.objects.all()
            ]
            ingei_compliances_list = [
                {
                    'id': i.id,
                    'name': i.name_es if language=="es" else i.name_en
                } for i in IngeiCompliance.objects.all()
            ]
            geographic_scales_list = [
                {
                    'id': g.id,
                    'name': g.name_es if language=="es" else g.name_en 
                } for g in GeographicScale.objects.all()
            ]
            initiative_types_list = [
                {
                    'id' : i.id,
                    'types' : i.initiative_type_es if language == "es" else i.initiative_type_en
                } for i in InitiativeType.objects.all()
                
            ]
            finance_status = [
                {
                    'id' : fs.id,
                    'status': fs.name_es if language=="es" else fs.name_en
                } for fs in FinanceStatus.objects.all()
            ]
            form_list = {
              'registration_types': registration_types_list,
              'institutions': institutions_list,
              'statuses': statuses_list,
              'finance_source_types': finance_source_types_list,
              'ingei_compliances': ingei_compliances_list,
              'geographic_scales': geographic_scales_list,
              'initiative_types': initiative_types_list,
              'finance_status' : finance_status
            }
            result = (True, form_list)
        except Mitigation.DoesNotExist:
            result = (False, {'error': self.MITIGATION_ACTION_DOES_NOT_EXIST})
        return result


   

    def get_file_content(self, file_id):
        
        MA_files = MAWorkflowStepFile.objects.get(id=file_id)
        path, filename = os.path.split(MA_files.file.name)
        return  (filename, BytesIO(self.storage.get_file(MA_files.file.name)))

    def download_file(self, id, file_id):
        return self.get_file_content(file_id)

    def _get_files_list(self, file_list):
        
        file_list = [file_list[0].union(q) for q in file_list[1:]] if len(file_list) > 1 else file_list
        file_list = file_list[0] if len(file_list) > 0 else file_list
        return [{'name': self._get_filename(f.file.name), 'file': self._get_file_path(str(f.workflow_step.mitigation_action.id), str(f.id))} for f in file_list]

    def _get_file_path(self, mitigation_action_id, mitigation_action_file_id):
        url = reverse("get_mitigation_action_file", kwargs={'id': mitigation_action_id, 'file_id': mitigation_action_file_id})
        return url

    def _get_filename(self, filename):
        fpath, fname = os.path.split(filename)
        return fname








