from mccr.models import OVV
from mccr.serializers import OVVSerializer
from ppcn.models import Organization, GeographicLevel, RequiredLevel, RecognitionType, Sector,GeiOrganization, GeiActivityType, SubSector, PPCN, PPCNFile
from django.contrib.auth.models import *
from mitigation_action.serializers import ContactSerializer
from ppcn.serializers import *
from ppcn.workflow_steps.models import PPCNWorkflowStepFile
from django_fsm import has_transition_perm
from io import BytesIO
from general.storages import S3Storage
from django.urls import reverse
from general.services import EmailServices
from general.helpers.serializer import SerializersHelper
from workflow.models import ReviewStatus
from workflow.serializers import CommentSerializer
from django.contrib.auth import get_user_model
from workflow.services import WorkflowService
from django.db import transaction, DatabaseError
import os


email_sender  = "sinamec@grupoincocr.com" ##change to sinamecc email
ses_service = EmailServices(email_sender)
User = get_user_model()
workflow_service = WorkflowService()

class PpcnService():

    def __init__(self):
        self.storage = S3Storage()
        self._serialize_helper = SerializersHelper()
        self.GENERIC_CREATE_ERROR = "Error at the moment to create {}"
        self.ORGANIZATION_DOES_NOT_EXIST = "Organization does not exist."
        self.EMPTY_ORGANIZATION_ERROR = "Request doesn't have organization, contact organization or ciiu code"
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
        self.SERIALIZER_ERROR = "Cannot serialize {0}  because {1}"
        self.CREATING_GEI_ORGANIZATION = "Error creating gei organization."
        self.CONTACT_NOT_MATCH_ERROR = "The contact of the organization doesn't match the one registered."
        self.GEI_ORGANIZATION_DOES_NOT_EXIST = "Gei Organization doesn't exist"
        self.CIIU_CODE_SERIALIZER_ERROR = "Cannot serialize ciiu code because {0}"
        self.LIST_ERROR = "Was expected a {0} list into data"
        self.MISSING_FIELD = "Missing {0} field into request"
        self.FUNCTION_INSTANCE_ERROR = 'PPCNService does not have {0} function'
        self.ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'
        self.SEND_TO_REVIEW_ERROR = 'Error at the moment to send to review the ppcn form'
    

    # data checker 
    def _check_all_field_complete(self, ppcn_data):

        ## we need to validate which fields should be verified

        pass 
    
    # auxiliary functions
    def _create_sub_record(self, data, sub_record_name):
        
        create_function = f'_create_{sub_record_name}'

        if hasattr(self, create_function):
            function = getattr(self, create_function)
            record_status, record_detail = function(data)
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(create_function))

        return result

    
    def _create_related_record_list(self, data, related_record_name, related_instance):
        
        create_function = f'_create_{related_record_name}_list'

        if hasattr(self, create_function):
            
            function = getattr(self, create_function)
            record_status, record_detail = function(data, related_instance)
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(create_function))
        
        return result
    

    def _update_related_record_list(self, data, related_record_name, related_instance):
        
        update_function = f'_update_{related_record_name}_list'
        
        if hasattr(self, update_function):
            
            function = getattr(self, update_function)
            record_status, record_detail = function(data, related_instance)
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(update_function))
        
        return result


    def _update_sub_record(self, sub_record_name, record_for_updating, data):
        
        update_function = f'_update_{sub_record_name}'
        
        if hasattr(self, update_function):
          
            function = getattr(self, update_function)
        
            record_status, record_detail = function(record_for_updating, data)
          
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

    def _create_or_update_record_list(self, data, related_field, related_instance):
        
        result = (False, [])
        if hasattr(related_instance, related_field):

            if getattr(related_instance, related_field).all().count() == 0:
                record_status, record_data = self._create_related_record_list(data, related_field, related_instance)## field = sub_record_name

            else:
                ## change field(string) to object(model instance) 
                record_status, record_data = self._update_related_record_list(data, related_field, related_instance)

            result = (record_status, record_data)

        else:
            result = (True, self.ATTRIBUTE_INSTANCE_ERROR)

        return result


    def _increase_review_counter(self, ppcn):

        ppcn.review_count += 1;
        ppcn.save()

        result = (True, ppcn)

        return result 


    # serialized objects
    def _get_serialized_contact(self, data, contact = False):

        serializer = self._serialize_helper.get_serialized_record(ContactSerializer, data, record=contact)

        return serializer
        

    def _get_serialized_organization(self, data, organization = False):

        serializer = self._serialize_helper.get_serialized_record(OrganizationSerializer, data, record=organization)

        return serializer


    def _get_serialized_ppcn(self, data, ppcn=False):

        serializer = self._serialize_helper.get_serialized_record(PPCNSerializer, data, record=ppcn)

        return serializer


    def _get_serialized_organization_classification(self, data, organization_classification=False):

        serializer = self._serialize_helper.get_serialized_record(OrganizationClassificationSerializer, data, record=organization_classification)

        return serializer
    

    def _get_serialized_reduction(self, data, reduction=False):

        serializer = self._serialize_helper.get_serialized_record(ReductionSerializer, data, record=reduction, partial=True)

        return serializer
    

    def _get_serialized_carbon_offset(self, data, carbon_offset=False):

        serializer = self._serialize_helper.get_serialized_record(CarbonOffsetSerializer, data, record=carbon_offset, partial=True)

        return serializer


    def _get_serialized_gei_organization(self, data, gei_organization = False):

        serializer = self._serialize_helper.get_serialized_record(GeiOrganizationSerializer, data, record=gei_organization)

        return serializer


    def _get_serialized_biogenic_emission(self, data, biogenic_emission=False):

        serializer = self._serialize_helper.get_serialized_record(BiogenicEmissionSerializer, data, record=biogenic_emission)

        return serializer


    def _get_serialized_gas_report(self, data, gas_report=False):

        serializer = self._serialize_helper.get_serialized_record(GasReportSerializer, data, record=gas_report)

        return serializer


    def _get_serialized_gas_scope(self, data, gas_scope=False):

        serializer = self._serialize_helper.get_serialized_record(GasScopeSerializer, data, record=gas_scope)

        return serializer


    def _get_serialized_gas_removal(self, data, gas_removal=False):

        serializer = self._serialize_helper.get_serialized_record(GasRemovalSerializer, data, record=gas_removal, partial=True)

        return serializer


    def _get_serialized_organization_category(self, data, organization_category=False):
        serializer = self._serialize_helper.get_serialized_record(OrganizationCategorySerializer, data, record=organization_category)

        return serializer


    def _get_serialized_gei_activity_type(self, data , gei_actitvity_type=False):

        serializer = self._serialize_helper.get_serialized_record(GeiActivityTypeSerializer, data, record=gei_actitvity_type, partial=True)

        return serializer


    def _get_serialized_quantified_gases_list(self, data, gas_scope_id):

        data = [{**quantified_gas, 'gas_scope': gas_scope_id}  for quantified_gas in data]

        serializer = self._serialize_helper.get_serialized_record(QuantifiedGasSerializer, data, many=True)

        return serializer

    def _get_serialized_ciiu_code_list(self, data, organization_id):
        
        data = [{**ciiu_code, 'organization': organization_id}  for ciiu_code in data]
 
        serializer = self._serialize_helper.get_serialized_record(CIIUCodeSerializer, data, many=True)

        return serializer

    def _get_serialized_gei_activity_type_list(self, data, gei_organization_id):

        data = [{**gei_actitvity_type, 'gei_organization': gei_organization_id}  for gei_actitvity_type in data]

        serializer = self._serialize_helper.get_serialized_record(GeiActivityTypeSerializer, data, many=True)

        return serializer 
    
    def _get_serialized_reduction_list(self, data, organization_classification_id):

        data = [{**reduction, 'organization_classification': organization_classification_id}  for reduction in data]

        serializer = self._serialize_helper.get_serialized_record(ReductionSerializer, data, many=True)

        return serializer 
    
    def _get_serialized_gas_removal_list(self, data, ppcn_id):

        data = [{**gas_removal, 'ppcn': ppcn_id}  for gas_removal in data]

        serializer = self._serialize_helper.get_serialized_record(GasRemovalSerializer, data, many=True)

        return serializer 
    
    def _get_serialized_carbon_offset_list(self, data, organization_classification_id):

        data = [{**carbon_offset, 'organization_classification': organization_classification_id}  for carbon_offset in data]

        serializer = self._serialize_helper.get_serialized_record(CarbonOffsetSerializer, data, many=True)

        return serializer 
  
    def get_serialized_geographic_level(self, request):

        geographic_level_data = {
            'level_es': request.data.get('level'),
            'level_en': request.data.get('level')
        }
        serializer = GeographicLevelSerializer(data=geographic_level_data)
        return serializer


    
    def get_serialized_change_log(self, ppcn_id, previous_status_id, current_status_id, user_id):
        change_log_data = {
            'ppcn': ppcn_id,
            'previous_status': previous_status_id,
            'current_status': current_status_id,
            'user': user_id
        }
        serializer = ChangeLogSerializer(data=change_log_data)
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

    ## Create objects

    def _create_reduction(self, data):

        serialized_reduction = self._get_serialized_reduction(data)
        if serialized_reduction.is_valid():
            reduction = serialized_reduction.save()
            result = (True, reduction)
        else:
            result = (False, serialized_reduction.errors)

        return result
    

    def _create_organization_category(self, data):

        serialized_organization_category = self._get_serialized_organization_category(data)
        if serialized_organization_category.is_valid():
            organization_category = serialized_organization_category.save()
            result = (True, organization_category)
        else:
            result = (False, serialized_organization_category.errors)

        return result

    def _create_carbon_offset(self, data):

        serialized_carbon_offset = self._get_serialized_carbon_offset(data)
        if serialized_carbon_offset.is_valid():
            carbon_offset = serialized_carbon_offset.save()
            result = (True, carbon_offset)
        else:
            result = (False, serialized_carbon_offset.errors)

        return result

    
    def _create_reduction_list(self, data, organization_classification):

        result = (True, [])
        
        if isinstance(data, list):
            serialized_reduction_list = self._get_serialized_reduction_list(data, organization_classification.id)
            
            if  serialized_reduction_list.is_valid():
                reduction_list = serialized_reduction_list.save()
                result = (True, reduction_list)
            else:
                result = (False, self.SERIALIZER_ERROR.format('reductions',str(serialized_reduction_list.errors)))
        
        else:
            result = (False, self.LIST_ERROR.format('reductions'))

        
        return result
    
    def _create_gas_removal_list(self, data, ppcn):
        
        result = (True, [])
        
        if isinstance(data, list):
            serialized_gas_removal_list = self._get_serialized_gas_removal_list(data, ppcn.id)
            
            if  serialized_gas_removal_list.is_valid():
                gas_removal_list = serialized_gas_removal_list.save()
                result = (True, gas_removal_list)
            else:
                result = (False, self.SERIALIZER_ERROR.format('gas_removals',str(serialized_gas_removal_list.errors)))
        
        else:
            result = (False, self.LIST_ERROR.format('gas_removals'))

        
        return result

    
    def _create_carbon_offset_list(self, data, organization_classification):

        result = (True, [])
        
        if isinstance(data, list):
            serialized_carbon_offset_list = self._get_serialized_carbon_offset_list(data, organization_classification.id)
            
            if  serialized_carbon_offset_list.is_valid():
                carbon_offset_list = serialized_carbon_offset_list.save()
                result = (True, carbon_offset_list)
            else:
                result = (False, self.SERIALIZER_ERROR.format('carbon offset',str(serialized_carbon_offset_list.errors)))
        
        else:
            result = (False, self.LIST_ERROR.format('carbon offset'))

        
        return result


    def _create_organization_classification(self, data):

        validation_dict = {}
        # fk's of object organization_classification that have nested fields
        field_list = [] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field)

                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)

        if all(validation_dict):
            serialized_organization_classification = self._get_serialized_organization_classification(data)
            if serialized_organization_classification.is_valid():
                organization_classification = serialized_organization_classification.save()

                field_related_list = ['reduction', 'carbon_offset']
                validation_dict.clear()

                for field_related in field_related_list:
                    if data.get(field_related, False):
                        record_status, record_data = self._create_related_record_list(data.get(field_related), field_related, organization_classification)

                        dict_data = record_data if isinstance(record_data, list) else [record_data]
                        validation_dict.setdefault(record_status,[]).extend(dict_data)

                if all(validation_dict):
                    result = (True, organization_classification)
                else:
                    result = (False, validation_dict.get(False))

            else:
                result = (False, serialized_organization_classification.errors)
        else:
            result = (False, validation_dict.get(False))

        return result

    def _create_gei_activity_type_list(self, data, gei_organization):

        result = (True, [])
        
        if isinstance(data, list):
            serialized_gei_activity_type = self._get_serialized_gei_activity_type_list(data, gei_organization.id)
            
            if  serialized_gei_activity_type.is_valid():
                gei_activity_type = serialized_gei_activity_type.save()

                result = (True, gei_activity_type)
            else:
                result = (False, self.SERIALIZER_ERROR.format('gei activity types',str(serialized_gei_activity_type.errors)))
        
        else:
            result = (False, self.LIST_ERROR.format('gei activity types'))

        return result

    def _create_gei_organization(self, data):
        validation_dict = {}

        # fk's of object organization_classification that have nested fields
        field_list = ['gas_report', 'organization_category'] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field)

                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)

        if all(validation_dict):

            serialized_gei_organization = self._get_serialized_gei_organization(data) 
            if serialized_gei_organization.is_valid():
                gei_organization = serialized_gei_organization.save()

                field_related_list = ['gei_activity_type']
                validation_dict.clear()

                for field_related in field_related_list:
                    if data.get(field_related, False):
                        record_status, record_data = self._create_related_record_list(data.get(field_related), field_related, gei_organization)

                        dict_data = record_data if isinstance(record_data, list) else [record_data]
                        validation_dict.setdefault(record_status,[]).extend(dict_data)

                if all(validation_dict):
                    result = (True, gei_organization)
                else:
                    result = (False, validation_dict.get(False))

            else:
                result = (False, serialized_gei_organization.errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result

    def _create_biogenic_emission(self, data):

        serialized_biogenic_emission = self._get_serialized_biogenic_emission(data)
        if serialized_biogenic_emission.is_valid():
            biogenic_emission = serialized_biogenic_emission.save()
            result = (True, biogenic_emission)
        else:
            result = (False, serialized_biogenic_emission.errors)

        return result
    

    def _create_gas_removal(self, data):

        serialized_gas_removal = self._get_serialized_gas_removal(data)
        
        if serialized_gas_removal.is_valid():
            gas_removal = serialized_gas_removal.save()
            result = (True, gas_removal)
        else:
            result = (False, serialized_gas_removal.errors)

        return result

    def _create_contact(self, data):

        serialized_contact = self._get_serialized_contact(data)
        
        if serialized_contact.is_valid():
            contact = serialized_contact.save()
            result = (True, contact)
        else:
            result = (False, serialized_contact.errors)

        return result


    def _create_gas_scope(self, data, gas_report_id):

        gas_scope_list = []
        result = (True, gas_scope_list)
        for gas_scope in data:
            gas_scope['gas_report'] = gas_report_id
            quantified_gases_list = gas_scope.get('quantified_gases')

            if isinstance(quantified_gases_list, list):
                serialized_gas_scope = self._get_serialized_gas_scope(gas_scope)

                if serialized_gas_scope.is_valid():
                    gas_scope = serialized_gas_scope.save()
                    serialized_quantified_gases = self._get_serialized_quantified_gases_list(quantified_gases_list, gas_scope.id)

                    if serialized_quantified_gases.is_valid():
                        quantified_gases = serialized_quantified_gases.save()
                        
                    else:
                        result = (False, serialized_quantified_gases.errors)
                        break
                else:
                    result = (False, serialized_gas_scope.errors)
                    break
            else:
                result = (False, self.MISSING_FIELD.format('gas_scopes'))
                break

            gas_scope_list.append(gas_scope)

        return  result

    
    def _create_gas_report(self, data):

        validation_dict = {}
        # fk's of object organization_classification that have nested fields
        field_list = ['biogenic_emission'] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field)

                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)
        
        if all(validation_dict):
            serialized_gas_report = self._get_serialized_gas_report(data)
            if serialized_gas_report.is_valid():
                gas_report = serialized_gas_report.save()
                if data.get('gas_scopes', False):
                    gas_scope_status, gas_scope_data = self._create_gas_scope(data.get('gas_scopes'), gas_report.id)
                    if gas_scope_status:
                        result = (True, gas_report)
                    else:
                        result = (True, gas_scope_data)
                else:
                    result = (True, gas_report)             
            else:
                result = (False, serialized_gas_report.errors)
        else:
            result = (False, validation_dict.get(False))

        return result
    


    def _create_ciiu_code(self, data, organization_id):
 
        result = (True, [])

        if isinstance(data, list): 
            serializer = self._get_serialized_ciiu_code_list(data, organization_id)

            if serializer.is_valid():

                ciiu_code_list = serializer.save()

                result = (True, ciiu_code_list)

            else: 
                result = (False, self.CIIU_CODE_SERIALIZER_ERROR.format(str(serializer.errors)))

        else:
            result = (False, self.LIST_ERROR.format('ciiu_code'))
            
        return result

    def _create_organization(self, data):
        
        validation_dict = {}
   
        # fk's of object organization that have nested fields
        field_list = ['contact'] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field)
                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]

        if all(validation_dict):

            serialized_organization = self._get_serialized_organization(data)
            if serialized_organization.is_valid():
                organization = serialized_organization.save()

                organization_id =  organization.id

                ciiu_code_data = data.get("ciiu_code_list", [])

                serialized_ciiu_code_status, serialized_ciiu_code_data = self._create_ciiu_code(ciiu_code_data, organization_id)

                if serialized_ciiu_code_status:
                    result = (True, organization)
                else:
                    result = (serialized_ciiu_code_status, serialized_ciiu_code_data)

            else:
                errors = serialized_organization.errors
                result = (False, errors)
  
        else:
            result = (False, self.EMPTY_ORGANIZATION_ERROR)

        return result

    ## update funtion

    def _update_organization_category(self, organization_category, data):

        serialized_organization_category = self._get_serialized_organization_category(data, organization_category)
        if serialized_organization_category.is_valid():
            organization_category = serialized_organization_category.save()
            result = (True, organization_category)
        else:
            result = (False, serialized_organization_category.errors)

        return result


    def _update_biogenic_emission(self, biogenic_emission, data):

        serialized_biogenic_emission = self._get_serialized_biogenic_emission(data, biogenic_emission)
        if serialized_biogenic_emission.is_valid():
            biogenic_emission = serialized_biogenic_emission.save()
            result = (True, biogenic_emission)
        else:
            result = (False, serialized_biogenic_emission.errors)

        return result


    def _update_gas_removal(self, gas_removal, data):

        serialized_gas_removal = self._get_serialized_gas_removal(data, gas_removal)
        
        if serialized_gas_removal.is_valid():
            gas_removal = serialized_gas_removal.save()
            result = (True, gas_removal)
        else:
            result = (False, serialized_gas_removal.errors)

        return result
    
    def _update_gas_removal_list(self, data, ppcn):

        result = (True, [])
        
        if isinstance(data, list):

            gas_removal_list = ppcn.gas_removal.all()

            ## [{ id: json object }, {} , ...] data for updating gas_removal record
            gas_removal_data_list =  { gr.get('id'): gr for gr in  data if gr.get('id', False) }
            gas_removal_list_for_updating = gas_removal_list.filter(id__in = list(gas_removal_data_list.keys()))

            gas_removal_list_updated = {}
            for gas_removal in gas_removal_list_for_updating:

                record_status, record_data = self._update_gas_removal(gas_removal, gas_removal_data_list.get(gas_removal.id, {}))
                dict_data = record_data if isinstance(record_data, list) else [record_data]

                gas_removal_list_updated.setdefault(record_status,[]).extend(dict_data) 

            ## updating data - exclude  updated records
            data = [gr for gr in data if not gr.get('id', False)]
            serialized_gas_removal = self._get_serialized_gas_removal_list(data, ppcn.id)

            if  serialized_gas_removal.is_valid() and all(gas_removal_list_updated):
                new_gas_removal = serialized_gas_removal.save()
                gas_removal_list_for_deleting = gas_removal_list.exclude(
                    id__in = list(gas_removal_data_list.keys())
                ).exclude(
                    id__in=[gr.id for gr in new_gas_removal]
                )
                gas_removal_list_for_deleting.delete()

                result = (True, gas_removal_list)

            else:
                result = (False, self.SERIALIZER_ERROR.format('gas removal',
                    str(serialized_gas_removal.errors) if all(gas_removal_list_updated) else gas_removal_list_updated.get(False, [])))
                    
        else:
            result = (False, self.LIST_ERROR.format('gas_removal'))

        return result

    def _update_contact(self, contact, data):
        
        serialized_contact = self._get_serialized_contact(data, contact)
        
        if serialized_contact.is_valid():
            contact = serialized_contact.save()
            result = (True, contact)

        else:
            result = (False, serialized_contact.errors)

        return result

    def _update_ciiu_code(self, data, organization):
 
        result = (True, [])
        
        if isinstance(data, list): 
            serializer = self._get_serialized_ciiu_code_list(data, organization.id)

            if serializer.is_valid():

                organization.ciiu_code.all().delete()
                new_ciiu_code_list = serializer.save()

                result = (True, new_ciiu_code_list)

            else: 
                result = (False, self.CIIU_CODE_SERIALIZER_ERROR.format(str(serializer.errors)))

        else:
            result = (False, self.LIST_ERROR.format('ciiu_code'))
            
        return result

    def _update_gei_activity_type(self, gei_actitvity_type, data):

        serialized_gei_activity_type = self._get_serialized_gei_activity_type(data, gei_actitvity_type)
        if serialized_gei_activity_type.is_valid():
            gei_activity_type = serialized_gei_activity_type.save()
            result = (True, gei_activity_type)
        else:
            result = (False, serialized_gei_activity_type.errors)

        return result

    def _update_gei_activity_type_list(self, data, gei_organization):

        result = (True, [])
        
        if isinstance(data, list):

            gei_actitvity_type_list = gei_organization.gei_activity_type.all()

            ## [{ id: json object }, {} , ...] data for updating gei activity record
            gei_activity_type_data_list =  { gei_act.get('id'): gei_act for gei_act in  data if gei_act.get('id', False) }
            gei_activity_type_list_for_updating = gei_actitvity_type_list.filter(id__in = list(gei_activity_type_data_list.keys()))

            gei_activity_type_list_updated = {}
            for gei_activity_type in gei_activity_type_list_for_updating:

                record_status, record_data = self._update_gei_activity_type(gei_activity_type, gei_activity_type_data_list.get(gei_activity_type.id, {}))
                dict_data = record_data if isinstance(record_data, list) else [record_data]

                gei_activity_type_list_updated.setdefault(record_status,[]).extend(dict_data) 

            ## updating data - exclude  updated records
            data = [gei_act for gei_act in data if not gei_act.get('id', False)]
            serialized_gei_activity_type = self._get_serialized_gei_activity_type_list(data, gei_organization.id)

            if  serialized_gei_activity_type.is_valid() and all(gei_activity_type_list_updated):
                new_gei_activity_type = serialized_gei_activity_type.save()
                gei_activity_type_list_for_deleting = gei_actitvity_type_list.exclude(
                    id__in = list(gei_activity_type_data_list.keys())
                ).exclude(
                    id__in=[gei_act.id for gei_act in new_gei_activity_type]
                )
                gei_activity_type_list_for_deleting.delete()

                result = (True, gei_actitvity_type_list)

            else:
                result = (False, self.SERIALIZER_ERROR.format("gei activity type",
                    str(serialized_gei_activity_type.errors) if all(gei_activity_type_list_updated) else gei_activity_type_list_updated.get(False, [])))
                    
        else:
            result = (False, self.LIST_ERROR.format('gei activity types'))

        return result


    def _update_reduction(self, reduction, data):

        serialized_reduction = self._get_serialized_reduction(data, reduction)
        if serialized_reduction.is_valid():
            reduction = serialized_reduction.save()
            result = (True, reduction)
        else:
            result = (False, serialized_reduction.errors)

        return result

    
    def _update_reduction_list(self, data, organization_classification):

        result = (True, [])
        
        if isinstance(data, list):

            reduction_list = organization_classification.reduction.all()

            ## [{ id: json object }, {} , ...] data for updating reduction record
            reduction_data_list =  { rd.get('id'): rd for rd in  data if rd.get('id', False) }
            reduction_list_for_updating = reduction_list.filter(id__in = list(reduction_data_list.keys()))

            reduction_list_updated = {}
            for reduction in reduction_list_for_updating:

                record_status, record_data = self._update_reduction(reduction, reduction_data_list.get(reduction.id, {}))
                dict_data = record_data if isinstance(record_data, list) else [record_data]

                reduction_list_updated.setdefault(record_status,[]).extend(dict_data) 

            ## updating data - exclude  updated records
            data = [rd for rd in data if not rd.get('id', False)]
            serialized_reduction = self._get_serialized_reduction_list(data, organization_classification.id)

            if  serialized_reduction.is_valid() and all(reduction_list_updated):
                new_reduction = serialized_reduction.save()
                reduction_list_for_deleting = reduction_list.exclude(
                    id__in = list(reduction_data_list.keys())
                ).exclude(
                    id__in=[rd.id for rd in new_reduction]
                )
                reduction_list_for_deleting.delete()

                result = (True, reduction_list)

            else:
                result = (False, self.SERIALIZER_ERROR.format("reduction",
                    str(serialized_reduction.errors) if all(reduction_list_updated) else reduction_list_updated.get(False, [])))
                    
        else:
            result = (False, self.LIST_ERROR.format('reduction'))

        return result

    def _update_carbon_offset(self, carbon_offset, data):

        serialized_carbon_offset = self._get_serialized_carbon_offset(data, carbon_offset)
        if serialized_carbon_offset.is_valid():
            carbon_offset = serialized_carbon_offset.save()
            result = (True, carbon_offset)
        else:
            result = (False, serialized_carbon_offset.errors)

        return result
    
    def _update_carbon_offset_list(self, data, organization_classification):

        result = (True, [])
        
        if isinstance(data, list):

            carbon_offset_list = organization_classification.carbon_offset.all()

            ## [{ id: json object }, {} , ...] data for updating carbon_offset record
            carbon_offset_data_list =  { c_offset.get('id'): c_offset for c_offset in  data if c_offset.get('id', False) }
            carbon_offset_list_for_updating = carbon_offset_list.filter(id__in = list(carbon_offset_data_list.keys()))

            carbon_offset_list_updated = {}
            for carbon_offset in carbon_offset_list_for_updating:

                record_status, record_data = self._update_carbon_offset(carbon_offset, carbon_offset_data_list.get(carbon_offset.id, {}))
                dict_data = record_data if isinstance(record_data, list) else [record_data]

                carbon_offset_list_updated.setdefault(record_status,[]).extend(dict_data) 

            ## updating data - exclude  updated records
            data = [c_offset for c_offset in data if not c_offset.get('id', False)]
            serialized_carbon_offset = self._get_serialized_carbon_offset_list(data, organization_classification.id)

            if  serialized_carbon_offset.is_valid() and all(carbon_offset_list_updated):
                new_carbon_offset = serialized_carbon_offset.save()
                carbon_offset_list_for_deleting = carbon_offset_list.exclude(
                    id__in = list(carbon_offset_data_list.keys())
                ).exclude(
                    id__in=[c_offset.id for c_offset in new_carbon_offset]
                )
                carbon_offset_list_for_deleting.delete()

                result = (True, carbon_offset_list)

            else:
                result = (False, self.SERIALIZER_ERROR.format(
                    str(serialized_carbon_offset.errors) if all(carbon_offset_list_updated) else carbon_offset_list_updated.get(False, [])))
                    
        else:
            result = (False, self.LIST_ERROR.format('carbon_offset'))

        return result


    def _update_organization(self, organization, data):

        validation_dict = {}
        # fk's of object organization that have nested fields
        field_list = ['contact'] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_or_update_record(organization, field,  data.get(field))
                
                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)
        
        if all(validation_dict):
            serialized_organization = self._get_serialized_organization(data, organization)

            if serialized_organization.is_valid():
                organization = serialized_organization.save()

                ciiu_code_data = data.get("ciiu_code_list", False)
                serialized_ciiu_code_status, serialized_ciiu_code_data = self._update_ciiu_code(ciiu_code_data, organization)

                if serialized_ciiu_code_status:
                    result = (True, organization)

                else:
                    result = (serialized_ciiu_code_status, serialized_ciiu_code_data)
            else:
                errors = serialized_organization.errors
                result = (False, errors)
  
        else:
            result = (False, self.EMPTY_ORGANIZATION_ERROR)

        return result


    def _update_organization_classification(self, organization_classification, data):

        validation_dict = {}
        # fk's of object organization_classification that have nested fields
        field_list = [] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_or_update_record(organization_classification, field, data.get(field))

                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)

        if all(validation_dict):
            serialized_organization_classification = self._get_serialized_organization_classification(data, organization_classification)
            if serialized_organization_classification.is_valid():
                organization_classification = serialized_organization_classification.save()

                field_related_list = ['reduction', 'carbon_offset']
                validation_dict.clear()

                for field_related in field_related_list:
                    if data.get(field_related, False):
                        record_status, record_data = self._create_or_update_record_list(data.get(field_related), field_related, organization_classification)

                        dict_data = record_data if isinstance(record_data, list) else [record_data]
                        validation_dict.setdefault(record_status,[]).extend(dict_data)

                if all(validation_dict):
                    result = (True, organization_classification)
                else:
                    result = (False, validation_dict.get(False))

            else:
                result = (False, serialized_organization_classification.errors)
        else:
            result = (False, validation_dict.get(False))

        return result

    def _update_gas_scope(self, data, gas_report):

        gas_scope_list = []
        result = (True, gas_scope_list)
        try:
            with transaction.atomic():
                for gas_scope in data:
                    gas_scope['gas_report'] = gas_report.id
                    quantified_gases_list = gas_scope.get('quantified_gases')

                    if isinstance(quantified_gases_list, list):
                        serialized_gas_scope = self._get_serialized_gas_scope(gas_scope)

                        if serialized_gas_scope.is_valid():
                            gas_scope = serialized_gas_scope.save()
                            serialized_quantified_gases = self._get_serialized_quantified_gases_list(quantified_gases_list, gas_scope.id)

                            if serialized_quantified_gases.is_valid():
                                quantified_gases = serialized_quantified_gases.save()
                                
                            else:
                                raise Exception(str(serialized_quantified_gases.errors))
                        else:
                            
                            raise Exception(str(serialized_gas_scope.errors))
                    else:

                        raise Exception(self.MISSING_FIELD.format('gas_scopes'))

                    gas_scope_list.append(gas_scope.id)
                
                gas_scopes_for_deleting = gas_report.gas_scope.all().exclude(id__in=gas_scope_list)
                gas_scopes_for_deleting.delete()


        except Exception as exc:
            result = (False, exc)

        return  result

    def _update_gas_report(self, gas_report, data):

        validation_dict = {}
        # fk's of object organization_classification that have nested fields
        field_list = ['biogenic_emission'] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_or_update_record(gas_report, field, data.get(field))

                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)
        
        if all(validation_dict):
            serialized_gas_report = self._get_serialized_gas_report(data)
            if serialized_gas_report.is_valid():
                gas_report = serialized_gas_report.save()
                if data.get('gas_scopes', False):
                    gas_scope_status, gas_scope_data = self._update_gas_scope(data.get('gas_scopes'), gas_report)
                    if gas_scope_status:
                        result = (True, gas_report)
                    else:
                        result = (True, gas_scope_data)
                else:
                    result = (True, gas_report)             
            else:
                result = (False, serialized_gas_report.errors)
        else:
            result = (False, validation_dict.get(False))

        return result




    def _update_gei_organization(self, gei_organization, data):

        validation_dict = {}

        # fk's of object organization_classification that have nested fields
        field_list = ['gas_report', 'organization_category'] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_or_update_record(gei_organization, field, data.get(field))

                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)

        if all(validation_dict):

            serialized_gei_organization = self._get_serialized_gei_organization(data, gei_organization) 
            if serialized_gei_organization.is_valid():
                gei_organization = serialized_gei_organization.save()

                field_related_list = ['gei_activity_type']
                validation_dict.clear()

                for field_related in field_related_list:
                    if data.get(field_related, False):
                        record_status, record_data = self._create_or_update_record_list(data.get(field_related), field_related, gei_organization,)

                        dict_data = record_data if isinstance(record_data, list) else [record_data]
                        validation_dict.setdefault(record_status,[]).extend(dict_data)

                if all(validation_dict):
                    result = (True, gei_organization)
                else:
                    result = (False, validation_dict.get(False))

            else:
                result = (False, serialized_gei_organization.errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result


    ## Aux Get Objects
    # 

    def _get_one(self, ppcn_id):
        
        try:
            ppcn = PPCN.objects.get(id=ppcn_id)

            result = (True, ppcn) 
            
        except PPCN.DoesNotExist as exc:

            result = (False, self.PPCN_DOES_NOT_EXIST)

        return result 



    def delete_organization(self, pk):
        try:
            org = Organization.objects.get(id=pk)
            org.delete()
            result = (True, {"Result":"Organization has been delete"})
        except:
            result = (False, {"Result":"Organization has been delete"})
        return result

    def get_all(self, request, language, user = False):

        context = {'language': language}
        try:
            ppcn_registries = PPCN.objects.all() if not user else PPCN.objects.filter(user=request.user).all()
            ppcn_data_list = []
            for ppcn in ppcn_registries:
                ppcn_data = PPCNSerializer(ppcn).data
                ppcn_data['gas_removal'] = []
                if ppcn.organization:
                    ppcn_data['organization'] = OrganizationSerializer(ppcn.organization).data
                    ppcn_data.get('organization')['ciiu_code'] = CIIUCodeSerializer(ppcn.organization.ciiu_code.all(), many=True).data
                    if ppcn.organization.contact:
                        ppcn_data.get('organization')['contact'] = ContactSerializer(ppcn.organization.contact).data
                
                if ppcn.organization_classification:
                    ppcn_data['organization_classification'] = OrganizationClassificationSerializer(ppcn.organization_classification).data
                    ppcn_data.get('organization_classification')['reduction'] = []
                    ppcn_data.get('organization_classification')['carbon_offset'] = []

                    if ppcn.organization_classification.required_level:
                        ppcn_data.get('organization_classification')['required_level'] = RequiredLevelSerializer(ppcn.organization_classification.required_level, context=context).data
                    if ppcn.organization_classification.recognition_type:
                        ppcn_data.get('organization_classification')['recognition_type'] = RecognitionTypeSerializer(ppcn.organization_classification.recognition_type, context=context).data
                    
                    for reduction in ppcn.organization_classification.reduction.all():
                        ppcn_data.get('organization_classification').get('reduction').append(ReductionSerializer(reduction).data)

                    for carbon_offset in ppcn.organization_classification.carbon_offset.all():
                        ppcn_data.get('organization_classification').get('carbon_offset').append(CarbonOffsetSerializer(carbon_offset).data)
                
                ppcn_data['ppcn_files'] = self._get_ppcn_files_list(ppcn.files.all())
                ppcn_data['file']= self._get_files_list([f.files.all() for f in ppcn.workflow_step.all()])
                ppcn_data['geographic_level'] = GeographicLevelSerializer(ppcn.geographic_level, context=context).data
                ppcn_data['comments'] = CommentSerializer(ppcn.comments.all(), many=True).data

                if ppcn.gei_organization:
                    ppcn_data['gei_organization'] = GeiOrganizationSerializer(ppcn.gei_organization).data
                    ppcn_data.get('gei_organization')['gei_activity_type'] = []
                    if ppcn.gei_organization.ovv:
                        ppcn_data.get('gei_organization')['ovv'] = OVVSerializer(ppcn.gei_organization.ovv).data
                        
                    if ppcn.gei_organization.gas_report:
                        ppcn_data.get('gei_organization')['gas_report'] = GasReportSerializer(ppcn.gei_organization.gas_report).data
                        if ppcn.gei_organization.gas_report.biogenic_emission:
                            ppcn_data.get('gei_organization').get('gas_report')['biogenic_emission'] = BiogenicEmissionSerializer(ppcn.gei_organization.gas_report.biogenic_emission).data
                        
                        if ppcn.gei_organization.gas_report.gas_scope:
                            ppcn_data.get('gei_organization').get('gas_report')['gas_scopes'] = []
                            for gas_scope in ppcn.gei_organization.gas_report.gas_scope.all():
                                gas_scope_data = GasScopeSerializer(gas_scope).data
                                gas_scope_data['quantified_gases'] = QuantifiedGasSerializer(gas_scope.quantified_gases.all(), many=True).data
                                ppcn_data.get('gei_organization').get('gas_report').get('gas_scopes').append(gas_scope_data)
                    
                    if ppcn.gei_organization.organization_category:
                        ppcn_data.get('gei_organization')['organization_category'] = OrganizationCategorySerializer(ppcn.gei_organization.organization_category).data
                    
                    for gei_activity_type in ppcn.gei_organization.gei_activity_type.all():
                        gei_activity_type_data = GeiActivityTypeSerializer(gei_activity_type).data
                        gei_activity_type_data['sector'] = SectorSerializer(gei_activity_type.sector, context=context).data
                        gei_activity_type_data['sub_sector'] = SubSectorSerializer(gei_activity_type.sub_sector, context=context).data
                        ppcn_data.get('gei_organization').get('gei_activity_type').append(gei_activity_type_data)

                for gas_removal in ppcn.gas_removal.all():
                        ppcn_data.get('gas_removal').append(GasRemovalSerializer(gas_removal).data)

                ppcn_data_list.append(ppcn_data)
            result = (True, ppcn_data_list)

        except PPCN.DoesNotExist:
            result = (False, self.PPCN_ERROR_GET_ALL)
        return result


    def create_change_log_entry(self, ppcn, previous_status, current_status, user):
        serialized_change_log = self.get_serialized_change_log(ppcn.id, previous_status, current_status, user.id)
        if serialized_change_log.is_valid():
            serialized_change_log.save()
            result = (True, serialized_change_log.data)
        else:
            result = (False, serialized_change_log.errors)
        return result

   

 
    def create(self, request):
        errors =[]
        validation_dict = {}
        data = request.data
        # fk's of object ppcn that have nested fields
        field_list = ['organization', 'gei_organization', 'organization_classification'] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field)

                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)
        
        if all(validation_dict):
            serialized_ppcn = self._get_serialized_ppcn(data)
            if serialized_ppcn.is_valid():
                ppcn = serialized_ppcn.save()
                field_related_list = ['gas_removal']
                validation_dict.clear()
                for field_related in field_related_list:
                    if data.get(field_related, False):
                        record_status, record_data = self._create_related_record_list(data.get(field_related), field_related, ppcn)

                        dict_data = record_data if isinstance(record_data, list) else [record_data]
                        validation_dict.setdefault(record_status,[]).extend(dict_data)

                if all(validation_dict):
                    result = (True, PPCNSerializer(ppcn).data)
                else:
                    result = (False, validation_dict.get(False))
            else:
                errors.append(serialized_ppcn.errors)
                result = (False, errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result


    def send_to_review(self, request, ppcn_id):
        ## TO DO: call _check_all_field_complete

        f = lambda x: x.method.__name__ == 'submit'

        try:
            ppcn = PPCN.objects.get(id=ppcn_id)
            user = request.user 
            ppcn_previous_status = ppcn.fsm_state
            transition_list = ppcn.get_available_fsm_state_transitions()
            transition_list = list(filter(f, transition_list))

            if len(transition_list) == 1:
                transition = transition_list[0]
                submit_function = getattr(ppcn, transition.method.__name__)
                submit_function()
                ppcn.save()
                change_log_status, change_log_data = self.create_change_log_entry(ppcn, ppcn_previous_status, ppcn.fsm_state, user)
                if change_log_status:
                    result = (True, 'PPCN request has been submitted')

                else:
                    result = (False, change_log_data)
            
            else:
                result = (False, self.SEND_TO_REVIEW_ERROR)
                
        except PPCN.DoesNotExist:
            result = (False, self.PPCN_DOES_NOT_EXIST)

        except Exception as exp:
            result = (False, exp)

        return result



    def get(self, id ,language = 'en'):
        context = {'language': language}
        try:
            ppcn = PPCN.objects.get(id=id)
            ppcn_data = PPCNSerializer(ppcn).data
            ppcn_data['gas_removal'] = []
            if ppcn.organization:
                    ppcn_data['organization'] = OrganizationSerializer(ppcn.organization).data
                    ppcn_data.get('organization')['ciiu_code'] = CIIUCodeSerializer(ppcn.organization.ciiu_code.all(), many=True).data
                    if ppcn.organization.contact:
                        ppcn_data.get('organization')['contact'] = ContactSerializer(ppcn.organization.contact).data
            if ppcn.organization_classification:
                ppcn_data['organization_classification'] = OrganizationClassificationSerializer(ppcn.organization_classification).data
                ppcn_data.get('organization_classification')['reduction'] = []
                ppcn_data.get('organization_classification')['carbon_offset'] = []

                if ppcn.organization_classification.required_level:
                    ppcn_data.get('organization_classification')['required_level'] = RequiredLevelSerializer(ppcn.organization_classification.required_level, context=context).data
                if ppcn.organization_classification.recognition_type:
                    ppcn_data.get('organization_classification')['recognition_type'] = RecognitionTypeSerializer(ppcn.organization_classification.recognition_type, context=context).data
                
                for reduction in ppcn.organization_classification.reduction.all():
                    ppcn_data.get('organization_classification').get('reduction').append(ReductionSerializer(reduction).data)

                for carbon_offset in ppcn.organization_classification.carbon_offset.all():
                    ppcn_data.get('organization_classification').get('carbon_offset').append(CarbonOffsetSerializer(carbon_offset).data)
                    
            ppcn_data['ppcn_files'] = self._get_ppcn_files_list(ppcn.files.all())
            ppcn_data['file'] = self._get_files_list([f.files.all() for f in ppcn.workflow_step.all()])
            ppcn_data['geographic_level'] = GeographicLevelSerializer(ppcn.geographic_level, context=context).data
            ppcn_data['comments'] = CommentSerializer(ppcn.comments.all(), many=True).data

            if ppcn.gei_organization:
                ppcn_data['gei_organization'] = GeiOrganizationSerializer(ppcn.gei_organization).data
                
                ppcn_data.get('gei_organization')['gei_activity_type'] = []
                if ppcn.gei_organization.ovv:
                    ppcn_data.get('gei_organization')['ovv'] = OVVSerializer(ppcn.gei_organization.ovv).data
                
                if ppcn.gei_organization.organization_category:
                    ppcn_data.get('gei_organization')['organization_category'] = OrganizationCategorySerializer(ppcn.gei_organization.organization_category).data
                    
                if  ppcn.gei_organization.gas_report:
                    ppcn_data.get('gei_organization')['gas_report'] = GasReportSerializer(ppcn.gei_organization.gas_report).data
                    if ppcn.gei_organization.gas_report.biogenic_emission:
                        ppcn_data.get('gei_organization').get('gas_report')['biogenic_emission'] = BiogenicEmissionSerializer(ppcn.gei_organization.gas_report.biogenic_emission).data
                    
                    if ppcn.gei_organization.gas_report.gas_scope:
                        ppcn_data.get('gei_organization').get('gas_report')['gas_scopes'] = []
                        for gas_scope in ppcn.gei_organization.gas_report.gas_scope.all():
                            gas_scope_data = GasScopeSerializer(gas_scope).data
                            gas_scope_data['quantified_gases'] = QuantifiedGasSerializer(gas_scope.quantified_gases.all(), many=True).data
                            ppcn_data.get('gei_organization').get('gas_report').get('gas_scopes').append(gas_scope_data)

                for gei_activity_type in ppcn.gei_organization.gei_activity_type.all():
                    gei_activity_type_data = GeiActivityTypeSerializer(gei_activity_type).data
                    gei_activity_type_data['sector'] = SectorSerializer(gei_activity_type.sector, context=context).data
                    gei_activity_type_data['sub_sector'] = SubSectorSerializer(gei_activity_type.sub_sector, context=context).data
                    ppcn_data.get('gei_organization').get('gei_activity_type').append(gei_activity_type_data)


            for gas_removal in ppcn.gas_removal.all():
                        ppcn_data.get('gas_removal').append(GasRemovalSerializer(gas_removal).data) 

            result = (True, ppcn_data)
        except PPCN.DoesNotExist:
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

        validation_dict = {}
        data = request.data
        
        field_list = ['organization', 'gei_organization', 'organization_classification'] 

        try:

            ppcn = PPCN.objects.get(id=id)
             # fk's of object ppcn that have nested fields
            for field in field_list:
                if data.get(field, False):
                    record_status, record_data = self._create_or_update_record(ppcn, field, data.get(field))
                    
                    if record_status:
                        data[field] = record_data.id
                    dict_data = record_data if isinstance(record_data, list) else [record_data]
                    validation_dict.setdefault(record_status,[]).extend(dict_data)

            if all(validation_dict):
                serialized_ppcn = self._get_serialized_ppcn(data, ppcn)
                if serialized_ppcn.is_valid():
                    ppcn = serialized_ppcn.save()
                    field_related_list = ['gas_removal']
                    validation_dict.clear()

                    for field_related in field_related_list:
                        if data.get(field_related, False):
                            record_status, record_data = self._create_or_update_record_list(data.get(field_related), field_related, ppcn)

                            dict_data = record_data if isinstance(record_data, list) else [record_data]
                            validation_dict.setdefault(record_status,[]).extend(dict_data)

                    if all(validation_dict):
                        result = (True, PPCNSerializer(ppcn).data)
                    else:
                        result = (False, validation_dict.get(False))
                else:

                    result = (False, serialized_ppcn.errors)
            else:
                result = (False, validation_dict.get(False))

        except PPCN.DoesNotExist:
            result = (False, self.PPCN_DOES_NOT_EXIST)

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

    def assign_comment(self, comment_list, ppcn, user):

        data = [{**comment, 'fsm_state': ppcn.fsm_state, 'user': user.id, 'review_number': ppcn.review_count}  for comment in comment_list]
        comment_list_status, comment_list_data = workflow_service.create_comment_list(data)

        if comment_list_status:
            ppcn.comments.add(*comment_list_data)
            result = (True, comment_list_data)
        
        else:
            result = (False, comment_list_data)

        return result


    def update_fsm_state(self, next_state, ppcn, user):
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
                ppcn_previous_status = ppcn.fsm_state
                transition_function()
                ppcn.save()
                change_log_status, change_log_data = self.create_change_log_entry(ppcn, ppcn_previous_status, ppcn.fsm_state, user)

                if change_log_status:
                    result = (True, PPCNSerializer(ppcn).data)
                
                else:
                    result = (False, change_log_data)

            else: result = (False, self.INVALID_STATUS_TRANSITION)
            
        
        return result


    def get_current_comments(self, request, ppcn_id):

        ppcn_status, ppcn_data = self._get_one(ppcn_id)

        if ppcn_status:
            review_number = ppcn_data.review_count
            fsm_state = ppcn_data.fsm_state
            commet_list = ppcn_data.comments.filter(review_number=review_number, fsm_state=fsm_state).all()

            serialized_comment = CommentSerializer(commet_list, many=True)

            result = (True, serialized_comment.data)
        
        else:
            result = (False, ppcn_data)

        return result
    
    def get_comments_by_fsm_state_or_review_number(self, request, ppcn_id, fsm_state=False, review_number=False):
        ppcn_status, ppcn_data = self._get_one(ppcn_id)
        search_key = lambda x, y: { x:y } if y else {}
        if ppcn_status:

            search_kwargs = {**search_key('fsm_state', fsm_state), **search_key('review_number', review_number)}
            commet_list = ppcn_data.comments.filter(**search_kwargs).all()

            serialized_comment = CommentSerializer(commet_list, many=True)

            result = (True, serialized_comment.data)
        
        else:
            result = (False, ppcn_data)

        return result





    def patch(self, request, ppcn_id):

        request_data = request.data.copy()
        next_state = request_data.pop('fsm_state', False)
        user = request.user
        ppcn_status, ppcn_data = self._get_one(ppcn_id)

        if ppcn_status and next_state:
  
            update_state_status, update_state_data = self.update_fsm_state(next_state, ppcn_data, user)
            if update_state_status:
                comment_list = request_data.get('comments')
                increase_review_counter_status, increase_review_counter_data = self._increase_review_counter(ppcn_data)
                if increase_review_counter_status:
                    assign_status, assign_data = self.assign_comment(comment_list, ppcn_data, user)
                    result = (assign_status, assign_data if not assign_status else PPCNSerializer(ppcn_data).data)
                
                else: 
                    result = (False, increase_review_counter_data)
                
            else:
                result = (False, update_state_data)

        else:
            result = (False, ppcn_data if next_state else self.MISSING_FIELD.format('fsm_state'))
        

        return result

