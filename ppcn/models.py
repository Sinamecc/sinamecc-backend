from __future__ import unicode_literals
from mitigation_action.models import Contact
from mccr.models import OVV
from django.conf import settings
import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from general.storages import PrivateMediaStorage
from workflow.models import Comment, ReviewStatus
from django_fsm import FSMField, transition
from general.permissions import PermissionsHelper

from ppcn.email_services import PPCNEmailServices
from general.services import EmailServices

ses_service = EmailServices()

User = get_user_model()
permission = PermissionsHelper()
CURRENCIES = (('CRC', _('Costa Rican colón')), ('USD', _('United States dollar')))
OFFSET_SCHEME = (('CER', _('CER')), ('VER', _('VER')), ('UCC', _('Unidades de Compesnsacion de Carbono')))


class InventoryMethodology(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("InventoryMethodology")
        verbose_name_plural = _("InventoryMethodologies")
    
    def __unicode__(self):
        return smart_unicode(self.type)


class PlusAction(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("PlusAction")
        verbose_name_plural = _("PlusActions")
    
    def __unicode__(self):
        return smart_unicode(self.type)

class PotentialGlobalWarming(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("PotentialGlobalWarming")
        verbose_name_plural = _("PotentialGlobalWarmings")
    
    def __unicode__(self):
        return smart_unicode(self.type)


class EmissionFactor(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("EmissionFactor")
        verbose_name_plural = _("EmissionFactors")
    
    def __unicode__(self):
        return smart_unicode(self.type)

class GeographicLevel(models.Model):

    level_es = models.CharField(max_length=200, blank=False, null=False)
    level_en = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("GeographicLevel")
        verbose_name_plural = _("GeographicLevels")
    
    def __unicode__(self):
        return smart_unicode(self.level)


class RequiredLevel(models.Model):

    level_type_es = models.CharField(max_length=200, blank=False, null=False)
    level_type_en = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("RequiredLevel")
        verbose_name_plural = _("RequiredLevels")

    def __unicode__(self):
        return smart_unicode(self.level)


class RecognitionType(models.Model):

    recognition_type_es = models.CharField(max_length=200, blank=False, null=False)
    recognition_type_en = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("RecognitionType")
        verbose_name_plural = _("RecognitionTypes")

    def __unicode__(self):
        return smart_unicode(self.recognition_type)

        
class CarbonOffset(models.Model):

    offset_scheme = models.CharField(choices=OFFSET_SCHEME, max_length=10, blank=False, null=False) 
    project_location = models.CharField(max_length=200, blank=False, null=False)
    certificate_identification = models.CharField(max_length=200, blank=False, null=False)
    total_carbon_offset = models.CharField(max_length=100, blank=False, null=False)
    offset_cost = models.DecimalField(max_digits=10, decimal_places=2)
    offset_cost_currency = models.CharField(choices=CURRENCIES, max_length=10, blank=False, null=False)
    period = models.CharField(max_length=100, blank=False, null=False)
    total_offset_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_offset_cost_currency = models.CharField(choices=CURRENCIES, max_length=10, blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Carbon Offset")
        verbose_name_plural = _("Carbon Offsets")
    
    def __unicode__(self):
        return smart_unicode(self.project_location)


class Reduction(models.Model):

    project = models.CharField(max_length=200, blank=False, null=False)
    activity = models.CharField(max_length=200, blank=False, null=False)
    detail_reduction = models.TextField(blank=False, null=False)
    emission = models.CharField(max_length=10, blank=False, null=False)
    total_emission = models.CharField(max_length=10, blank=False, null=False)
    investment = models.DecimalField(max_digits=10, decimal_places=2)
    investment_currency = models.CharField(choices=CURRENCIES, max_length=10, blank=False, null=False)
    total_investment = models.DecimalField(max_digits=10, decimal_places=2)
    total_investment_currency = models.CharField(choices=CURRENCIES, max_length=10, blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Reduction")
        verbose_name_plural = _("Reductions")
    
    def __unicode__(self):
        return smart_unicode(self.project)




class OrganizationCategory(models.Model):

    organization_category = models.CharField(max_length=200, null=True)
    buildings_number = models.IntegerField(blank=False, null=True)
    data_inventory_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    methodologies_complexity = models.CharField(max_length=200, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Organization Category")
        verbose_name_plural = _("Organization Categories")
    
    def __unicode__(self):
        return smart_unicode("Organization Category {}".format(self.id))

class OrganizationClassification(models.Model):
    
    emission_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    buildings_number = models.IntegerField(blank=False, null=False)
    data_inventory_quantity = models.DecimalField(max_digits=10, decimal_places=2)

    required_level = models.ForeignKey(RequiredLevel,null=True, blank=True, related_name='organization_classification')
    recognition_type = models.ForeignKey(RecognitionType,null=True, blank=True, related_name='organization_classification')

    reduction = models.ForeignKey(Reduction, null=True, related_name='organization_classification')
    carbon_offset = models.ForeignKey(CarbonOffset, null=True, related_name='organization_classification')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Organization Classification")
        verbose_name_plural = _("Organization Classification")
    
    def __unicode__(self):
        return smart_unicode("Organization Classification {}".format(self.id))


class Organization(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False)
    legal_identification = models.CharField(max_length=12, blank=False, null=False)
    representative_name = models.CharField(max_length=200, blank=False, null=False)
    representative_legal_identification = models.CharField(max_length=12, blank=False, null=False)
    phone_organization = models.CharField(max_length=200, blank=False, null=True)
    postal_code = models.CharField(max_length=200, blank=True, null=True)
    fax = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=False, null=False)
    contact = models.ForeignKey(Contact, related_name='organization', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __unicode__(self):
        return smart_unicode(self.name)

class CIIUCode(models.Model):

    ciiu_code = models.CharField(max_length=200, blank=False, null=False)
    organization = models.ForeignKey(Organization, blank=False, null=False,  related_name='ciiu_code')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("CIIU Code")
        verbose_name_plural = _("CIIU Codes")

    def __unicode__(self):
        return smart_unicode(self.ciiu_code)

class Sector(models.Model):
    name_es = models.CharField(max_length=200, blank=False, null=False)
    name_en = models.CharField(max_length=200, blank=False, null=False)
    geographicLevel = models.ForeignKey(GeographicLevel, blank = False, null = False)

    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")

    def __unicode__(self):
        return smart_unicode(self.name)


class SubSector(models.Model):

    name_es = models.CharField(max_length=200, blank=False, null=False)
    name_en = models.CharField(max_length=200, blank=False, null=False)
    sector = models.ForeignKey(Sector, related_name='sector')
    class Meta:
        verbose_name = _("SubSector")
        verbose_name_plural = _("SubSectors")

    def __unicode__(self):
        return smart_unicode(self.name)

class BiogenicEmission(models.Model):

    total = models.DecimalField(max_digits=20, decimal_places=5)
    scope_1 = models.CharField(max_length=100, null=True, blank=True)
    scope_2 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Biogenic Emission")
        verbose_name_plural = _("Biogenic Emissions")
    
    def __unicode__(self):
        return smart_unicode('biogenic emission {}'.format(self.total))


class GasReport(models.Model):

    other_gases = models.TextField(null=True, blank=True)
    biogenic_emission = models.ForeignKey(BiogenicEmission, related_name='gas_report')
    cost_ghg_inventory = models.DecimalField(max_digits=20, decimal_places=2)
    cost_ghg_inventory_currency = models.CharField(choices=CURRENCIES, max_length=10, blank=False, null=False)
    cost_ovv_process = models.DecimalField(max_digits=20, decimal_places=2)
    cost_ovv_process_currency = models.CharField(choices=CURRENCIES, max_length=10, blank=False, null=False)

    class Meta:
        verbose_name = _("Gas Report")
        verbose_name_plural = _("Gas Report")
    
    def __unicode__(self):
        return smart_unicode(self.id)

class GasScope(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)
    gas_report = models.ForeignKey(GasReport, related_name='gas_scope', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Gas Scope")
        verbose_name_plural = _("Gas Scopes")
    
    def __unicode__(self):
        return smart_unicode(self.name)

class QuantifiedGas(models.Model):

    name = models.CharField(max_length=50, blank=False, null=False)
    value = models.DecimalField(max_digits=20, decimal_places=5)
    gas_scope = models.ForeignKey(GasScope, related_name='quantified_gases' ,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Quantified Gas")
        verbose_name_plural = _("Quantified Gases")
    
    def __unicode__(self):
        return smart_unicode(self.type)  
    

class GeiActivityType(models.Model):
    
    activity_type = models.CharField(max_length=500, blank=False, null=False)
    sub_sector = models.ForeignKey(SubSector, related_name='gei_sub_sector')
    sector = models.ForeignKey(Sector, related_name='gei_sector')

    class Meta:
        verbose_name = _("Gei Activity Type")
        verbose_name_plural = _("Gei Activity Types")
    
    def __unicode__(self):
        return smart_unicode(self.id)
    

class GeiOrganization(models.Model):

    ovv = models.ForeignKey(OVV, related_name='ovv', blank=False, null=False)
    emission_ovv_date = models.DateField(blank=False, null=False)
    report_year =  models.IntegerField(blank=False, null=False)
    base_year = models.IntegerField(blank=False, null=False)
    gas_report = models.ForeignKey(GasReport, related_name='gei_organization',null=True, blank=True)
    organization_category = models.ForeignKey(OrganizationCategory, related_name='gei_organization', null=True)
    gei_activity_types = models.ManyToManyField(GeiActivityType)

    class Meta:
        verbose_name = _("GeiOrganization")
        verbose_name_plural = _("GeiOrganization")

    def __unicode__(self):
        return smart_unicode(self.activity_type)


class PPCN(models.Model):

    CONFIDENTIAL = (
        ('confidential', _('Confidential')), 
        ('no_confidential', _('No Confidential')), 
        ('partially_confidential', _('Partially Confidential'))
    )

    user = models.ForeignKey(User, related_name='ppcn', null = False)
    organization = models.ForeignKey(Organization, related_name='organization',null=True, blank=True, on_delete=models.CASCADE )
    confidential = models.CharField(max_length=50, choices=CONFIDENTIAL, default='confidential')
    confidential_fields = models.TextField(blank=False, null=True) ## use to partially confidential
    geographic_level = models.ForeignKey(GeographicLevel,null=True, blank=True, related_name='geographic_level')
    organization_classification = models.ForeignKey(OrganizationClassification, blank=False, null=True, related_name='ppcn')
    gei_organization = models.ForeignKey(GeiOrganization, blank=True, null=True, related_name='gei_organization')

    review_count = models.IntegerField(null=True, blank=True, default=0)
    comments = models.ManyToManyField(Comment, blank=True)
    fsm_state = FSMField(default='PPCN_new', protected=True)
   

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('PPCN')
        verbose_name_plural = _('PPCNs')
        permissions = (
            ("can_provide_information", "Can provide information ppcn"),
            ("user_ca_permission","user CA permission PPCN"),
            ("user_dcc_permission","user DCC permision PPCN"),
            ("user_executive_secretary_permission","user executive secretary permission PPCN")
        )
    
    def __unicode__(self):
        return smart_unicode(self.type)
    

    #first implementation.
    def can_submit(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_new
        return self.fsm_state == 'PPCN_new'

    @transition(field='fsm_state', source='PPCN_new', target='PPCN_submitted', conditions=[can_submit], on_error='failed', permission='')
    def submit(self):

        result = "The ppcn is transitioning from PPCN_new to PPCN_submitted"
        print(result)
        email_services = PPCNEmailServices(ses_service)
        
        result_status, result_data = email_services.notify_submission_DCC(self)
        if not result_status: return (result_status, result_data)
        
        result_status, result_data = email_services.notify_submission_user(self)
        if not result_status: return (result_status, result_data)
        
        return (True, result)

    #Transitions DCC

    def can_evaluate_DCC(self):
        # Transition condition logic goes here
        # Verify current state

        return self.fsm_state == 'PPCN_submitted' 

    @transition(field='fsm_state', source='PPCN_submitted', target='PPCN_evaluation_by_DCC', conditions=[can_evaluate_DCC], on_error='failed', permission='')
    def evaluate_DCC(self):
        print('The ppcn is transitioning from PPCN_submitted to PPCN_evaluation_by_DCC')
        # Additional logic goes here.
        pass


    def can_submit_DCC(self):
        # Transition condition logic goes here
        # Verify current state

        return self.fsm_state == 'PPCN_evaluation_by_DCC' 

    @transition(field='fsm_state', source='PPCN_evaluation_by_DCC', target='PPCN_decision_step_DCC', conditions=[can_submit_DCC], on_error='failed', permission='')
    def submit_DCC(self):
        print('The ppcn is transitioning from PPCN_evaluation_by_DCC to PPCN_decision_step_DCC')
        # Additional logic goes here.
        pass

    def can_rejected_request_by_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_evaluation_by_DCC
        return self.fsm_state == 'PPCN_decision_step_DCC'
    
    @transition(field='fsm_state', source='PPCN_decision_step_DCC', target='PPCN_rejected_request_by_DCC', conditions=[can_rejected_request_by_DCC], on_error='failed', permission='')
    def rejected_request_by_DCC(self):
        print("The ppcn is transitioning from PPCN_decision_step_DCC to PPCN_rejected_request_by_DCC")
        # Transition condition logic goes here
        # Verify current state
        # send notification
        pass


    def can_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_rejected_request_by_DCC
        # - PPCN_rejected_request_by_CA
        return self.fsm_state == 'PPCN_rejected_request_by_DCC' or self.fsm_state == 'PPCN_rejected_request_by_CA'
    
    @transition(field='fsm_state', source='PPCN_rejected_request_by_DCC', target='PPCN_end', conditions=[can_end], on_error='failed', permission='')
    def end(self):
        print("The ppcn is transitioning from PPCN_rejected_request_by_DCC to PPCN_end")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass
    
    def can_accepted_request_by_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_evaluation_by_DCC
        # - PPCN_evaluation_by_DCC
        return self.fsm_state == 'PPCN_decision_step_DCC'
    
    @transition(field='fsm_state', source='PPCN_decision_step_DCC', target='PPCN_accepted_request_by_DCC', conditions=[can_accepted_request_by_DCC], on_error='failed', permission='')
    def accept_request_by_DCC(self):
        print("The ppcn is transitioning from PPCN_decision_step_DCC to PPCN_accepted_request_by_DCC")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass
    
    def can_changes_requested_by_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_evaluation_by_DCC
        return self.fsm_state == 'PPCN_decision_step_DCC'
    
    @transition(field='fsm_state', source='PPCN_decision_step_DCC', target='PPCN_changes_requested_by_DCC', conditions=[can_changes_requested_by_DCC], on_error='failed', permission='')
    def changes_requested_by_DCC(self):
        print("The ppcn is transitioning from PPCN_decision_step_DCC to PPCN_changes_requested_by_DCC")
        # Transition condition logic goes here
        # Verify current state
        # send notification
        pass

    def can_update_by_request_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_changes_requested_by_DCC
        # - PPCN_updating_by_request_DCC
        return self.fsm_state == 'PPCN_changes_requested_by_DCC'
    
    @transition(field='fsm_state', source='PPCN_changes_requested_by_DCC', target='PPCN_updating_by_request_DCC', conditions=[can_update_by_request_DCC], on_error='failed', permission='')
    def update_by_request_DCC(self):
        print("The ppcn is transitioning from PPCN_changes_requested_by_DCC to PPCN_updating_by_request_DCC")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass

    
    def can_update_evaluate_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_updating_by_request_DCC
        return self.fsm_state == 'PPCN_updating_by_request_DCC'


    @transition(field='fsm_state', source='PPCN_updating_by_request_DCC', target='PPCN_evaluation_by_DCC', conditions=[can_update_evaluate_DCC], on_error='failed', permission='')
    def update_evaluate_DCC(self):
        print("The ppcn is transitioning from PPCN_updating_by_request_DCC to PPCN_evaluation_by_DCC")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass


    # Transitons CA -> Controlaria Ambiental

    def can_evaluation_by_CA(self):
   
        condition = []
        condition_state = (self.fsm_state == 'PPCN_accepted_request_by_DCC')
        condition.append(condition_state)

        condition_geographic_level = (not self.geographic_level.level_en.upper() == "CANTONAL")
        condition.append(condition_geographic_level)
        
        condition_result = (not condition.count(False))
        return condition_result
    
    @transition(field='fsm_state', source='PPCN_accepted_request_by_DCC', target='PPCN_evaluation_by_CA', conditions=[can_evaluation_by_CA], on_error='failed', permission='')
    def evaluate_by_CA(self):
        print("The ppcn is transitioning from accept_request_DCC to PPCN_evaluation_by_CA")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass
    
    def can_end_cantonal_DCC(self):
   
        condition = []
        condition_state = (self.fsm_state == 'PPCN_accepted_request_by_DCC')
        condition.append(condition_state)
        
        condition_geographic_level = (self.geographic_level.level_en.upper() == "CANTONAL")
        condition.append(condition_geographic_level)
        
        condition_result = (not condition.count(False))
        return condition_result
    
    @transition(field='fsm_state', source='PPCN_accepted_request_by_DCC', target='PPCN_end', conditions=[can_end_cantonal_DCC], on_error='failed', permission='')
    def end_cantonal_DCC(self):
        print("The ppcn is transitioning from accept_request_DCC to PPCN_end")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass

    
    def can_submit_CA(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_evaluation_by_CA
        return self.fsm_state == 'PPCN_evaluation_by_CA'
    
    @transition(field='fsm_state', source='PPCN_evaluation_by_CA', target='PPCN_decision_step_CA', conditions=[can_submit_CA], on_error='failed', permission='')
    def submit_CA(self):
        print("The ppcn is transitioning from PPCN_evaluation_by_CA to PPCN_decision_step_CA")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass    

    def can_rejected_request_by_CA(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_evaluation_by_CA
        return self.fsm_state == 'PPCN_decision_step_CA'
    
    @transition(field='fsm_state', source='PPCN_decision_step_CA', target='PPCN_rejected_request_by_CA', conditions=[can_rejected_request_by_CA], on_error='failed', permission='')
    def rejected_request_by_CA(self):
        print("The ppcn is transitioning from PPCN_decision_step_CA to PPCN_rejected_request_by_CA")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass
    
    @transition(field='fsm_state', source='PPCN_rejected_request_by_CA', target='PPCN_end', conditions=[can_end], on_error='failed', permission='')
    def end_CA(self):
        print("The ppcn is transitioning from PPCN_rejected_request_by_CA to PPCN_end")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass
    
    def can_accepted_request_by_CA(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_accepted_request_by_CA
        return self.fsm_state == 'PPCN_decision_step_CA'
    
    @transition(field='fsm_state', source='PPCN_decision_step_CA', target='PPCN_accepted_request_by_CA', conditions=[can_accepted_request_by_CA], on_error='failed', permission='')
    def accept_request_by_CA(self):
        print("The ppcn is transitioning from PPCN_decision_step_CA to PPCN_accepted_request_by_CA")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass


    def can_send_recognition_certificate(self):
        # Transition condition logic goes here
        # Verify current state
        # - PPCN_send_recognition_certificate
        # - PPCN_accepted_request_by_CA
        return self.fsm_state == 'PPCN_accepted_request_by_CA'
    
    @transition(field='fsm_state', source='PPCN_accepted_request_by_CA', target='PPCN_send_recognition_certificate', conditions=[can_send_recognition_certificate], on_error='failed', permission='')
    def send_recognition_certificate(self):
        print("The ppcn is transitioning from PPCN_accepted_request_by_CA to PPCN_send_recognition_certificate")
        # Transition condition logic goes here
        # Verify current state
        # send notification

        pass

class ChangeLog(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=False)
    # Foreign Keys
    ppcn = models.ForeignKey(PPCN, related_name='change_log')
    previous_status = models.CharField(max_length=100, null=True)
    current_status = models.CharField(max_length=100)
    
    user = models.ForeignKey(User, related_name='change_log_ppcn')

    class Meta:
        verbose_name = _("ChangeLog")
        verbose_name_plural = _("ChangeLogs")
        ordering = ('date',)

    def __unicode__(self):
        return smart_unicode(self.name)

class PPCNFile(models.Model):

    user = models.ForeignKey(User, related_name='ppcn_file')
    file = models.FileField(blank = False, null = False, upload_to='ppcn/files/%Y%m%d/%H%M%S',storage=PrivateMediaStorage())
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    ppcn_form = models.ForeignKey(PPCN, related_name = "files", blank = False, null= False, on_delete=models.CASCADE)

    class meta:
        verbose_name = _('ppcn_file')
        verbose_name_plural = _('ppcn_files')

    def __unicode__(self):
        return smart_unicode(self.name)
