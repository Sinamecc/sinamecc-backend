from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from general.storages import PrivateMediaStorage
from mitigation_action.models import Mitigation
from workflow.models import Comment, ReviewStatus
from django_fsm import FSMField, transition
import uuid

User =  get_user_model()

class MCCRUserType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("MCCRUserType")
        verbose_name_plural = _("MCCRUserTypes")

    def __unicode__(self):
        return smart_unicode(self.name)

# TODO: fix upload_to to include MCCR UUID
class MCCRRegistry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50, blank=False, null=False)
    user = models.ForeignKey(User, related_name='mccr')
    mitigation = models.ForeignKey(Mitigation, related_name='mccr')
    fsm_state = FSMField(default='new', protected=True)
    user_type = models.ForeignKey(MCCRUserType, related_name='mccr')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("MCCRRegistry")
        verbose_name_plural = _("MCCRRegistries")

    def __unicode__(self):
        return smart_unicode(self.id)

    # FSM Annotated Methods (Transitions) and Ordinary Conditions
    # --- Transition ---
    # new -> mccr_submitted
    def can_submit(self):
        # Transition condition logic goes here
        # Verify current state
        # - new
        return self.fsm_state == 'new'

    @transition(field='fsm_state', source='new', target='mccr_submitted', conditions=[can_submit], on_error='failed', permission='')
    def submit(self):
        print('The MCCR is transitioning from new to mccr_submitted')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_submitted -> mccr_ovv_assigned_first_review
    def can_assign_ovv_for_first_review(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_submitted
        return self.fsm_state == 'mccr_submitted' or self.fsm_state == 'ovv_reject_assignation'

    @transition(field= 'fsm_state', source = 'mccr_submitted', target = 'mccr_ovv_assigned_first_review',conditions=[can_assign_ovv_for_first_review], on_error = 'failed', permission = '')
    def assign_ovv_for_first_review(self):
        print('The MCCR is transitioning from mccr_submitted to mccr_ovv_assigned_first_review')
        # Notify to DCC, assign OVV
        # self.notify_submission_DCC()
        pass

    # --- Transition ---
    # mccr_ovv_assigned_first_review -> mccr_ovv_assigned_notification
    def can_ovv_assigned_send_notification(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_assigned_first_review
        return self.fsm_state == 'mccr_ovv_assigned_first_review'

    @transition(field= 'fsm_state', source = 'mccr_ovv_assigned_first_review', target = 'mccr_ovv_assigned_notification',conditions=[can_ovv_assigned_send_notification],  on_error = 'failed', permission = '')
    def assigned_send_notification(self):
        print('The MCCR is transitioning from mccr_ovv_assigned_first_review to mccr_ovv_assigned_notification')
        # Additional logic goes here.
        # self.notify()
        pass

    # --- Transition ---
    # mccr_ovv_assigned_notification -> mccr_ovv_accept_reject
    def can_ovv_accept_reject(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_assigned_notification
        return self.fsm_state == 'mccr_ovv_assigned_notification'

    @transition(field= 'fsm_state', source = 'mccr_ovv_assigned_notification', target = 'mccr_ovv_accept_reject',conditions=[can_ovv_accept_reject], on_error = 'failed', permission = '')
    def ovv_accept_reject(self):
        print('The MCCR is transitioning from mccr_ovv_assigned_notification to mccr_ovv_accept_reject')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_accept_reject -> mccr_ovv_accept_assignation
    def can_ovv_accept_assignation(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_reject
        return self.fsm_state == 'mccr_ovv_accept_reject'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_reject', target = 'mccr_ovv_accept_assignation',conditions=[can_ovv_accept_assignation], on_error = 'failed', permission = '')
    def ovv_accept_assignation(self):
        print('The MCCR is transitioning from mccr_ovv_accept_reject to mccr_ovv_accept_assignation')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_accept_reject -> mccr_ovv_reject_assignation
    def can_ovv_reject_assignation(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_reject
        return self.fsm_state == 'mccr_ovv_accept_reject'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_reject', target = 'mccr_ovv_reject_assignation',conditions=[can_ovv_reject_assignation], on_error = 'failed', permission = '')
    def reject_assignation(self):
        print('The MCCR is transitioning from mccr_ovv_accept_reject to mccr_ovv_reject_assignation')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_accept_assignation -> mccr_ovv_upload_evaluation
    def can_ovv_upload_evaluation(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_assignation
        return self.fsm_state == 'mccr_ovv_accept_assignation'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_assignation', target = 'mccr_ovv_upload_evaluation',conditions=[can_ovv_upload_evaluation], on_error = 'failed', permission = '')
    def ovv_upload_evaluation(self):
        print('The MCCR is transitioning from mccr_ovv_accept_assignation to mccr_ovv_upload_evaluation')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_reject_assignation -> mccr_ovv_assigned_first_review
    def can_ovv_assigned_first_review(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_reject_assignation
        return self.fsm_state == 'mccr_ovv_reject_assignation'

    @transition(field= 'fsm_state', source = 'mccr_ovv_reject_assignation', target = 'mccr_ovv_assigned_first_review',conditions=[can_ovv_assigned_first_review], on_error = 'failed', permission = '')
    def ovv_assigned_first_review(self):
        print('The MCCR is transitioning from mccr_ovv_reject_assignation to mccr_ovv_assigned_first_review')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_upload_evaluation -> mccr_ovv_accept_dp
    def can_ovv_accept_dp(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_upload_evaluation
        return self.fsm_state == 'mccr_ovv_upload_evaluation'

    @transition(field= 'fsm_state', source = 'mccr_ovv_upload_evaluation', target = 'mccr_ovv_accept_dp',conditions=[can_ovv_accept_dp], on_error = 'failed', permission = '')
    def ovv_accept_dp(self):
        print('The MCCR is transitioning from mccr_ovv_upload_evaluation to mccr_ovv_accept_dp')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_upload_evaluation -> mccr_ovv_reject_dp
    def can_ovv_reject_dp(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_upload_evaluation
        return self.fsm_state == 'mccr_ovv_upload_evaluation'

    @transition(field= 'fsm_state', source = 'mccr_ovv_upload_evaluation', target = 'mccr_ovv_reject_dp',conditions=[can_ovv_reject_dp], on_error = 'failed', permission = '')
    def ovv_reject_dp(self):
        print('The MCCR is transitioning from mccr_ovv_upload_evaluation to mccr_ovv_reject_dp')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_upload_evaluation -> mccr_ovv_request_changes_dp
    def can_ovv_request_changes_dp(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_upload_evaluation
        return self.fsm_state == 'mccr_ovv_upload_evaluation'

    @transition(field= 'fsm_state', source = 'mccr_ovv_upload_evaluation', target = 'mccr_ovv_request_changes_dp',conditions=[can_ovv_request_changes_dp], on_error = 'failed', permission = '')
    def ovv_request_changes_dp(self):
        print('The MCCR is transitioning from mccr_ovv_upload_evaluation to mccr_ovv_request_changes_dp')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_accept_dp -> mccr_secretary_get_information
    def can_secretary_get_information(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_dp
        return self.fsm_state == 'mccr_ovv_accept_dp'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_dp', target = 'mccr_secretary_get_information',conditions=[can_secretary_get_information], on_error = 'failed', permission = '')
    def secretary_get_information(self):
        print('The MCCR is transitioning from mccr_ovv_accept_dp to mccr_secretary_get_information')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_secretary_get_information -> mccr_on_evaluation_by_secretary
    def can_evaluate_by_secretary(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_secretary_get_information
        return self.fsm_state == 'mccr_secretary_get_information'

    @transition(field= 'fsm_state', source = 'mccr_secretary_get_information', target = 'mccr_on_evaluation_by_secretary',conditions=[can_evaluate_by_secretary], on_error = 'failed', permission = '')
    def evaluate_by_secretary(self):
        print('The MCCR is transitioning from mccr_secretary_get_information to mccr_on_evaluation_by_secretary')
        # Additional logic goes here.
        pass

    def can_secretary_proceed(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_on_evaluation_by_secretary
        return self.fsm_state == 'mccr_on_evaluation_by_secretary'

    @transition(field= 'fsm_state', source = 'mccr_on_evaluation_by_secretary', target = 'mccr_secretary_can_proceed',conditions=[can_secretary_proceed], on_error = 'failed', permission = '')
    def secretary_can_proceed(self):
        print('The MCCR is transitioning from mccr_on_evaluation_by_secretary to mccr_secretary_can_proceed')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # * -> mccr_end
    @transition(field= 'fsm_state', source = '*', target = 'mccr_end', on_error = 'failed', permission = '')
    def mccr_end(self):
        # to do: narrow down statuses where it can transition
        print('The MCCR is transitioning from any state to mccr_end')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_on_evaluation_by_secretary -> mccr_end

    # --- Transition ---
    # mccr_secretary_can_proceed -> mccr_end
    
class ChangeLog(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=False)
    # Foreign Keys
    ppcn = models.ForeignKey(MCCRRegistry, related_name='change_log')
    previous_status = models.CharField(max_length=100, null=True)
    current_status = models.CharField(max_length=100)
    
    user = models.ForeignKey(User, related_name='change_log_mccr')

    class Meta:
        verbose_name = _("ChangeLog")
        verbose_name_plural = _("ChangeLogs")
        ordering = ('date',)

    def __unicode__(self):
        return smart_unicode(self.name)


class MCCRFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(blank=False, null=False, upload_to='mccr/%Y%m%d/%H%M%S', storage=PrivateMediaStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mccr = models.ForeignKey(MCCRRegistry, related_name='files', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("MCCRFile")
        verbose_name_plural = _("MCCRFiles")

    def __unicode__(self):
        return smart_unicode(self.name)

class OVV(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    email = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=30, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Organismo Validador Verifador")
        verbose_name_plural = _("Organismos Validadores Verificadores")

    def __unicode__(self):
        return smart_unicode(self.name)

class MCCRRegistryOVVRelation(models.Model):
    mccr = models.ForeignKey(MCCRRegistry, on_delete=models.CASCADE)
    ovv = models.ForeignKey(OVV, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("MCCR OVV Relation")
        verbose_name_plural = _("MCCR OVV Relations")

    def __unicode__(self):
        return smart_unicode(self.name)