from __future__ import unicode_literals
from django.conf import settings

import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from workflow.models import Comment, ReviewStatus
from django_fsm import FSMField, transition

User =  get_user_model()

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

class Finance(models.Model):
    finance_source_type = models.ForeignKey(FinanceSourceType, related_name='finance', blank=False, null=False)
    source = models.CharField(max_length=100, blank=False, null=False)

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

class Mitigation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strategy_name = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    purpose = models.CharField(max_length=500, blank=False, null=False)
    quantitative_purpose = models.CharField(max_length=500, blank=False, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    gas_inventory = models.CharField(max_length=100, blank=False, null=False)
    emissions_source = models.CharField(max_length=100, blank=False, null=False)
    carbon_sinks = models.CharField(max_length=100, blank=False, null=False)
    impact_plan = models.CharField(max_length=500, blank=False, null=False)
    impact = models.CharField(max_length=500, blank=False, null=False)
    bibliographic_sources = models.CharField(max_length=500, blank=False, null=False)
    is_international = models.BooleanField(blank=False, null=False)
    international_participation = models.CharField(max_length=100, blank=False, null=False)
    sustainability = models.CharField(max_length=500, blank=False, null=False)
    question_ucc = models.CharField(max_length=500, blank=False, null=True)
    question_ovv = models.CharField(max_length=500, blank=False, null=False)

    # Foreign Keys
    user = models.ForeignKey(User, related_name='mitigation_action')
    registration_type = models.ForeignKey(RegistrationType, related_name='mitigation_action')
    institution = models.ForeignKey(Institution, related_name='mitigation_action')
    contact = models.ForeignKey(Contact, related_name='mitigation_action')
    status = models.ForeignKey(Status, related_name='mitigation_action')
    progress_indicator = models.ForeignKey(ProgressIndicator, related_name='mitigation_action')
    finance = models.ForeignKey(Finance, related_name='mitigation_action')
    ingei_compliances = models.ManyToManyField(IngeiCompliance)
    geographic_scale = models.ForeignKey(GeographicScale, related_name='mitigation_action')
    location = models.ForeignKey(Location, related_name='mitigation_action')

    # Workflow
    review_count = models.IntegerField(null=True, blank=True, default=0)
    comments = models.ManyToManyField(Comment, blank=True)
    fsm_state = FSMField(default='new', protected=True)

    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("MitigationAccess")
        verbose_name_plural = _("MitigationAccesses")
        ordering = ('created',)

    # FSM Annotated Methods (Transitions) and Ordinary Conditions
    # --- Transition ---
    # new -> submitted
    def can_submit(self):
        # Transition condition logic goes here
        return True

    @transition(field='fsm_state', source='new', target='submitted', conditions=[can_submit], on_error='failed', permission='')
    def submit(self):
        print('The mitigation action has been submitted')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_by_DCC -> submit_evaluation_DCC
    def can_submit_DCC(self):
        # Transition condition logic goes here
        # Verify possible previous states
        # - submitted
        # - updating_by_request
        return self.fsm_state == 'submitted' or self.fsm_state == 'updating_by_request'

    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='submit_evaluation_DCC', conditions=[can_submit_DCC], on_error='failed', permission='')
    def submit_DCC(self):
        print('The mitigation action is in DCC evaluation submission.')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_evaluation_DCC -> changes_requested_by_DCC
    def can_change_DCC(self):
        # Transition condition logic goes here
        # Verify possible previous states
        # - in_evaluation_by_DCC
        return self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='submit_evaluation_DCC', target='changes_requested_by_DCC', conditions=[can_change_DCC], on_error='failed', permission='')
    def change_DCC(self):
        print('The mitigation action is in changes requested by DCC.')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_evaluation_DCC -> rejected_by_DCC
    def can_reject_DCC(self):
        # Transition condition logic goes here
        # Verify possible previous states
        # - in_evaluation_by_DCC
        return self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='submit_evaluation_DCC', target='rejected_by_DCC', conditions=[can_reject_DCC], on_error='failed', permission='')
    def reject_DCC(self):
        print('The mitigation action is in rejected by DCC.')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_evaluation_DCC -> registering
    def can_register(self):
        # Transition condition logic goes here
        # Verify possible previous states
        # - in_evaluation_by_DCC
        return self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='submit_evaluation_DCC', target='registering', conditions=[can_register], on_error='failed', permission='')
    def register(self):
        print('The mitigation action is in registering.')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # changes_requested_by_DCC -> updating_by_request
    def can_update_by_request(self):
        # Transition condition logic goes here
        # Verify possible previous states
        # - in_evaluation_by_DCC
        return self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='changes_requested_by_DCC', target='updating_by_request', conditions=[can_update_by_request], on_error='failed', permission='')
    def update_by_request(self):
        print('The mitigation action is in update by request.')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # rejected_by_DCC -> end
    def can_end(self):
        # Transition condition logic goes here
        # Verify possible previous states
        # - in_evaluation_by_DCC
        return self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='rejected_by_DCC', target='end', conditions=[can_end], on_error='failed', permission='')
    def end(self):
        print('The mitigation action is in end.')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # registering -> in_evaluation_INGEI_by_DCC_IMN
    def can_evaluate_INGEI(self):
        # Transition condition logic goes here
        # Verify possible previous states
        # - in_evaluation_by_DCC
        return self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='registering', target='in_evaluation_INGEI_by_DCC_IMN', conditions=[can_evaluate_INGEI], on_error='failed', permission='')
    def evaluate_INGEI(self):
        print('The mitigation action is in INGEI evaluation.')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # updating_by_request -> in_evaluation_by_DCC
    def can_evaluate_DCC(self):
        # Transition condition logic goes here
        # Verify possible previous states
        # - changes_requested_by_DCC
        return self.fsm_state == 'changes_requested_by_DCC'

    @transition(field='fsm_state', source='updating_by_request', target='in_evaluation_by_DCC', conditions=[can_evaluate_DCC], on_error='failed', permission='')
    def evaluate_DCC(self):
        print('The mitigation action is in DCC evaluation.')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_INGEI_by_DCC_IMN -> submit_INGEI_harmonization_required
    def can_submit_INGEI(self):
        # Transition condition logic goes here
        # Verify possible previous states
        # - registering
        return self.fsm_state == 'registering'

    @transition(field='fsm_state', source='in_evaluation_INGEI_by_DCC_IMN', target='submit_INGEI_harmonization_required', conditions=[can_submit_INGEI], on_error='failed', permission='')
    def submit_INGEI(self):
        print('The mitigation action is in INGEI Harmonization.')
        # Additional logic goes here.
        pass

    def __unicode__(self):
        return smart_unicode(self.name)

class ChangeLog(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=False)
    # Foreign Keys
    mitigation_action = models.ForeignKey(Mitigation, related_name='change_log')
    previous_status = models.ForeignKey(ReviewStatus, null=True, related_name='change_log_previous')
    current_status = models.ForeignKey(ReviewStatus, related_name='change_log_current')
    
    user = models.ForeignKey(User, related_name='change_log')

    class Meta:
        verbose_name = _("ChangeLog")
        verbose_name_plural = _("ChangeLogs")
        ordering = ('date',)

    def __unicode__(self):
        return smart_unicode(self.name)
