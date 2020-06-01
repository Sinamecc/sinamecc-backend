from ppcn.models import Organization, GeographicLevel, RequiredLevel, RecognitionType, Sector,GeiOrganization, GeiActivityType, SubSector, PPCN, PPCNFile
from mccr.models import OVV
from mccr.serializers import OVVSerializer
from django.contrib.auth.models import *
from mitigation_action.services import MitigationActionService
from mitigation_action.serializers import ContactSerializer
from ppcn.serializers import *
from ppcn.workflow_steps.models import PPCNWorkflowStepFile
from django_fsm import can_proceed, has_transition_perm
from io import BytesIO
from general.storages import S3Storage
from django.http import FileResponse
from django.urls import reverse
from general.services import EmailServices
from general.helpers.services import ServiceHelper
from workflow.models import ReviewStatus
from workflow.serializers import CommentSerializer
from django.contrib.auth import get_user_model
from workflow.services import WorkflowService
import datetime, uuid, json, os, pdb


email_sender  = "sinamec@grupoincocr.com" ##change to sinamecc email
ses_service = EmailServices(email_sender)
User = get_user_model()
workflow_service = WorkflowService()

class PpcnService():

    def __init__(self):
        self.storage = S3Storage()
        self._service_helper = ServiceHelper()
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
        self.ASSING_GEI_ACTIVITY_TYPES = "Error assigning gei activity types."
        self.CREATING_GEI_ORGANIZATION = "Error creating gei organization."
        self.CONTACT_NOT_MATCH_ERROR = "The contact of the organization doesn't match the one registered."
        self.GEI_ORGANIZATION_DOES_NOT_EXIST = "Gei Organization doesn't exist"
        self.CIIU_CODE_SERIALIZER_ERROR = "Cannot serialize ciiu code because {0}"
        self.LIST_ERROR = "Was expected a {0} list into data"
        self.MISSING_FIELD = "Missing {} field into request"
        self.ATTRIBUTE_INSTANCE_ERROR = 'PPCNService does not have {0} function'
        self.SEND_TO_REVIEW_ERROR = 'Error at the moment to send to review the ppcn form'
    

    # data checker 
    def _check_all_field_complete(self, ppcn_data):

        ## we need to validate which fields should be verified

        pass 
    
    # auxiliar functions
    def _create_sub_record(self, data, name_sub_record):
        
        create_function = f'_create_{name_sub_record}'

        if hasattr(self, create_function):
            function = getattr(self, create_function)
            record_status, record_detail = function(data)
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.ATTRIBUTE_INSTANCE_ERROR.format(create_function))

        return result


    # serialized objects
    def _get_serialized_contact(self, data, contact = False):

        serializer = self._service_helper.get_serialized_record(ContactSerializer, data, record=contact)

        return serializer
        

    def _get_serialized_organization(self, data, organization = False):

        serializer = self._service_helper.get_serialized_record(OrganizationSerializer, data, record=organization)

        return serializer


    def _get_serialized_ppcn(self, data, ppcn=False):

        serializer = self._service_helper.get_serialized_record(PPCNSerializer, data, record=ppcn)

        return serializer


    def _get_serialized_organization_classification(self, data, organization_classification=False):

        serializer = self._service_helper.get_serialized_record(OrganizationClassificationSerializer, data, record=organization_classification)

        return serializer
    

    def _get_serialized_reduction(self, data, reduction=False):

        serializer = self._service_helper.get_serialized_record(ReductionSerializer, data, record=reduction)

        return serializer
    

    def _get_serialized_carbon_offset(self, data, carbon_offset=False):

        serializer = self._service_helper.get_serialized_record(CarbonOffsetSerializer, data, record=carbon_offset)

        return serializer


    def _get_serialized_gei_organization(self, data, gei_organization = False):

        serializer = self._service_helper.get_serialized_record(GeiOrganizationSerializer, data, record=gei_organization)

        return serializer


    def _get_serialized_biogenic_emission(self, data, biogenic_emission=False):

        serializer = self._service_helper.get_serialized_record(BiogenicEmissionSerializer, data, record=biogenic_emission)

        return serializer


    def _get_serialized_gas_report(self, data, gas_report=False):

        serializer = self._service_helper.get_serialized_record(GasReportSerializer, data, record=gas_report)

        return serializer


    def _get_serialized_gas_scope(self, data, gas_scope=False):
        serializer = self._service_helper.get_serialized_record(GasScopeSerializer, data, record=gas_scope)

        return serializer


    def _get_serialized_gas_removal(self, data, gas_removal=False):

        serializer = self._service_helper.get_serialized_record(GasRemovalSerializer, data, record=gas_removal)

        return serializer


    def _get_serialized_organization_category(self, data, organization_category=False):
        serializer = self._service_helper.get_serialized_record(OrganizationCategorySerializer, data, record=organization_category)

        return serializer


    def _get_serialized_quantified_gases_list(self, data, gas_scope_id):

        data = [{**quantified_gas, 'gas_scope': gas_scope_id}  for quantified_gas in data]

        serializer = self._service_helper.get_serialized_record(QuantifiedGasSerializer, data, many=True)

        return serializer


    def _get_serialized_ciuu_code_list(self, data, organization_id):
    
        result = (True, [])

        if isinstance(data, list):
            data = [{**ciiu_code, 'organization': organization_id}  for ciiu_code in data]
 
            serializer = self._service_helper.get_serialized_record(CIIUCodeSerializer, data, many=True)

            if serializer.is_valid():
                serializer.save()

            else: 
                result = (False, self.CIIU_CODE_SERIALIZER_ERROR.format(str(serializer.errors)))

        else:
            result = (False, self.LIST_ERROR.format('ciiu_code'))
            
        return result
    

    def get_serialized_geographic_level(self, request):

        geographic_level_data = {
            'level_es': request.data.get('level'),
            'level_en': request.data.get('level')
        }
        serializer = GeographicLevelSerializer(data=geographic_level_data)
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

    def _create_organization_classification(self, data):

        validation_dict = {}

        if data.get('reduction', False):
            reduction_status, reduction_data = self._create_reduction(data.get('reduction'))
            if reduction_status:
                data['reduction'] = reduction_data.id

            dict_data = reduction_data if isinstance(reduction_data, list) else [reduction_data]
            validation_dict.setdefault(reduction_status,[]).extend(dict_data)
                                    
        if data.get('carbon_offset', False):
            carbon_offset_status, carbon_offset_data = self._create_carbon_offset(data.get('carbon_offset'))
            if carbon_offset_status:
                data['carbon_offset'] = carbon_offset_data.id
            dict_data = carbon_offset_data if isinstance(carbon_offset_data, list) else [carbon_offset_data]
            validation_dict.setdefault(carbon_offset_status,[]).extend(dict_data)

        if all(validation_dict):
            serialized_organization_classification = self._get_serialized_organization_classification(data)
            if serialized_organization_classification.is_valid():
                organization_classification = serialized_organization_classification.save()
                result = (True, organization_classification)
            else:
                result = (False, serialized_organization_classification.errors)
        else:
            result = (False, validation_dict.get(False))

        return result


    def _create_gei_organization(self, data):
        validation_dict = {}

        if data.get('gas_report', False):
            gas_report_status, gas_report_data = self._create_gas_report(data.get('gas_report'))
            if gas_report_status:
                data['gas_report'] = gas_report_data.id
            dict_data = gas_report_data if isinstance(gas_report_data, list) else [gas_report_data]
            validation_dict.setdefault(gas_report_status,[]).extend(dict_data)
        

        if data.get('organization_category', False):
            organization_category_status, organization_category_data = self._create_organization_category(data.get('organization_category'))
            if organization_category_status:
                data['organization_category'] = organization_category_data.id
            dict_data = organization_category_data if isinstance(organization_category_data, list) else [organization_category_data]
            validation_dict.setdefault(organization_category_status,[]).extend(dict_data)
    
        if all(validation_dict):
            serialized_gei_organization = self._get_serialized_gei_organization(data) 
            if serialized_gei_organization.is_valid():
                gei_organization = serialized_gei_organization.save()
                if data.get('gei_activity_types', False):

                    gei_activity_types_status, gei_activity_types_data = self._assign_gei_activity_types(data, gei_organization)

                    if gei_activity_types_status:
                        result = (True, gei_organization)
                    else:
                        result = (False, gei_activity_types_data)
                else:
                    result = (False, self.ASSING_GEI_ACTIVITY_TYPES)
            else:
                result = (False, serialized_gei_organization.errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result

    def _create_biogenic_emsission(self, data):

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
        
        if data.get('biogenic_emission', False):
            biogenic_emission_status, biogenic_emission_data = self._create_biogenic_emsission(data.get('biogenic_emission'))
            if biogenic_emission_status:
                data['biogenic_emission'] = biogenic_emission_data.id

            dict_data = biogenic_emission_data if isinstance(biogenic_emission_data, list) else [biogenic_emission_data]
            validation_dict.setdefault(biogenic_emission_status,[]).extend(dict_data)

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


    def _assign_gei_activity_types(self, data, gei_organization):

        gei_activity_types_list = data.get('gei_activity_types')
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

    def _create_organization(self, data):

        data = data
        contact_data = data.get("contact", False)
        ciiu_code_data = data.get("ciiu_code_list", False)
        validation_list = [data, contact_data, ciiu_code_data]

        if all(validation_list):
            serialized_contact = self._get_serialized_contact(contact_data)

            if serialized_contact.is_valid():
                contact = serialized_contact.save()
                data['contact'] = contact.id
                serialized_organization = self._get_serialized_organization(data)

                if serialized_organization.is_valid():
                    organization = serialized_organization.save()
                    organization_id =  organization.id
                    serialized_ciiu_code_status, serialized_ciiu_code_data = self._get_serialized_ciuu_code_list(ciiu_code_data, organization_id)

                    if serialized_ciiu_code_status:
                        result = (True, organization)
                    else:
                        result = (serialized_ciiu_code_status, serialized_ciiu_code_data)

                else:
                    errors = serialized_organization.errors
                    result = (False, errors)
            else:
                errors = serialized_contact.errors
                result = (False, errors)
        else:
            result = (False, self.EMPTY_ORGANIZATION_ERROR)

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
            contact_serialized = self._get_serialized_contact(request.data.get('organization'), contact)

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
                if ppcn.organization:
                    ppcn_data['organization'] = OrganizationSerializer(ppcn.organization).data
                    ppcn_data.get('organization')['ciiu_code'] = CIIUCodeSerializer(ppcn.organization.ciiu_code.all(), many=True).data
                    if ppcn.organization.contact:
                        ppcn_data.get('organization')['contact'] = ContactSerializer(ppcn.organization.contact).data
                
                if ppcn.organization_classification:
                    ppcn_data['organization_classification'] = OrganizationClassificationSerializer(ppcn.organization_classification).data
                    if ppcn.organization_classification.required_level:
                        ppcn_data.get('organization_classification')['required_level'] = RequiredLevelSerializer(ppcn.organization_classification.required_level, context=context).data
                    if ppcn.organization_classification.recognition_type:
                        ppcn_data.get('organization_classification')['recognition_type'] = RecognitionTypeSerializer(ppcn.organization_classification.recognition_type, context=context).data
                    if ppcn.organization_classification.reduction:
                        ppcn_data.get('organization_classification')['reduction'] = ReductionSerializer(ppcn.organization_classification.reduction).data
                    if ppcn.organization_classification.carbon_offset:
                        ppcn_data.get('organization_classification')['carbon_offset'] = CarbonOffsetSerializer(ppcn.organization_classification.carbon_offset).data
                
                if ppcn.gas_removal:
                    ppcn_data['gas_removal'] = GasRemovalSerializer(ppcn.gas_removal).data

                ppcn_data['next_state'] = self.next_action(ppcn)
                ppcn_data['ppcn_files'] = self._get_ppcn_files_list(ppcn.files.all())
                ppcn_data['file']: self._get_files_list([f.files.all() for f in ppcn.workflow_step.all()])
                ppcn_data['geographic_level'] = GeographicLevelSerializer(ppcn.geographic_level, context=context).data
                ppcn_data['comments'] = CommentSerializer(ppcn.comments.all(), many=True).data

                if ppcn.gei_organization:
                    ppcn_data['gei_organization'] = GeiOrganizationSerializer(ppcn.gei_organization).data
                    ppcn_data.get('gei_organization')['gei_activity_types'] = []
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
                    
                    for gei_activity_type in ppcn.gei_organization.gei_activity_types.all():
                        gei_activity_type_data = GeiActivityTypeSerializer(gei_activity_type).data
                        gei_activity_type_data['sector'] = SectorSerializer(gei_activity_type.sector, context=context).data
                        gei_activity_type_data['sub_sector'] = SubSectorSerializer(gei_activity_type.sub_sector, context=context).data
                        ppcn_data.get('gei_organization').get('gei_activity_types').append(gei_activity_type_data)

                ppcn_data_list.append(ppcn_data)
            result = (True, ppcn_data_list)

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

    ## Change this !!!!
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
        data = request.data

        # fk's of object ppcn that have nested fields
        field_list = ['organization', 'gei_organization', 'organization_classification', 'gas_removal'] 
        
        for field in field_list:
            if data.get(field, False):
                record_status, record_detail = self._create_sub_record(data.get(field), field)
                valid_relations.append(record_status)
                if record_status: data[field] = record_detail.id
                else: errors.append(record_detail)

        if all(valid_relations):
            serialized_ppcn = self._get_serialized_ppcn(data)
            if serialized_ppcn.is_valid():
                ppcn = serialized_ppcn.save()
                result = (True, PPCNSerializer(ppcn).data)
            else:
                errors.append(serialized_ppcn.errors)
                result = (False, errors)
        else:
            result = (False, errors)
            
        return result


    def send_to_review(self, request, ppcn_id):
        ## TO DO: call _check_all_field_complete

        f = lambda x: x.method.__name__ == 'submit'

        try:
            ppcn = PPCN.objects.get(id=ppcn_id)
            transition_list = ppcn.get_available_fsm_state_transitions()
            transition_list = list(filter(f, transition_list))

            if len(transition_list) == 1:
                transition = transition_list[0]
                submit_function = getattr(ppcn, transition.method.__name__)
                submit_function()
                ppcn.save()
                result = (True, 'PPCN request has been submitted')
            
            else:
                result = (False, self.SEND_TO_REVIEW_ERROR)
                
        except PPCN.DoesNotExist:
            result = (False, self.PPCN_DOES_NOT_EXIST)

        except Exception as exp:
            result = (False, exp)

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
        context = {'language': language}
        try:
            ppcn = PPCN.objects.get(id=id)
            ppcn_data = PPCNSerializer(ppcn).data
            if ppcn.organization:
                    ppcn_data['organization'] = OrganizationSerializer(ppcn.organization).data
                    ppcn_data.get('organization')['ciiu_code'] = CIIUCodeSerializer(ppcn.organization.ciiu_code.all(), many=True).data
                    if ppcn.organization.contact:
                        ppcn_data.get('organization')['contact'] = ContactSerializer(ppcn.organization.contact).data
            if ppcn.organization_classification:
                ppcn_data['organization_classification'] = OrganizationClassificationSerializer(ppcn.organization_classification).data
                if ppcn.organization_classification.required_level:
                    ppcn_data.get('organization_classification')['required_level'] = RequiredLevelSerializer(ppcn.organization_classification.required_level, context=context).data
                if ppcn.organization_classification.recognition_type:
                    ppcn_data.get('organization_classification')['recognition_type'] = RecognitionTypeSerializer(ppcn.organization_classification.recognition_type, context=context).data
                if ppcn.organization_classification.reduction:
                    ppcn_data.get('organization_classification')['reduction'] = ReductionSerializer(ppcn.organization_classification.reduction).data
                if ppcn.organization_classification.carbon_offset:
                    ppcn_data.get('organization_classification')['carbon_offset'] = CarbonOffsetSerializer(ppcn.organization_classification.carbon_offset).data
            
            if ppcn.gas_removal:
                    ppcn_data['gas_removal'] = GasRemovalSerializer(ppcn.gas_removal).data
                    
            ppcn_data['next_state'] = self.next_action(ppcn)
            ppcn_data['ppcn_files'] = self._get_ppcn_files_list(ppcn.files.all())
            ppcn_data['file']: self._get_files_list([f.files.all() for f in ppcn.workflow_step.all()])
            ppcn_data['geographic_level'] = GeographicLevelSerializer(ppcn.geographic_level, context=context).data
            ppcn_data['comments'] = CommentSerializer(ppcn.comments.all(), many=True).data

            if ppcn.gei_organization:
                ppcn_data['gei_organization'] = GeiOrganizationSerializer(ppcn.gei_organization).data
                
                ppcn_data.get('gei_organization')['gei_activity_types'] = []
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

                for gei_activity_type in ppcn.gei_organization.gei_activity_types.all():
                    gei_activity_type_data = GeiActivityTypeSerializer(gei_activity_type).data
                    gei_activity_type_data['sector'] = SectorSerializer(gei_activity_type.sector, context=context).data
                    gei_activity_type_data['sub_sector'] = SubSectorSerializer(gei_activity_type.sub_sector, context=context).data
                    ppcn_data.get('gei_organization').get('gei_activity_types').append(gei_activity_type_data)

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
                gei_organization_status, gei_organization_detail = self._create_gei_organization(request)
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
