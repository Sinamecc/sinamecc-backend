from ppcn.models import Organization, GeographicLevel, RequiredLevel, RecognitionType, Sector,GeiOrganization, GeiActivityType, SubSector, PPCN, PPCNFile
from mccr.models import OVV
from django.contrib.auth.models import *
from mitigation_action.services import MitigationActionService
from mitigation_action.serializers import ContactSerializer
import json
from ppcn.serializers import *
from ppcn.workflow_steps.models import PPCNWorkflowStepFile
from rest_framework.parsers import JSONParser
import datetime
import uuid
from django_fsm import can_proceed, has_transition_perm
from io import BytesIO
from general.storages import S3Storage
from django.http import FileResponse
from django.urls import reverse
import os
import pdb
from general.services import EmailServices
email_sender  = "sinamec@grupoincocr.com" ##change to sinamecc email
ses_service = EmailServices(email_sender)
from workflow.models import ReviewStatus

from django.contrib.auth import get_user_model
User = get_user_model()

from workflow.services import WorkflowService
workflow_service = WorkflowService()

class PpcnService():

    def __init__(self):
        self.storage = S3Storage()
        self.ORGANIZATION_DOES_NOT_EXIST = "Organization does not exist."
        self.ORGANIZATION_ERROR_GET_ALL = "Error retrieving all organizations records."
        self.GEOGRAPHIC_LEVEL_ERROR_GET_ALL = "Error retrieving all geographic level records."
        self.REQUIRED_LEVEL_ERROR_GET_ALL = "Error retrieving all required level records."
        self.RECOGNITION_TYPE_ERROR_GET_ALL = "Error retrieving all recognition type records."
        self.SECTOR_ERROR_GET_ALL = "Error retrieving all sectors records."
        self.SUB_SECTOR_ERROR_GET_ALL = "Error retrieving all subsectors records."
        self.PPCN_ERROR_GET_ALL = "Error retrieving all PPCN records."
        self.PPCN_DOES_NOT_EXIST = "PPCN does not exist."
        self.PPCN_FILE_DOES_NOT_EXIST = "PPCN file does not exist."
        self.INVALID_STATUS_TRANSITION = "Invalid ppcn state transition."
        self.INVALID_USER_TRANSITION = "the user doesn´t have permission for this transition"
        self.INVALID_CURRENT_STATUS = "Invalid current ppcn status."
        self.NO_PATCH_DATA_PROVIDED = "No PATCH data provided."
        self.COMMENT_NOT_ASSIGNED = "The provided comment could not be assigned correctly."
        self.PPCN_ERROR_EMPTY_OVV_LIST = "Empty OVV list"
        self.STATE_HAS_NO_AVAILABLE_TRANSITIONS = "State has no available transitions."
        self.ASSING_GEI_ACTIVITY_TYPES = "Error assigning gei activity types."
        self.CREATING_GEI_ORGANIZATION = "Error creating gei organization."
        self.CONTACT_NOT_MATCH_ERROR = "The contact of the organization doesn't match the one registered."
        self.GEI_ORGANIZATION_DOES_NOT_EXIST = "Gei Organization doesn't exist"



    # serialized objects
    def get_serialized_geographic_level(self, request):

        geographic_level_data = {
            'level_es': request.data.get('level'),
            'level_en': request.data.get('level')
        }
        serializer = GeographicLevelSerializer(data=geographic_level_data)
        return serializer

    def get_serialized_contact(self, data, contact = False):

        contact_data = {
            'full_name': data.get('contact').get('full_name'),
            'job_title': data.get('contact').get('job_title'),
            'email': data.get('contact').get('email'),
            'phone': data.get('contact').get('phone'),
        }
       
        if contact:
            serializer = ContactSerializer(contact, data=contact_data)
        else:
            serializer = ContactSerializer(data = contact_data)
        return serializer

    def get_serialized_change_log(self, ppcn_id, previous_status_id, current_status_id, user):
        change_log_data = {
            'ppcn': ppcn_id,
            'previous_status': previous_status_id,
            'current_status': current_status_id,
            'user': user
        }
        serializer = ChangeLogSerializer(data=change_log_data)
        return serializer


    def get_serialized_gei_organization(self, request, gei_organization = False):
        
        gei_organization_data = { 
            'ovv': request.data.get('gei_organization').get('ovv'),
            'emission_ovv_date': request.data.get('gei_organization').get('emission_ovv_date'),
            'report_year': request.data.get('gei_organization').get('report_year'),
            'base_year': request.data.get('gei_organization').get('base_year')
        }

        if gei_organization:
            serializer = GeiOrganizationSerializer(gei_organization ,data=gei_organization_data)
        else:
            serializer = GeiOrganizationSerializer(data=gei_organization_data)
        return serializer


    def get_serialized_organization(self, request ,contact_id, organization = False):
        organization_data = {
            'name': request.data.get('organization').get('name'),
            'representative_name': request.data.get('organization').get('representative_name'),
            'phone_organization': request.data.get('organization').get('phone_organization'),
            'postal_code': request.data.get('organization').get('postal_code'),
            'fax': request.data.get('organization').get('fax'),
            'address': request.data.get('organization').get('address'),
            'contact': contact_id,
            'ciiu': request.data.get('organization').get('ciiu'),
        }
        if organization:
            serializer = OrganizationSerializer(organization ,data=organization_data)
        else:
            serializer = OrganizationSerializer(data=organization_data)
        return serializer

    def get_serialized_ppcn(self, request, organization_id = None, gei_organization_id = None, ppcn = False):
        ppcn_data = {
            'organization': organization_id,
            'gei_organization': gei_organization_id,
            'geographic_level': request.data.get('geographic_level'), 
            'required_level': request.data.get('required_level'), 
            'recognition_type':request.data.get('recognition_type'),
            'user':request.data.get('user')
        }
        if ppcn:
            serializer = PPCNSerializer(ppcn ,data=ppcn_data)
        else:
            serializer = PPCNSerializer(data=ppcn_data)
        return serializer

    def get_serialized_PPCCFile(self, file, request, ppcnFile = False):
        ppcnFileData = {
            'user': request.user.id,
            'file':file, 
            'ppcn_form':request.data.get('ppcn_form')
        }
        if ppcnFile:
            serializer = PPCNFileSeriaizer(ppcnFile, data=ppcnFileData)
        else:
            serializer = PPCNFileSeriaizer(data=ppcnFileData)
        return serializer

    def get_serialized_gei_activity_type(self, data):
        activity_type_data = {

            'activity_type': data.get('activity_type'),
            'sub_sector': data.get('sub_sector'),
            'sector':  data.get('sector')
        }
        serializer = GeiActivityTypeSerializer(data=activity_type_data)
        return serializer



    def get_all_geographic_level(self, language):

        try:
            form = [
                {
                    'id': l.id,
                    'level': l.level_es if language == 'es' else l.level_en
                } for l in GeographicLevel.objects.all()
            ]
            result = (True, form)

        except GeographicLevel.DoesNotExist:
            result = (False, self.LEVEL_ERROR_GET_ALL)
        return result

    def get_all_required_level(self, language):
        try:
            form = [
                {
                    'id': l.id,
                    'level_type': l.level_type_en if language == "en" else l.level_type_es
                }for l in RequiredLevel.objects.all()
            ] 
            
            result = (True, form)
        except RequiredLevel.DoesNotExist:
            result = (False, self.GEOGRAPHIC_LEVEL_ERROR_GET_ALL)
        return result

    def get_all_recognition_type(self, language):
        try:
            recognition = [
                {
                    'id': r.id,
                    'recognition_type': r.recognition_type_en if language == "en" else r.recognition_type_es
                }for r in RecognitionType.objects.all()
            ]
            result = (True, recognition)
        except RecognitionType.DoesNotExist:
            result = (False, self.RECOGNITION_TYPE_ERROR_GET_ALL)
        return result

    def get_all_sector(self, id ,language):
        try:
            sector = [
                {
                    'id': s.id,
                    'name': s.name_en if language == "en" else s.name_es
                }for s in Sector.objects.filter(geographicLevel_id = id)
            ]
            result = (True, sector)
        except Sector.DoesNotExist:
            result = (False, self.SECTOR_ERROR_GET_ALL)
        return result

    def get_all_sub_sector(self, sector, language):
        try:
            subsector = [
                {
                    'id': s.id,
                    'name': s.name_en if language == "en" else s.name_es
                } for s in SubSector.objects.filter(sector=sector)
            ]
            result = (True, subsector)
        except SubSector.DoesNotExist:
            result = (False, self.SUB_SECTOR_ERROR_GET_ALL)
        return result

    def get_all_ovv(self):
        try:
            ovv_list = [
                {
                    "id": o.id,
                    "email": o.email,
                    "phone": o.phone,
                    "name": o.name
                } for o in OVV.objects.all()
            ]
            result = (True, ovv_list)

        except OVV.DoesNotExist:
            result = (False, {"error": self.PPCN_ERROR_EMPTY_OVV_LIST})
        return result

    def get_one_organization(self, pk, language):
        try:
            org = Organization.objects.get(id=pk)
            organization_data = [
                {
                    'id': org.id,
                    'name': org.name,
                    'representative_name': org.representative_name,
                    'postal_code': org.postal_code,
                    'fax': org.fax,
                    'address': org.address,
                    'ciiu': org.ciiu,
                    'contact':{

                        'id' : org.contact.id,
                        'full_name': org.contact.full_name,
                        'job_title': org.contact.job_title,
                        'phone': org.contact.phone,
                        'email': org.contact.email
                    }
                }
            ]
            result = (True, organization_data)
        except Organization.DoesNotExist:
            result = (False, self.ORGANIZATION_DOES_NOT_EXIST)
        return result

    def create_organization(self, request):
        
        serialized_contact = self.get_serialized_contact( request.data.get('organization') ) 
        if serialized_contact.is_valid():
            contact = serialized_contact.save()
            serialized_organization = self.get_serialized_organization(request, contact.id)
            if serialized_organization.is_valid():
                organization = serialized_organization.save()
                result = (True, organization)
            else:
                errors = serialized_organization.errors
                result = (False, errors)
        else:
            errors = serialized_contact.errors
            result = (False, errors)
            
        return result

    def update_organization(self, request, id):

        contact_id = request.data.get('organization').get('contact').get('id')
        organization = Organization.objects.get(pk=id)
        result = (False, self.ORGANIZATION_DOES_NOT_EXIST)
        if organization != None:
            if not str(organization.contact.id) == str(contact_id):
                result = (False, self.CONTACT_NOT_MATCH_ERROR)
                return result
            
            contact = Contact.objects.get(id=contact_id)
            contact_serialized = self.get_serialized_contact(request.data.get('organization'), contact)

            if contact_serialized.is_valid():
                contact_serialized.save()
                serialized_organization = self.get_serialized_organization(request, contact_id, organization)
                if serialized_organization.is_valid():
                    organization = serialized_organization.save()
                    result = (True, organization)
                else:
                    result = (False, serialized_organization.error)
            else:

                result = (False, contact_serialized.errors)

        return result

    def delete_organization(self, pk):
        try:
            org = Organization.objects.get(id=pk)
            org.delete()
            result = True
        except:
            result = False
        return result

    def get_all(self, request, language, user = False):
        try:

            ppcn_registries = PPCN.objects.all() if not user else PPCN.objects.filter(user=request.user).all()
            ppcn_data = [
                {
                    'id': pp.id,
                    'organization': {
                        'id' : pp.organization.id,
                        'name' : pp.organization.name,
                        'representative_name' : pp.organization.representative_name,
                        'phone_organization' : pp.organization.phone_organization,
                        'postal_code' : pp.organization.postal_code,
                        'fax' : pp.organization.fax,
                        'address' : pp.organization.address,
                        'ciiu' : pp.organization.ciiu,
                        'contact' : 
                        {
                            'id' : pp.organization.contact.id,
                            'full_name' : pp.organization.contact.full_name,
                            'job_title' : pp.organization.contact.job_title,
                            'email' : pp.organization.contact.email,
                            'phone' : pp.organization.contact.phone
                        }
                    },
                    'geographic_level':{
                        'id' : pp.geographic_level.id,
                        'level' : pp.geographic_level.level_es if language == 'es' else pp.geographic_level.level_en

                    },
                    'required_level': {
                        'id' : pp.required_level.id,
                        'level_type' :  pp.required_level.level_type_es if language == 'es' else pp.required_level.level_type_en
                    },
                    'recognition_type': {
                        'id' : pp.recognition_type.id,
                        'recognition_type' : pp.recognition_type.recognition_type_es if language == 'es' else pp.recognition_type.recognition_type_en
                    },
                    'gei_organization':{
                        'id': pp.gei_organization.id, 
                        'ovv': {
                            'id': pp.gei_organization.ovv.id,
                            'name':  pp.gei_organization.ovv.name,
                            'email': pp.gei_organization.ovv.email,
                        },
                        'emission_ovv_date': pp.gei_organization.emission_ovv_date, 
                        'report_year': pp.gei_organization.report_year, 
                        'base_year': pp.gei_organization.base_year, 
                        'gei_activity_types': [
                            {
                                'id': gei_activity_type.id,
                                'sector': gei_activity_type.sector.name_es if language == 'es' else gei_activity_type.sector.name_en,
                                'sub_sector': gei_activity_type.sub_sector.name_es if language == 'es' else gei_activity_type.sub_sector.name_en,
                                'activity_type': gei_activity_type.activity_type

                            } for gei_activity_type in  pp.gei_organization.gei_activity_types.all()
                        ]
                    } 
                    if pp.gei_organization else None, 
                    'comments':[
                        {
                            'id': comment.id,
                            'comment': comment.comment
                        } for comment in pp.comments.all()
                    ],
                    'fsm_state': pp.fsm_state,
                    'next_state': self.next_action(pp),
                    'created': pp.created,
                    'updated': pp.updated,
                    'ppcn_files': self._get_ppcn_files_list(pp.files.all()),
                    'file': self._get_files_list([f.files.all() for f in pp.workflow_step.all()]),
                    'user': pp.user.id
                } for pp in ppcn_registries
            ]
            result = (True, ppcn_data)
        except Sector.DoesNotExist:
            result = (False, self.PPCN_ERROR_GET_ALL)
        return result


    def create_change_log_entry(self, ppcn, previous_status, current_status, user):
        serialized_change_log = self.get_serialized_change_log(ppcn.id, previous_status, current_status, user)
        if serialized_change_log.is_valid():
            serialized_change_log.save()
            result = (True, serialized_change_log.data)
        else:
            result = (False, serialized_change_log.errors)
        return result

    def assign_gei_activity_types(self, request, gei_organization):

        gei_activity_types_list = request.data.get('gei_activity_types')
        errors = [self.ASSING_GEI_ACTIVITY_TYPES]
        result_status = True
        for gei_activity_type in gei_activity_types_list:
            serialized_gei_activity_type = self.get_serialized_gei_activity_type(gei_activity_type)
            if serialized_gei_activity_type.is_valid():
                gei_activity_type = serialized_gei_activity_type.save()
                gei_organization.gei_activity_types.add(gei_activity_type)
            else:
                result_status = False
                errors.append(serialized_gei_activity_type.errors)
        
        if result_status:
            result = (True, gei_organization)

        else:
            result = (False, errors)

        return result

    def create_gei_organization(self, request):

        serialized_gei_organization = self.get_serialized_gei_organization(request) 
        if serialized_gei_organization.is_valid():
            gei_organization = serialized_gei_organization.save()
            if request.data.get('gei_activity_types') != None:

                gei_activity_types_status, gei_activity_types_data = self.assign_gei_activity_types(request, gei_organization)

                if gei_activity_types_status:
                    result = (True, gei_organization)
                else:
                    result = (False, gei_activity_types_data)
            else:
                result = (False, self.ASSING_GEI_ACTIVITY_TYPES)
        else:
            result = (False, serialized_gei_organization.errors)
            
        return result
    
    def update_gei_organization(self, request, id):

        gei_organization = GeiOrganization.objects.get(pk=id)
        if gei_organization == None:
            return (False, self.GEI_ORGANIZATION_DOES_NOT_EXIST)

        serialized_gei_organization = self.get_serialized_gei_organization(request, gei_organization) 

        if serialized_gei_organization.is_valid():
            gei_organization = serialized_gei_organization.save()

            if request.data.get('gei_activity_types') != None:
                gei_organization.gei_activity_types.clear()
                gei_activity_types_status, gei_activity_types_data = self.assign_gei_activity_types(request, gei_organization)

                if gei_activity_types_status:
                    result = (True, gei_organization)
                else:
                    result = (False, gei_activity_types_data)
            else:
                result = (False, self.ASSING_GEI_ACTIVITY_TYPES)
        else:
            result = (False, serialized_gei_organization.errors)
            
        return result
        
                
        

    def create(self, request):

        errors =[]
        valid_relations = []
        organization_id, gei_organization_id = None, None

        if request.data.get('organization') != None:
            organization_status, organization_detail= self.create_organization(request)
            valid_relations.append(organization_status)
            if organization_status: organization_id = organization_detail.id
            else: errors.append(organization_detail)

        if request.data.get('gei_organization') != None:
            gei_organization_status, gei_organization_detail = self.create_gei_organization(request)
            valid_relations.append(gei_organization_status)
            if gei_organization_status: gei_organization_id = gei_organization_detail.id
            else: errors.append(gei_organization_detail)

        if not valid_relations.count(False):
            ## Change logic here!!
            serialized_ppcn = self.get_serialized_ppcn(request, organization_id, gei_organization_id)
            if serialized_ppcn.is_valid():
                ppcn = serialized_ppcn.save()
                ppcn_previous_status = ppcn.fsm_state
                if not has_transition_perm(ppcn.submit, request.user):
                    errors.append(self.INVALID_USER_TRANSITION)
                    result = (False, errors)
                else:
                    ppcn.submit()
                    ppcn.save()
                    self.create_change_log_entry(ppcn, ppcn_previous_status, ppcn.fsm_state, request.data.get('user'))
                    result = (True, PPCNSerializer(ppcn).data)
            else:
                errors.append(serialized_ppcn.errors)
                result = (False, errors)
        else:
            result = (False, errors)
            
        return result

    def next_action(self, ppcn):
        result = {'states': False, 'required_comments': False}
        # change for transitions method available for users
        transitions = ppcn.get_available_fsm_state_transitions()
        states = []
        for transition in  transitions:
            states.append(transition.target)
        result['states'] = states if len(states) else False
        result['required_comments'] = True if len(states) > 1 else False
            
        return result



    def get(self, id ,language = 'en'):
        try:
            pp = PPCN.objects.get(id=id)
            ppcn_data = {
                    'id': pp.id,
                    'organization': {
                        'id' : pp.organization.id,
                        'name' : pp.organization.name,
                        'representative_name' : pp.organization.representative_name,
                        'phone_organization' : pp.organization.phone_organization,
                        'postal_code' : pp.organization.postal_code,
                        'fax' : pp.organization.fax,
                        'address' : pp.organization.address,
                        'ciiu' : pp.organization.ciiu,
                        'contact' :
                        {
                            'id' : pp.organization.contact.id,
                            'full_name' : pp.organization.contact.full_name,
                            'job_title' : pp.organization.contact.job_title,
                            'email' : pp.organization.contact.email,
                            'phone' : pp.organization.contact.phone
                        }
                    },
                    'geographic_level':{
                        'id' : pp.geographic_level.id,
                        'level' : pp.geographic_level.level_es if language == 'es' else pp.geographic_level.level_en

                    },
                    'required_level': {
                        'id' : pp.required_level.id,
                        'level_type' :  pp.required_level.level_type_es if language == 'es' else pp.required_level.level_type_en
                    },
                    'recognition_type': {
                        'id' : pp.recognition_type.id,
                        'recognition_type' : pp.recognition_type.recognition_type_es if language == 'es' else pp.recognition_type.recognition_type_en
                    },
                    'gei_organization':{
                        'id': pp.gei_organization.id, 
                        'ovv': {
                            'id': pp.gei_organization.ovv.id,
                            'name':  pp.gei_organization.ovv.name,
                            'email': pp.gei_organization.ovv.email,
                        },
                        'emission_ovv_date': pp.gei_organization.emission_ovv_date, 
                        'report_year': pp.gei_organization.report_year, 
                        'base_year': pp.gei_organization.base_year,
                        'gei_activity_types': [
                            {
                                'id': gei_activity_type.id,
                                'sector': {
                                    'id': gei_activity_type.sector.id,
                                    'name' : gei_activity_type.sector.name_es if language == 'es' else gei_activity_type.sector.name_en
                                },
                                'sub_sector':{
                                    'id' : gei_activity_type.sub_sector.id,
                                    'name': gei_activity_type.sub_sector.name_es if language == 'es' else gei_activity_type.sub_sector.name_en
                                },
                                'activity_type': gei_activity_type.activity_type

                            } for gei_activity_type in  pp.gei_organization.gei_activity_types.all()
                        ]
                    } if pp.gei_organization else None, 
                    'comments': [
                        {
                            'id': comment.id,
                            'comment': comment.comment
                        } for comment in pp.comments.all()
                    ],
                    'created': pp.created,
                    'updated': pp.updated,
                    'ppcn_files': self._get_ppcn_files_list(pp.files.all()),
                    'file': self._get_files_list([f.files.all() for f in pp.workflow_step.all()]),
                    'fsm_state': pp.fsm_state,
                    'next_state': self.next_action(pp),
                    'user': pp.user.id,
                }
            result = (True, ppcn_data)
        except Sector.DoesNotExist:
            result = (False, self.PPCN_DOES_NOT_EXIST)
        return result
    
    def delete(self, id):
        try:
            pp = PPCN.objects.get(id=id)
            pp.delete()
            result = (True, {"Result":"PPCN has been delete"})
        except:
            result = (False, {"Result":"PPCN has not been delete"})
        return result

    def update(self, id, request):
        errors =[]
        valid_relations = []
        
        ppcn = PPCN.objects.get(pk=id)
        gei_organization_id, organization_id = None, None
        
        if request.data.get('organization') != None:
            organization_id = request.data.get('organization').get('id')
            if organization_id != None:
                organization_status, organization_detail= self.update_organization(request, organization_id)
            else:
                organization_status, organization_detail= self.create_organization(request)
            valid_relations.append(organization_status)
            if organization_status: organization_id = organization_detail.id
            else: errors.append(organization_detail)

        if request.data.get('gei_organization') != None:
            gei_organization_id = request.data.get('gei_organization').get('id')
            if gei_organization_id != None:
                gei_organization_status, gei_organization_detail = self.update_gei_organization(request, gei_organization_id)
            else:
                gei_organization_status, gei_organization_detail = self.create_gei_organization(request)
            valid_relations.append(gei_organization_status)
            if gei_organization_status: gei_organization_id = gei_organization_detail.id
            else: errors.append(gei_organization_detail)

        result = (False, errors)        
        if not valid_relations.count(False):

            serialized_ppcn = self.get_serialized_ppcn(request, organization_id, gei_organization_id, ppcn)
            if serialized_ppcn.is_valid():
                ppcn = serialized_ppcn.save()
                ppcn_previous_status = ppcn.fsm_state
                if not has_transition_perm(ppcn.update_by_request_DCC):
                    errors.append(self.INVALID_STATUS_TRANSITION)
                ppcn.update_by_request_DCC()
                ppcn.save()
                self.create_change_log_entry(ppcn, ppcn_previous_status, ppcn.fsm_state, request.data.get('user'))
            
                result = (True, PPCNSerializer(ppcn).data)
            else:
                errors = serialized_ppcn.errors
                result = (False, errors)
           
        return result

    def post_PPCNFILE(self, request):
        result = []
        for f in request.data.getlist("files[]"):
            serialized_ppcn_file = self.get_serialized_PPCCFile(f, request)
            if serialized_ppcn_file.is_valid():
                

                result.append(PPCNFileSeriaizer(serialized_ppcn_file.save()).data)
            else:
                errors = serialized_ppcn_file.errors
                return (False, errors)
        return  (True, result)

    def get_file_content(self, file_id):
        ppcn_file = PPCNWorkflowStepFile.objects.get(id=file_id)
        path, filename = os.path.split(ppcn_file.file.name)
        return  (filename, BytesIO(self.storage.get_file(ppcn_file.file.name)))

    def get_ppcn_file_content(self, file_id):
        ppcn_file = PPCNFile.objects.get(id=file_id)
        path, filename = os.path.split(ppcn_file.file.name)
        return  (filename, BytesIO(self.storage.get_file(ppcn_file.file.name)))

    def download_file(self, id, file_id):
        return self.get_file_content(file_id)

    def download_ppcn_file(self, id, file_id):
        return self.get_ppcn_file_content(file_id)

    def _get_files_list(self, file_list):
        file_list = [file_list[0].union(q) for q in file_list[1:]] if len(file_list) > 1 else file_list
        file_list = file_list[0] if len(file_list) > 0 else file_list
        return [{'name': self._get_filename(f.file.name), 'file': self._get_file_path(str(f.workflow_step.ppcn.id), str(f.id))} for f in file_list ]

    def _get_ppcn_files_list(self, file_list):
        return [{'name': self._get_filename(f.file.name), 'file': self._get_ppcn_file_path(str(f.ppcn_form.id), str(f.id))} for f in file_list.all()]

    def _get_file_path(self, ppcn_id, ppcn_file_id):
        url = reverse("get_ppcn_file_version", kwargs={'id': ppcn_id, 'ppcn_file_id': ppcn_file_id})
        return url

    def _get_ppcn_file_path(self, ppcn_id, ppcn_file_id):
        url = reverse("get_ppcn_file", kwargs={'id': ppcn_id, 'ppcn_file_id': ppcn_file_id})
        return url

    def _get_filename(self, filename):
        fpath, fname = os.path.split(filename)
        return fname

    def get_form_ppcn(self, geographicLevel_id, language):
        try:
            required_evel = [
                {
                    'id': l.id,
                    'level': l.level_type_en if language == "en" else l.level_type_es
                } for l in RequiredLevel.objects.all()
            ]
            recognition_type = [
                {
                    'id': r.id,
                    'recognition': r.recognition_type_en if language == "en" else r.recognition_type_es
                } for r in RecognitionType.objects.all()
            ]

            sectors = self.get_all_sector(geographicLevel_id, language)[1]
            ovvs = self.get_all_ovv()[1]

            form_list = {
                'required_level': required_evel,
                'recognition_type': recognition_type,
                'sector': sectors,
                'ovv':ovvs,
            }
            result = (True, form_list)
        except RequiredLevel.DoesNotExist:
            result = (False, self.REQUIRED_LEVEL_ERROR_GET_ALL)
        return result

    def getReviewStatus(self, id):
        return ReviewStatus.objects.get(pk=id)

    def get_change_log(self, id):
        try:
            ppcn = PPCN.objects.get(id=id)
            change_log_content = []
            for log in ChangeLog.objects.filter(ppcn=ppcn.id):
                change_log_data = {
                    'date': log.date,
                    'ppcn': log.ppcn.id,
                    'previous_state': log.previous_status,
                    'current_status': log.current_status,
                    'user': log.user.id
                }
                change_log_content.append(change_log_data)
            result = (True, change_log_content)
        except PPCN.DoesNotExist:
            result = (False, self.PPCN_DOES_NOT_EXIST)
        return result

    def assign_comment(self, request, ppcn):
        comment_result_status, comment_result_data = workflow_service.create_comment(request)
        if comment_result_status:
            comment = comment_result_data
            ppcn.comments.add(comment)
        return comment_result_status

    def update_fsm_state(self, next_state, ppcn,user):
        result = (False, self.INVALID_STATUS_TRANSITION)
        # --- Transition ---
        # source -> target
        transitions = ppcn.get_available_fsm_state_transitions()
        states = {}
        for transition in  transitions:
            states[transition.target] = transition

        states_keys = states.keys()
        if len(states_keys) <= 0: result = (False, self.STATE_HAS_NO_AVAILABLE_TRANSITIONS)

        if next_state in states_keys:
            state_transition= states[next_state]
            transition_function = getattr(ppcn ,state_transition.method.__name__)

            if has_transition_perm(transition_function,user):
                transition_function()
                ppcn.save()
                result = (True, PPCNSerializer(ppcn).data)
            else: result = (False, self.INVALID_STATUS_TRANSITION)
            
        
        return result

    def patch(self, id, request):
        ppcn =  PPCN.objects.get(id=id)
        if(request.data.get('fsm_state')):
            patch_data = {
                'review_count': ppcn.review_count + 1
            }
            serialized_ppcn = PPCNSerializer(ppcn, data=patch_data, partial=True)
            if serialized_ppcn.is_valid():
                ppcn_previous_status = ppcn.fsm_state
                ppcn = serialized_ppcn.save()
                update_state_status, update_state_data = self.update_fsm_state(request.data.get('fsm_state'), ppcn,request.user)
                if update_state_status:
                    self.create_change_log_entry(ppcn,ppcn_previous_status,ppcn.fsm_state,request.data.get('user'))
                    result = (True, update_state_data)
                else:
                    result = (False, update_state_data)
                    return result
            if request.data.get('comment'):
                comment_status = self.assign_comment(request, ppcn)
                if comment_status:
                    result = (True, PPCNSerializer(ppcn).data)
                else:
                    result = (False, self.COMMENT_NOT_ASSIGNED)
        else:
            result = (False, self.NO_PATCH_DATA_PROVIDED)

        return result
