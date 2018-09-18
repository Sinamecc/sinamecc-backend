from ppcn.models import Organization, GeographicLevel, RequiredLevel, RecognitionType, Sector, SubSector, PPCN, PPCNFile
from ppcn.views import *
from mitigation_action.models import Contact
from mitigation_action.serializers import ContactSerializer
import json
from ppcn.serializers import *
from ppcn.workflow_steps.models import PPCNWorkflowStepFile
from rest_framework.parsers import JSONParser
import datetime
import uuid
from django_fsm import can_proceed
from io import BytesIO
from general.storages import S3Storage
from django.http import FileResponse
from django.urls import reverse
import os
import pdb
from general.services import EmailServices
email_sender  = "sinamecc@grupoincocr.com" ##change to sinamecc email
ses_service = EmailServices(email_sender)
from workflow.models import ReviewStatus

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
        self.NO_PATCH_DATA_PROVIDED = "No PATCH data provided."


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

    def get_serialized_ppcn(self, request, organization_id, ppcn = False):
        ppcn_data = {
            'organization': organization_id,
            'geographicLevel': request.data.get('geographicLevel'), 
            'requiredLevel': request.data.get('requiredLevel'), 
            'sector': request.data.get('sector'),
            'subsector': request.data.get('subsector'), 
            'recognitionType':request.data.get('recognitionType'),
            'base_year':request.data.get('base_year'),
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
            result (False, self.LEVEL_ERROR_GET_ALL)
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
            result (False, self.GEOGRAPHIC_LEVEL_ERROR_GET_ALL)
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
            result (False, self.RECOGNITION_TYPE_ERROR_GET_ALL)
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
            result (False, self.SECTOR_ERROR_GET_ALL)
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

    def post_organization(self, request):
        
        serialized_contact = self.get_serialized_contact( request.data.get('organization') ) 
        if serialized_contact.is_valid():
            contact = serialized_contact.save()
            serialized_organization = self.get_serialized_organization(request, contact.id)
            if serialized_organization.is_valid():
                organization = serialized_organization.save()
                result = (True, OrganizationSerializer(organization).data)
            else:
                errors = serialized_organization.errors
                result = (False, errors)
        else:
            errors = serialized_contact.errors
            result = (False, errors)
        return result

    def put_organization(self, request, pk):
        errors = []
        contact_id = request.data.get('contact').get('id')
        contact = Contact.objects.get(id=contact_id)
        contact_serialized = self.get_serialized_contact(request.data.get('organization'), contact)
        if contact_serialized.is_valid():
            contact_serialized.save()
            organization = Organization.objects.get(id=pk)
            serialized_organization = self.get_serialized_organization(request, contact_id, organization)
            if serialized_organization.is_valid():
                    organization = serialized_organization.save()
                    result = (True, OrganizationSerializer(organization).data)
            else:
                errors.append(serialized_organization.errors)
                result = (False, errors)
        else:
            errors.append(contact_serialized.errors)
            result = (False, errors)
        return result

    def delete_organization(self, pk):
        try:
            org = Organization.objects.get(id=pk)
            org.delete()
            result = True
        except:
            result = False
        return result

    def get_all(self, language):
        try:
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
                    'geographicLevel':{
                        'id' : pp.geographicLevel.id,
                        'level' : pp.geographicLevel.level_es if language == 'es' else pp.geographicLevel.level_en

                    },
                    'requiredLevel': {
                        'id' : pp.requiredLevel.id,
                        'level_type' :  pp.requiredLevel.level_type_es if language == 'es' else pp.requiredLevel.level_type_en
                    },
                    'sector': {
                        'id': pp.sector.id,
                        'sector': pp.sector.name_es if language == 'es' else pp.sector.name_en
                    },
                    'subsector': {
                        'id' : pp.subsector.id,
                        'name' : pp.subsector.name_es if language == 'es' else pp.subsector.name_en
                    },
                    'recognitionType': {
                        'id' : pp.recognitionType.id,
                        'recognition_type' : pp.recognitionType.recognition_type_es if language == 'es' else pp.recognitionType.recognition_type_es
                    },
                    'base_year': pp.base_year,
                    'fsm_state': pp.fsm_state,
                    'created': pp.created,
                    'updated': pp.updated
                }for pp in PPCN.objects.all()
            ]
            result = (True, ppcn_data)
        except Sector.DoesNotExist:
            result (False, self.PPCN_ERROR_GET_ALL)
        return result


    def create_change_log_entry(self, ppcn, previous_status, current_status, user):
        serialized_change_log = self.get_serialized_change_log(ppcn.id, previous_status, current_status, user)
        if serialized_change_log.is_valid():
            serialized_change_log.save()
            result = (True, serialized_change_log.data)
        else:
            result = (False, serialized_change_log.errors)
        return result

    def create(self, request):

        errors =[]
        save_result, result_detail= self.post_organization(request)
        if save_result:
            organization_id = result_detail.get('id')
            serialized_ppcn = self.get_serialized_ppcn(request, organization_id)
            if serialized_ppcn.is_valid():
                ppcn = serialized_ppcn.save()
                ppcn_previous_status = ppcn.fsm_state
                if not can_proceed(ppcn.submit):
                    errors.append(self.INVALID_STATUS_TRANSITION)
                ppcn.submit()
                ppcn.save()
                self.create_change_log_entry(ppcn, ppcn_previous_status, ppcn.fsm_state, request.data.get('user'))
                
                result = (True, PPCNSerializer(ppcn).data)
            else:
                errors.append(serialized_ppcn.errors)
                result = (False, errors)

        else:
            result = (False, result_detail)
        return result

    def possible_next_state(self, current_fsm_state):
        result_arr = []
        if current_fsm_state == 'new':
            result_arr.append({
                'state': 'submitted'
            })
        elif current_fsm_state == 'submitted':
            result_arr.append({
                'state': 'evaluation_by_DCC'
            })
        elif current_fsm_state == 'evaluation_by_DCC':
            result_arr.append(
                {'state': 'accepted_request_by_DCC'}
            )
            result_arr.append(
                {'state': 'rejected_request'}
            )
        elif current_fsm_state == 'accepted_request_by_DCC':
            result_arr.append(
                {'state': 'evaluation_by_CA'}
            )
        elif current_fsm_state == 'evaluation_by_CA':
            result_arr.append(
                {'state': 'accepted_request_by_DCC'}
            )
            result_arr.append(
                {'state': 'rejected_request'}
            )
        elif current_fsm_state == 'rejected_request':
            result_arr.append(
                {'state': 'end'}
            )
        elif current_fsm_state == 'accepted_request_by_DCC':
            result_arr.append(
                {'state': 'send_recognition_certificate'}
            )
        return result_arr

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
                    'geographicLevel':{
                        'id' : pp.geographicLevel.id,
                        'level' : pp.geographicLevel.level_es if language == 'es' else pp.geographicLevel.level_en

                    },
                    'requiredLevel': {
                        'id' : pp.requiredLevel.id,
                        'level_type' :  pp.requiredLevel.level_type_es if language == 'es' else pp.requiredLevel.level_type_en
                    },
                    'sector':{
                        'id': pp.sector.id,
                        'sector': pp.sector.name_es if language == 'es' else pp.sector.name_en
                    },
                    'subsector': {
                        'id' : pp.subsector.id,
                        'name' : pp.subsector.name_es if language == 'es' else pp.subsector.name_en
                    },
                    'recognitionType': {
                        'id' : pp.recognitionType.id,
                        'recognition_type' : pp.recognitionType.recognition_type_es if language == 'es' else pp.recognitionType.recognition_type_es
                    },
                    'base_year': pp.base_year,
                    'created': pp.created,
                    'updated': pp.updated,
                    'file': self._get_files_list([f.files.all() for f in pp.workflow_step.all()]),
                    'fsm_state': pp.fsm_state,
                    'next_state': self.possible_next_state(pp.fsm_state)
                }
            result = (True, ppcn_data)
        except Sector.DoesNotExist:
            result (False, self.PPCN_ERROR_GET_ALL)
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

        errors = None
        ppcn = PPCN.objects.get(id=id)
        organization = Organization.objects.get(id=ppcn.organization.id)
        contact = Contact.objects.get(id=organization.contact.id)

        serialized_contact = self.get_serialized_contact(request.data.get('organization'), contact)
        if serialized_contact.is_valid():
            serialized_contact.save()
            serialized_organization = self.get_serialized_organization(request, contact.id, organization)
            if serialized_organization.is_valid():
                organization = serialized_organization.save()
                serialized_ppcn = self.get_serialized_ppcn(request, organization.id, ppcn)
                if serialized_ppcn.is_valid():
                    ppcn = serialized_ppcn.save()
                    result = (True, PPCNSerializer(ppcn).data)
                else:
                    errors = serialized_ppcn.errors
                    result = (False, errors)
            else:
                errors = serialized_organization.errors
                result = (False, errors)
        else:
            errors = serialized_contact.errors
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


    def download_file(self, id, file_id):
        return self.get_file_content(file_id)

    def _get_files_list(self, file_list):
        file_list = [file_list[0].union(q) for q in file_list[1:]] if len(file_list) > 1 else file_list
        file_list = file_list[0] if len(file_list) > 0 else file_list
        return [{'name': self._get_filename(f.file.name), 'file': self._get_file_path(str(f.workflow_step.ppcn.id), str(f.id))} for f in file_list ]

    def _get_file_path(self, ppcn_id, ppcn_file_id):
        url = reverse("get_ppcn_file_version", kwargs={'id': ppcn_id, 'ppcn_file_id': ppcn_file_id})
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

            form_list = {
                'required_level': required_evel,
                'recognition_type': recognition_type,
                'sector': sectors
            }
            result = (True, form_list)
        except RequiredLevel.DoesNotExist:
            result (False, self.REQUIRED_LEVEL_ERROR_GET_ALL)
        return result

    def sendNotification(self, recipient_list, subject, message_body):

        result = ses_service.send_notification(recipient_list, subject, message_body)
        
        return result
            
    def sendStatusNotification(self, recipient_list, subject, message_body, link):

        """first implementation"""
        subject = "PPCN: " + subject
        message_body += "\nlink: " + link

        result = self.sendNotification(recipient_list, subject, message_body)

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

    def update_fsm_state(self, next_state, ppcn):
        # --- Transition ---
        # submitted -> evaluation_by_DCC
        if next_state == 'evaluation_by_DCC':
            if not can_proceed(ppcn.evaluate_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            ppcn.evaluate_DCC()
            ppcn.save()
            result = (True, PPCNSerializer(ppcn).data)
        # --- Transition ---
        # submitted -> rejectd_request_by_DCC
        elif next_state == 'rejected_request':
            if not can_proceed(ppcn.rejected_request_by_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            ppcn.rejected_request_by_DCC()
            ppcn.save()
            result = (True, PPCNSerializer(ppcn).data)

        # --- Transition ---
        # evaluation_by_DCC -> accepted_request_by_DCC
        elif next_state == 'accepted_request_by_DCC':
            if not can_proceed(ppcn.accept_request_by_DCC):
                result = (False, self.INVALID_STATUS_TRANSITION)
            ppcn.accept_request_by_DCC()
            ppcn.save()
            result = (True, PPCNSerializer(ppcn).data)
        # --- Transition ---
        # submitted -> rejectd_request_by_CA
        elif next_state == 'rejected_request':
            if not can_proceed(ppcn.rejected_request_by_CA):
                result = (False, self.INVALID_STATUS_TRANSITION)
            ppcn.rejected_request_by_CA()
            ppcn.save()
            result = (True, PPCNSerializer(ppcn).data)
        # --- Transition ---
        # accepted_request_by_DCC -> evaluation_by_CA
        elif next_state == 'evaluation_by_CA':
            if not can_proceed(ppcn.evaluate_by_CA):
                result = (False, self.INVALID_STATUS_TRANSITION)
            ppcn.evaluate_by_CA()
            ppcn.save()
            result = (True, PPCNSerializer(ppcn).data)
        # --- Transition ---
        # evaluation_by_CA -> accept_request_by_CA
        elif next_state == 'accept_request_by_CA':
            if not can_proceed(ppcn.accept_request_by_CA):
                result = (False, self.INVALID_STATUS_TRANSITION)
            ppcn.accept_request_by_CA()
            ppcn.save()
            result = (True, PPCNSerializer(ppcn).data)

        # --- Transition ---
        # evaluation_by_CA -> accept_request_by_CA
        elif next_state == 'send_recognition_certificate':
            if not can_proceed(ppcn.send_recognition_certificate):
                result = (False, self.INVALID_STATUS_TRANSITION)
            ppcn.send_recognition_certificate()
            ppcn.save()
            result = (True, PPCNSerializer(ppcn).data)
        # --- Transition ---
        # rejected_request_by_CDD_and_CA -> end
        elif next_state == 'end':
            if not can_proceed(ppcn.end):
                result = (False, self.INVALID_STATUS_TRANSITION)
            ppcn.end()
            ppcn.save()
            result = (True, PPCNSerializer(ppcn).data)
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
                update_state_status, update_state_data = self.update_fsm_state(request.data.get('fsm_state'), ppcn)
                if update_state_status:
                    self.create_change_log_entry(ppcn,ppcn_previous_status,ppcn.fsm_state,request.data.get('user'))
                    result = (True, update_state_data)
                else:
                    result = (False, update_state_data)
            if request.data.get('comment'):
                comment_status = self.assign_comment(request, ppcn)
                if comment_status:
                    result = (True, PPCNSerializer(ppcn).data)
                else:
                    result = (False, self.COMMENT_NOT_ASSIGNED)
        else:
            result = (False, self.NO_PATCH_DATA_PROVIDED)
        return result
