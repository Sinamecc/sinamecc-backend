from __future__ import unicode_literals
from django.conf import settings

import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from workflow.models import Comment, ReviewStatus
from general.storages import PrivateMediaStorage
from django_fsm import FSMField, transition
from general.services import EmailServices
from mitigation_action.email_services import MitigationActionEmailServices
from general.services import EmailServices
from general.permissions import PermissionsHelper
User =  get_user_model()
permission = PermissionsHelper()
##Email services, defaul email -> sinamec@grupoincocr.com
ses_service = EmailServices()
class RegistrationType(models.Model):
    type_key = models.CharField(max_length=20, blank=False, null=False)
    type_es = models.CharField(max_length=100, blank=False, null=False)
    type_en = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("RegistrationType")
        verbose_name_plural = _("RegistrationTypes")

    def __unicode__(self):
        return smart_unicode(self.type)

class Institution(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")

    def __unicode__(self):
        return smart_unicode(self.name)

class Contact(models.Model):
    full_name = models.CharField(max_length=100, blank=False, null=False)
    job_title = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False)
    phone = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __unicode__(self):
        return smart_unicode(self.full_name)

class Status(models.Model):
    status_es = models.CharField(max_length=100, blank=False, null=False)
    status_en = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")

    def __unicode__(self):
        return smart_unicode(self.status)

class ProgressIndicator(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    type = models.CharField(max_length=100, blank=False, null=False)
    unit = models.CharField(max_length=100, blank=False, null=False)
    start_date = models.DateField(null=False)

    class Meta:
        verbose_name = _("ProgressIndicator")
        verbose_name_plural = _("ProgressIndicators")

    def __unicode__(self):
        return smart_unicode(self.type)

class FinanceSourceType(models.Model):
    name_es = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("FinanceSourceType")
        verbose_name_plural = _("FinanceSourceTypes")

    def __unicode__(self):
        return smart_unicode(self.name)

class FinanceStatus(models.Model):
    name_es = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("FinanceStatus")
        verbose_name_plural = _("FinanceStatuses")

    def __unicode__(self):
        return smart_unicode(self.name)

class InitiativeFinance(models.Model):

    status = models.ForeignKey(FinanceStatus, related_name='initiative_finance_status', blank=False, null=False)
    finance_source_type = models.ForeignKey(FinanceSourceType, related_name='initiative_finance_source_type', blank=False, null=False)
    source = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = _("InitiativeFinance")
        verbose_name_plural = _("InitiativeFinances")

    def __unicode__(self):
        return smart_unicode(self.name)

class Finance(models.Model):

    status = models.ForeignKey(FinanceStatus, related_name='finance_status', blank=False, null=False)
    source = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Finance")
        verbose_name_plural = _("Finances")

    def __unicode__(self):
        return smart_unicode(self.name)

class IngeiCompliance(models.Model):
    name_es = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("IngeiCompliance")
        verbose_name_plural = _("IngeiCompliances")

    def __unicode__(self):
        return smart_unicode(self.name)

class GeographicScale(models.Model):
    name_es = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("GeographicScale")
        verbose_name_plural = _("GeographicScales")

    def __unicode__(self):
        return smart_unicode(self.name)

class Location(models.Model):
    geographical_site = models.CharField(max_length=100, blank=False, null=False)
    is_gis_annexed = models.BooleanField(blank=False, null=False)
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __unicode__(self):
        return smart_unicode(self.geographical_site)



class InitiativeType(models.Model):

    initiative_type_es = models.CharField(max_length=100, blank=False, null=False)
    initiative_type_en = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("InitiativeType")
        verbose_name_plural = _("InitiativeTypes")

    def __unicode__(self):
        return smart_unicode(self.initiative_type_en)

class Initiative(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    
    objective = models.CharField(max_length=400, blank=False, null=False)
    description = models.CharField(max_length=400, blank=False, null=False)
    goal = models.CharField(max_length=400, blank=False, null=False)

    initiative_type  = models.ForeignKey(InitiativeType, related_name = "initiative_type")
    entity_responsible = models.CharField(max_length=100, blank=False, null=False)
    contact =  models.ForeignKey(Contact, related_name='contact')
    budget = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    finance = models.ForeignKey(InitiativeFinance, related_name='finance')
    status = models.ForeignKey(Status, related_name = 'status')

    class Meta:
        verbose_name = _("Initiative")
        verbose_name_plural = _("Initiatives")

    def __unicode__(self):
        return smart_unicode(self.initiative_type_en)

class Mitigation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strategy_name = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    purpose = models.CharField(max_length=500, blank=True, null=True)
    start_date = models.DateField(blank = True, null=True)
    end_date = models.DateField(blank = True, null=True)
    gas_inventory = models.CharField(max_length=100, blank=True, null=True)
    emissions_source = models.CharField(max_length=100, blank=True, null=True)
    carbon_sinks = models.CharField(max_length=100, blank=True, null=True)
    impact_plan = models.CharField(max_length=500, blank=True, null=True)
    impact = models.CharField(max_length=500, blank=True, null=True)
    calculation_methodology = models.CharField(max_length=500, blank=True, null=True)
    is_international = models.NullBooleanField(blank=True, null=True)
    international_participation = models.CharField(max_length=100, blank=True, null=True)
    # Foreign Keys
    user = models.ForeignKey(User, related_name='mitigation_action')
    registration_type = models.ForeignKey(RegistrationType, related_name='mitigation_action', blank=True, null=True)
    initiative = models.ForeignKey(Initiative, related_name='mitigation_action', blank=True, null=True)
    institution = models.ForeignKey(Institution, related_name='mitigation_action', blank=True, null=True)
    contact = models.ForeignKey(Contact, related_name='mitigation_action', blank=True, null=True)
    status = models.ForeignKey(Status, related_name='mitigation_action', blank=True, null=True)
    progress_indicator = models.ForeignKey(ProgressIndicator, related_name='mitigation_action', blank=True, null=True)
    finance = models.ForeignKey(Finance, related_name='mitigation_action', blank=True, null=True)
    ingei_compliances = models.ManyToManyField(IngeiCompliance)
    geographic_scale = models.ForeignKey(GeographicScale, related_name='mitigation_action', blank=True, null=True)
    location = models.ForeignKey(Location, related_name='mitigation_action', blank=True, null=True)

    # Workflow
    review_count = models.IntegerField(null=True, blank=True, default=0)
    comments = models.ManyToManyField(Comment, blank=True)
    fsm_state = FSMField(default='new', protected=True, max_length=100)

    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("MitigationAccess")
        verbose_name_plural = _("MitigationAccesses")
        ordering = ('created',)
        permissions = (
            ("can_provide_information", "Can Provide Information MA"),
            ("user_dcc_permission", "User DCC Permission MA"),
            ("user_executive_secretary_permission", "User Executive Secretary Permission MA"),
        )

    # FSM Annotated Methods (Transitions) and Ordinary Conditions
    # --- Transition ---
    # new -> submitted
    def can_submit(self):
        # Transition condition logic goes here
        # Verify current state
        # - new
        return self.fsm_state == 'new'

    @transition(field='fsm_state', source='new', target='submitted', conditions=[can_submit], on_error='failed', permission='')
    def submit(self):
        result = 'The mitigation action is transitioning from new to submitted'
        # Notify to DCC placeholder
        print(result)
        email_services = MitigationActionEmailServices(ses_service)
        
        result_status, result_data = email_services.notify_submission_DCC(self)
        if not result_status: return (result_status, result_data)
        
        result_status, result_data = email_services.notify_submission_user(self)
        if not result_status: return (result_status, result_data)
        
        return (True, result)


    # --- Transition ---
    # submitted -> in_evaluation_by_DCC
    def can_evaluate_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted
        return self.fsm_state == 'submitted'
    
    @transition(field='fsm_state', source='submitted', target='in_evaluation_by_DCC', conditions=[can_evaluate_DCC], on_error='failed', permission='')
    def evaluate_DCC(self):
        print('The mitigation action is transitioning from submitted to in_evaluation_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # updating_by_request -> in_evaluation_by_DCC
    def can_update_evaluate_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - updating_by_request
        return self.fsm_state == 'updating_by_request'

    @transition(field='fsm_state', source='updating_by_request', target='in_evaluation_by_DCC', conditions=[can_update_evaluate_DCC], on_error='failed', permission='')
    def update_evaluate_DCC(self):
        print('The mitigation action is transitioning from updating_by_request to in_evaluation_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_by_DCC -> decision_step_DCC
    def can_submit_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_by_DCC
        return self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='decision_step_DCC', conditions=[can_submit_DCC], on_error='failed', permission='')
    def submit_DCC(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to decision_step_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_DCC -> changes_requested_by_DCC
    def can_request_changes_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_DCC
        # - in_evaluation_by_DCC
        return self.fsm_state == 'decision_step_DCC' or self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='decision_step_DCC', target='changes_requested_by_DCC', conditions=[can_request_changes_DCC], on_error='failed', permission='')
    def request_changes_DCC(self):
        print('The mitigation action is transitioning from decision_step_DCC to changes_requested_by_DCC')
        # Notify to DCC placeholder
        # self.notify_changes_requested_DCC()
        pass

    # --- Transition ---
    # decision_step_DCC -> rejected_by_DCC
    def can_reject_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_DCC
        # - in_evaluation_by_DCC
        return self.fsm_state == 'decision_step_DCC' or self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='decision_step_DCC', target='rejected_by_DCC', conditions=[can_reject_DCC], on_error='failed', permission='')
    def reject_DCC(self):
        print('The mitigation action is transitioning from decision_step_DCC to rejected_by_DCC')
        # Notify to DCC placeholder
        # self.notify_reject_DCC()
        pass

    # --- Transition ---
    # decision_step_DCC -> registering
    def can_register(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_DCC
        # - in_evaluation_by_DCC
        return self.fsm_state == 'decision_step_DCC' or self.fsm_state == 'in_evaluation_by_DCC'
    
    @transition(field='fsm_state', source='decision_step_DCC', target='registering', conditions=[can_register], on_error='failed', permission='')
    def register(self):
        print('The mitigation action is transitioning from decision_step_DCC to registering')
        # Notify to DCC placeholder
        # self.notify_registering_DCC()
        pass

    # --- Transition ---
    # in_evaluation_by_DCC -> changes_requested_by_DCC
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='changes_requested_by_DCC', conditions=[can_request_changes_DCC], on_error='failed', permission='')
    def evaluate_request_changes_DCC(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to changes_requested_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # changes_requested_by_DCC -> updating_by_request
    def can_update_by_request(self):
        # Transition condition logic goes here
        # Verify current state
        # - changes_requested_by_DCC
        return self.fsm_state == 'changes_requested_by_DCC'

    @transition(field='fsm_state', source='changes_requested_by_DCC', target='updating_by_request', conditions=[can_update_by_request], on_error='failed', permission='')
    def update_by_request(self):
        result = 'The mitigation action is transitioning from changes_requested_by_DCC to updating_by_request'
        
        print(result)
        email_services = MitigationActionEmailServices(ses_service)
        
        result_status, result_data = email_services.notify_submission_DCC(self)
        if not result_status: return (result_status, result_data)
        
        result_status, result_data = email_services.notify_submission_user(self)
        if not result_status: return (result_status, result_data)
        
        return (True, result)
    # --- Transition ---
    # in_evaluation_by_DCC -> rejected_by_DCC
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='rejected_by_DCC', conditions=[can_reject_DCC], on_error='failed', permission='')
    def evaluate_reject_by_DCC(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to rejected_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # rejected_by_DCC -> end
    def can_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - rejected_by_DCC
        return self.fsm_state == 'rejected_by_DCC'

    @transition(field='fsm_state', source='rejected_by_DCC', target='end', conditions=[can_end], on_error='failed', permission='')
    def end(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to rejected_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_by_DCC -> registering
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='registering', conditions=[can_register], on_error='failed', permission='')
    def evaluate_register(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to registering')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # registering -> in_evaluation_INGEI_by_DCC_IMN
    def can_evaluate_INGEI(self):
        # Transition condition logic goes here
        # Verify current state
        # - registering
        return self.fsm_state == 'registering'

    @transition(field='fsm_state', source='registering', target='in_evaluation_INGEI_by_DCC_IMN', conditions=[can_evaluate_INGEI], on_error='failed', permission='')
    def evaluate_INGEI(self):
        print('The mitigation action is transitioning from registering to in_evaluation_INGEI_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_INGEI_by_DCC_IMN -> submit_INGEI_harmonization_required
    def can_submit_INGEI(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_INGEI_by_DCC_IMN
        return self.fsm_state == 'in_evaluation_INGEI_by_DCC_IMN'

    @transition(field='fsm_state', source='in_evaluation_INGEI_by_DCC_IMN', target='submit_INGEI_harmonization_required', conditions=[can_submit_INGEI], on_error='failed', permission='')
    def submit_INGEI(self):
        print('The mitigation action is transitioning from in_evaluation_INGEI_by_DCC_IMN to submit_INGEI_harmonization_required')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_harmonization_required -> INGEI_harmonization_required
    def can_require_INGEI_harmonization(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_harmonization_required
        return self.fsm_state == 'submit_INGEI_harmonization_required'

    @transition(field='fsm_state', source='submit_INGEI_harmonization_required', target='INGEI_harmonization_required', conditions=[can_require_INGEI_harmonization], on_error='failed', permission='')
    def require_INGEI_harmonization(self):
        print('The mitigation action is transitioning from submit_INGEI_harmonization_required to INGEI_harmonization_required')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_harmonization_required -> submitted_SINAMECC_conceptual_proposal_integration
    def can_submit_INGEI_SINAMECC_conceptual_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_harmonization_required
        return self.fsm_state == 'submit_INGEI_harmonization_required'

    @transition(field='fsm_state', source='submit_INGEI_harmonization_required', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_submit_INGEI_SINAMECC_conceptual_proposal], on_error='failed', permission='')
    def submit_INGEI_SINAMECC_conceptual_proposal(self):
        print('The mitigation action is transitioning from submit_INGEI_harmonization_required to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_INGEI_by_DCC_IMN -> INGEI_harmonization_required
    def can_evaluate_require_INGEI_harmonization(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_INGEI_by_DCC_IMN
        return self.fsm_state == 'in_evaluation_INGEI_by_DCC_IMN'

    @transition(field='fsm_state', source='in_evaluation_INGEI_by_DCC_IMN', target='INGEI_harmonization_required', conditions=[can_evaluate_require_INGEI_harmonization], on_error='failed', permission='')
    def evaluate_require_INGEI_harmonization(self):
        print('The mitigation action is transitioning from in_evaluation_INGEI_by_DCC_IMN to INGEI_harmonization_required')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_harmonization_required -> updating_INGEI_changes_proposal
    def can_update_INGEI_changes_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_harmonization_required
        return self.fsm_state == 'INGEI_harmonization_required'

    @transition(field='fsm_state', source='INGEI_harmonization_required', target='updating_INGEI_changes_proposal', conditions=[can_update_INGEI_changes_proposal], on_error='failed', permission='')
    def update_INGEI_changes_proposal(self):
        print('The mitigation action is transitioning from INGEI_harmonization_required to updating_INGEI_changes_proposal')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_harmonization_required -> submitted_SINAMECC_conceptual_proposal_integration
    def can_submit_SINAMECC_conceptual_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_harmonization_required
        return self.fsm_state == 'INGEI_harmonization_required'

    @transition(field='fsm_state', source='INGEI_harmonization_required', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_submit_SINAMECC_conceptual_proposal], on_error='failed', permission='')
    def submit_SINAMECC_conceptual_proposal(self):
        print('The mitigation action is transitioning from INGEI_harmonization_required to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # updating_INGEI_changes_proposal -> submitted_INGEI_changes_proposal_evaluation
    def can_submit_INGEI_changes_evaluation(self):
        # Transition condition logic goes here
        # Verify current state
        # - updating_INGEI_changes_proposal
        return self.fsm_state == 'updating_INGEI_changes_proposal'

    @transition(field='fsm_state', source='updating_INGEI_changes_proposal', target='submitted_INGEI_changes_proposal_evaluation', conditions=[can_submit_INGEI_changes_evaluation], on_error='failed', permission='')
    def submit_INGEI_changes_evaluation(self):
        print('The mitigation action is transitioning from updating_INGEI_changes_proposal to submitted_INGEI_changes_proposal_evaluation')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submitted_INGEI_changes_proposal_evaluation -> in_evaluation_INGEI_changes_proposal_by_DCC_IMN
    def can_evaluate_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted_INGEI_changes_proposal_evaluation
        return self.fsm_state == 'submitted_INGEI_changes_proposal_evaluation'

    @transition(field='fsm_state', source='submitted_INGEI_changes_proposal_evaluation', target='in_evaluation_INGEI_changes_proposal_by_DCC_IMN', conditions=[can_evaluate_DCC_IMN], on_error='failed', permission='')
    def evaluate_DCC_IMN(self):
        print('The mitigation action is transitioning from submitted_INGEI_changes_proposal_evaluation to in_evaluation_INGEI_changes_proposal_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_INGEI_changes_proposal_by_DCC_IMN -> submit_INGEI_changes_proposal_evaluation_result
    def can_submit_INGEI_changes_proposal_evaluation_result(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_INGEI_changes_proposal_by_DCC_IMN
        return self.fsm_state == 'in_evaluation_INGEI_changes_proposal_by_DCC_IMN'

    @transition(field='fsm_state', source='in_evaluation_INGEI_changes_proposal_by_DCC_IMN', target='submit_INGEI_changes_proposal_evaluation_result', conditions=[can_submit_INGEI_changes_proposal_evaluation_result], on_error='failed', permission='')
    def submit_INGEI_changes_proposal_evaluation_result(self):
        print('The mitigation action is transitioning from in_evaluation_INGEI_changes_proposal_by_DCC_IMN to submit_INGEI_changes_proposal_evaluation_result')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_changes_proposal_evaluation_result -> INGEI_changes_proposal_changes_requested_by_DCC_IMN
    def can_request_changes_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_changes_proposal_evaluation_result
        return self.fsm_state == 'submit_INGEI_changes_proposal_evaluation_result'

    @transition(field='fsm_state', source='submit_INGEI_changes_proposal_evaluation_result', target='INGEI_changes_proposal_changes_requested_by_DCC_IMN', conditions=[can_request_changes_DCC_IMN], on_error='failed', permission='')
    def request_changes_DCC_IMN(self):
        print('The mitigation action is transitioning from submit_INGEI_changes_proposal_evaluation_result to INGEI_changes_proposal_changes_requested_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_changes_proposal_evaluation_result -> INGEI_changes_proposal_rejected_by_DCC_IMN
    def can_reject_changes_proposal_by_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_changes_proposal_evaluation_result
        return self.fsm_state == 'submit_INGEI_changes_proposal_evaluation_result'

    @transition(field='fsm_state', source='submit_INGEI_changes_proposal_evaluation_result', target='INGEI_changes_proposal_rejected_by_DCC_IMN', conditions=[can_reject_changes_proposal_by_DCC_IMN], on_error='failed', permission='')
    def reject_changes_proposal_by_DCC_IMN(self):
        print('The mitigation action is transitioning from submit_INGEI_changes_proposal_evaluation_result to INGEI_changes_proposal_rejected_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_changes_proposal_evaluation_result -> INGEI_changes_proposal_accepted_by_DCC_IMN
    def can_accept_changes_proposal_by_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_changes_proposal_evaluation_result
        return self.fsm_state == 'submit_INGEI_changes_proposal_evaluation_result'

    @transition(field='fsm_state', source='submit_INGEI_changes_proposal_evaluation_result', target='INGEI_changes_proposal_accepted_by_DCC_IMN', conditions=[can_accept_changes_proposal_by_DCC_IMN], on_error='failed', permission='')
    def accept_changes_proposal_by_DCC_IMN(self):
        print('The mitigation action is transitioning from submit_INGEI_changes_proposal_evaluation_result to INGEI_changes_proposal_accepted_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_changes_proposal_changes_requested_by_DCC_IMN -> updating_INGEI_changes_proposal_by_request_of_DCC_IMN
    def can_update_changes_proposal_by_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_changes_proposal_changes_requested_by_DCC_IMN
        return self.fsm_state == 'INGEI_changes_proposal_changes_requested_by_DCC_IMN'

    @transition(field='fsm_state', source='INGEI_changes_proposal_changes_requested_by_DCC_IMN', target='updating_INGEI_changes_proposal_by_request_of_DCC_IMN', conditions=[can_update_changes_proposal_by_DCC_IMN], on_error='failed', permission='')
    def update_changes_proposal_by_DCC_IMN(self):
        print('The mitigation action is transitioning from INGEI_changes_proposal_changes_requested_by_DCC_IMN to updating_INGEI_changes_proposal_by_request_of_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_changes_proposal_rejected_by_DCC_IMN -> submitted_SINAMECC_conceptual_proposal_integration
    def can_submit_SINAMECC_conceptual_proposal_integration(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_changes_proposal_rejected_by_DCC_IMN
        return self.fsm_state == 'INGEI_changes_proposal_rejected_by_DCC_IMN'

    @transition(field='fsm_state', source='INGEI_changes_proposal_rejected_by_DCC_IMN', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_submit_SINAMECC_conceptual_proposal_integration], on_error='failed', permission='')
    def submit_SINAMECC_conceptual_proposal_integration(self):
        print('The mitigation action is transitioning from INGEI_changes_proposal_rejected_by_DCC_IMN to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_changes_proposal_accepted_by_DCC_IMN -> implementing_INGEI_changes
    def can_implement_INGEI_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_changes_proposal_accepted_by_DCC_IMN
        return self.fsm_state == 'INGEI_changes_proposal_accepted_by_DCC_IMN'

    @transition(field='fsm_state', source='INGEI_changes_proposal_accepted_by_DCC_IMN', target='implementing_INGEI_changes', conditions=[can_implement_INGEI_changes], on_error='failed', permission='')
    def implement_INGEI_changes(self):
        print('The mitigation action is transitioning from INGEI_changes_proposal_accepted_by_DCC_IMN to implementing_INGEI_changes')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # updating_INGEI_changes_proposal_by_request_of_DCC_IMN -> in_evaluation_INGEI_changes_proposal_by_DCC_IMN
    def can_update_evaluate_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - updating_INGEI_changes_proposal_by_request_of_DCC_IMN
        return self.fsm_state == 'updating_INGEI_changes_proposal_by_request_of_DCC_IMN'

    @transition(field='fsm_state', source='updating_INGEI_changes_proposal_by_request_of_DCC_IMN', target='in_evaluation_INGEI_changes_proposal_by_DCC_IMN', conditions=[can_update_evaluate_DCC_IMN], on_error='failed', permission='')
    def update_evaluate_DCC_IMN(self):
        print('The mitigation action is transitioning from updating_INGEI_changes_proposal_by_request_of_DCC_IMN to in_evaluation_INGEI_changes_proposal_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # implementing_INGEI_changes -> submitted_SINAMECC_conceptual_proposal_integration
    def can_implement_submit_SINAMECC_conceptual_proposal_integration(self):
        # Transition condition logic goes here
        # Verify current state
        # - implementing_INGEI_changes
        return self.fsm_state == 'implementing_INGEI_changes'

    @transition(field='fsm_state', source='implementing_INGEI_changes', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_implement_submit_SINAMECC_conceptual_proposal_integration], on_error='failed', permission='')
    def implement_submit_SINAMECC_conceptual_proposal_integration(self):
        print('The mitigation action is transitioning from implementing_INGEI_changes to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submitted_SINAMECC_conceptual_proposal_integration -> in_evaluation_conceptual_proposal_by_DCC
    def can_evaluate_conceptual_proposal_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted_SINAMECC_conceptual_proposal_integration
        return self.fsm_state == 'submitted_SINAMECC_conceptual_proposal_integration'

    @transition(field='fsm_state', source='submitted_SINAMECC_conceptual_proposal_integration', target='in_evaluation_conceptual_proposal_by_DCC', conditions=[can_evaluate_conceptual_proposal_DCC], on_error='failed', permission='')
    def evaluate_conceptual_proposal_DCC(self):
        print('The mitigation action is transitioning from submitted_SINAMECC_conceptual_proposal_integration to in_evaluation_conceptual_proposal_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # conceptual_proposal_approved -> planning_integration_with_SINAMECC
    def can_plan_integration_SINAMECC(self):
        # Transition condition logic goes here
        # Verify current state
        # - conceptual_proposal_approved
        return self.fsm_state == 'conceptual_proposal_approved'

    @transition(field='fsm_state', source='conceptual_proposal_approved', target='planning_integration_with_SINAMECC', conditions=[can_plan_integration_SINAMECC], on_error='failed', permission='')
    def plan_integration_SINAMECC(self):
        print('The mitigation action is transitioning from conceptual_proposal_approved to planning_integration_with_SINAMECC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # changes_requested_to_conceptual_proposal -> submitted_conceptual_proposal_changes
    def can_submit_conceptual_proposal_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - changes_requested_to_conceptual_proposal
        return self.fsm_state == 'changes_requested_to_conceptual_proposal'

    @transition(field='fsm_state', source='changes_requested_to_conceptual_proposal', target='submitted_conceptual_proposal_changes', conditions=[can_submit_conceptual_proposal_changes], on_error='failed', permission='')
    def submit_conceptual_proposal_changes(self):
        print('The mitigation action is transitioning from changes_requested_to_conceptual_proposal to submitted_conceptual_proposal_changes')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submitted_conceptual_proposal_changes -> submitted_SINAMECC_conceptual_proposal_integration
    def can_submit_SINAMECC_conceptual_proposal_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted_conceptual_proposal_changes
        return self.fsm_state == 'submitted_conceptual_proposal_changes'

    @transition(field='fsm_state', source='submitted_conceptual_proposal_changes', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_submit_SINAMECC_conceptual_proposal_changes], on_error='failed', permission='')
    def submit_SINAMECC_conceptual_proposal_changes(self):
        print('The mitigation action is transitioning from submitted_conceptual_proposal_changes to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # SINAMECC_integration_approved -> implementing_SINAMECC_changes
    def can_implement_SINAMECC_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - SINAMECC_integration_approved
        return self.fsm_state == 'SINAMECC_integration_approved'

    @transition(field='fsm_state', source='SINAMECC_integration_approved', target='implementing_SINAMECC_changes', conditions=[can_implement_SINAMECC_changes], on_error='failed', permission='')
    def implement_SINAMECC_changes(self):
        print('The mitigation action is transitioning from SINAMECC_integration_approved to implementing_SINAMECC_changes')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # SINAMECC_integration_changes_requested -> submitted_SINAMECC_integration_changes
    def can_submit_SINAMECC_integration_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - SINAMECC_integration_changes_requested
        return self.fsm_state == 'SINAMECC_integration_changes_requested'

    @transition(field='fsm_state', source='SINAMECC_integration_changes_requested', target='submitted_SINAMECC_integration_changes', conditions=[can_submit_SINAMECC_integration_changes], on_error='failed', permission='')
    def submit_SINAMECC_integration_changes(self):
        print('The mitigation action is transitioning from SINAMECC_integration_changes_requested to submitted_SINAMECC_integration_changes')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submitted_SINAMECC_integration_changes -> planning_integration_with_SINAMECC
    def can_submit_plan_integration_SINAMECC(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted_SINAMECC_integration_changes
        return self.fsm_state == 'submitted_SINAMECC_integration_changes'

    @transition(field='fsm_state', source='submitted_SINAMECC_integration_changes', target='planning_integration_with_SINAMECC', conditions=[can_submit_plan_integration_SINAMECC], on_error='failed', permission='')
    def submit_plan_integration_SINAMECC(self):
        print('The mitigation action is transitioning from submitted_SINAMECC_integration_changes to planning_integration_with_SINAMECC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # implementing_SINAMECC_changes -> end
    def can_end_SINAMECC(self):
        # Transition condition logic goes here
        # Verify current state
        # - implementing_SINAMECC_changes
        return self.fsm_state == 'implementing_SINAMECC_changes'

    @transition(field='fsm_state', source='implementing_SINAMECC_changes', target='end', conditions=[can_end_SINAMECC], on_error='failed', permission='')
    def end_SINAMECC(self):
        print('The mitigation action is transitioning from implementing_SINAMECC_changes to end')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_conceptual_proposal_by_DCC -> decision_step_DCC_proposal
    def can_decide_DCC_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - implementing_SINAMECC_changes
        return self.fsm_state == 'in_evaluation_conceptual_proposal_by_DCC'

    @transition(field='fsm_state', source='in_evaluation_conceptual_proposal_by_DCC', target='decision_step_DCC_proposal', conditions=[can_decide_DCC_proposal], on_error='failed', permission='')
    def decide_DCC_proposal(self):
        print('The mitigation action is transitioning from in_evaluation_conceptual_proposal_by_DCC to decision_step_DCC_proposal')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_DCC_proposal -> conceptual_proposal_approved
    def can_approve_conceptual_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_conceptual_proposal_by_DCC
        return self.fsm_state == 'decision_step_DCC_proposal'

    @transition(field='fsm_state', source='decision_step_DCC_proposal', target='conceptual_proposal_approved', conditions=[can_approve_conceptual_proposal], on_error='failed', permission='')
    def approve_conceptual_proposal(self):
        print('The mitigation action is transitioning from decision_step_DCC_proposal to conceptual_proposal_approved')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_DCC_proposal -> changes_requested_to_conceptual_proposal
    def can_request_changes_conceptual_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_conceptual_proposal_by_DCC
        return self.fsm_state == 'decision_step_DCC_proposal'

    @transition(field='fsm_state', source='decision_step_DCC_proposal', target='changes_requested_to_conceptual_proposal', conditions=[can_request_changes_conceptual_proposal], on_error='failed', permission='')
    def request_changes_conceptual_proposal(self):
        print('The mitigation action is transitioning from decision_step_DCC_proposal to changes_requested_to_conceptual_proposal')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # planning_integration_with_SINAMECC -> decision_step_SINAMEC
    def can_decide_SINAMECC(self):
        # Transition condition logic goes here
        # Verify current state
        # - implementing_SINAMECC_changes
        return self.fsm_state == 'planning_integration_with_SINAMECC'

    @transition(field='fsm_state', source='planning_integration_with_SINAMECC', target='decision_step_SINAMEC', conditions=[can_decide_SINAMECC], on_error='failed', permission='')
    def decide_SINAMECC(self):
        print('The mitigation action is transitioning from planning_integration_with_SINAMECC to decision_step_SINAMEC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_SINAMEC -> SINAMECC_integration_approved
    def can_approve_SINAMECC_integration(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_SINAMEC
        return self.fsm_state == 'decision_step_SINAMEC'

    @transition(field='fsm_state', source='decision_step_SINAMEC', target='SINAMECC_integration_approved', conditions=[can_approve_SINAMECC_integration], on_error='failed', permission='')
    def approve_SINAMECC_integration(self):
        print('The mitigation action is transitioning from decision_step_SINAMEC to SINAMECC_integration_approved')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_SINAMEC -> SINAMECC_integration_changes_requested
    def can_request_changes_SINAMECC_integration(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_SINAMEC
        return self.fsm_state == 'decision_step_SINAMEC'

    @transition(field='fsm_state', source='decision_step_SINAMEC', target='SINAMECC_integration_changes_requested', conditions=[can_request_changes_SINAMECC_integration], on_error='failed', permission='')
    def request_changes_SINAMECC_integration(self):
        print('The mitigation action is transitioning from decision_step_SINAMEC to SINAMECC_integration_changes_requested')
        # Additional logic goes here.
        pass

    def __unicode__(self):
        return smart_unicode(self.name)

    

class ChangeLog(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=False)
    # Foreign Keys
    mitigation_action = models.ForeignKey(Mitigation, related_name='change_log')
    previous_status = models.CharField(max_length=100, null=True)
    current_status = models.CharField(max_length=100)
    
    user = models.ForeignKey(User, related_name='change_log')

    class Meta:
        verbose_name = _("ChangeLog")
        verbose_name_plural = _("ChangeLogs")
        ordering = ('date',)

    def __unicode__(self):
        return smart_unicode(self.name)
