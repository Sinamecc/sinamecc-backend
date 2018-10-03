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

    def can_submit(self):
        # Transition condition logic goes here
        # Verify current state
        # - new
        return self.fsm_state == 'new'

    @transition(field='fsm_state', source='new', target='submitted', conditions=[can_submit], on_error='failed', permission='')
    def submit(self):
        print('The mccr is transitioning from new to submitted')
        
        pass
    

    def can_assign_ovv_for_first_review(self):

        # Transition condition logic goes here
        # Verify current state
        # - submitted
        return self.fsm_state == 'submitted' or self.fsm_state == 'ovv_reject_assignation'
    
    @transition(field= 'fsm_state', source = 'submitted', target = 'ovv_assigned_first_review',conditions=[can_assign_ovv_for_first_review],  on_error = 'failed', permission = '')
    def assign_ovv_for_first_review(self):
        print('the mccr is transitioning from submitted to ovv_assigned_first_review')
        #send notification to DCC, assign OVV
        pass


    def can_ovv_assigned_send_notification(self):
        # Transition condition logic goes here
        # Verify current state
        # - ovv_assigned_first_review
        return self.fsm_state == 'ovv_assigned_first_review'
    
    @transition(field= 'fsm_state', source = 'ovv_assigned_first_review', target = 'ovv_assigned_notification', conditions=[can_ovv_assigned_send_notification],  on_error = 'failed', permission = '')
    def ovv_assigned_send_notification(self):
        print('the mccr is transitioning from ovv_assigned_first_review to ovv_assigned_notification')
        #logic to send notification
        pass


    def can_ovv_accept_reject(self):
        # Transition condition logic goes here
        # Verify current state
        # - ovv_assigned_notification
        return self.fsm_state == 'ovv_assigned_notification'
    
    @transition(field= 'fsm_state', source = 'ovv_assigned_notification', target = 'ovv_accept_reject', conditions=[can_ovv_accept_reject],on_error = 'failed', permission = '')
    def ovv_accept_reject(self):
        print('the mccr is transitioning from ovv_assigned_notification to ovv_accept_reject')
        #logic to send notification
        pass

    

    def can_reject_accept_assignation(self):
        # Transition condition logic goes here
        # Verify current state
        # - ovv_accept_reject
        return self.fsm_state == 'ovv_accept_reject'
    
    @transition(field= 'fsm_state', source = 'ovv_accept_reject', target = 'ovv_accept_assignation', conditions=[can_reject_accept_assignation],on_error = 'failed', permission = '')
    def accept_assignation(self):
        print('the mccr is transitioning from ovv_accept_reject to ovv_accept_assignation')
        
        pass
    
    @transition(field= 'fsm_state', source = 'ovv_accept_reject', target = 'ovv_reject_assignation', conditions=[can_reject_accept_assignation],on_error = 'failed', permission = '')
    def reject_assignation(self):
        print('the mccr is transitioning from ovv_accept_reject to ovv_reject_assignation')
       
        pass

    


    @transition(field= 'fsm_state', source = 'ovv_reject_assignation', target = 'ovv_assigned_first_review', conditions=[can_assign_ovv_for_first_review],on_error = 'failed', permission = '')
    def reject_assignation_send_first_review(self):
        print('the mccr is transitioning from ovv_reject_assignation to ovv_assigned_first_review')
       
        pass



    def can_upload_evaluation(self):
        # Transition condition logic goes here
        # Verify current state
        # - ovv_accept_assignation
        return self.fsm_state == 'ovv_accept_assignation'
    
    @transition(field= 'fsm_state', source = 'ovv_accept_assignation', target = 'ovv_upload_evaluation', conditions=[can_upload_evaluation],on_error = 'failed', permission = '')
    def upload_evaluation(self):
        print('the mccr is transitioning from ovv_accept_assignation to ovv_upload_evaluation')


        pass


    def can_reject_accept_request_changes_dp(self):
        # Transition condition logic goes here
        # Verify current state
        # - ovv_upload_evaluation
        #target -> ovv_reject_dp, ovv_accept_dp, ovv_request_changes_dp
        return self.fsm_state == 'ovv_upload_evaluation'
    
    @transition(field= 'fsm_state', source = 'ovv_upload_evaluation', target = 'ovv_reject_pd', conditions=[can_reject_accept_request_changes_dp],on_error = 'failed', permission = '')
    def reject_dp(self):
        print('the mccr is transitioning from ovv_upload_evaluation to ovv_reject_pd')

        #send notification 

        pass
    
    @transition(field= 'fsm_state', source = 'ovv_upload_evaluation', target = 'ovv_accept_dp', conditions=[can_reject_accept_request_changes_dp],on_error = 'failed', permission = '')
    def accept_dp(self):
        print('the mccr is transitioning from ovv_upload_evaluation to ovv_accept_dp')

        #send notification 

        pass
    
    @transition(field= 'fsm_state', source = 'ovv_upload_evaluation', target = 'ovv_request_changes_dp', conditions=[can_reject_accept_request_changes_dp],on_error = 'failed', permission = '')
    def request_changes_dp(self):
        print('the mccr is transitioning from ovv_upload_evaluation to ovv_request_changes_dp')

        #we need to define next state 

        pass


    def can_get_information_evaluation(self):
        # Transition condition logic goes here
        # Verify current state
        # - ovv_upload_evaluation
        #target -> ovv_reject_dp, ovv_accept_dp, ovv_request_changes_dp
        return self.fsm_state == 'ovv_upload_evaluation'
    
    @transition(field= 'fsm_state', source = 'ovv_accept_dp', target = 'ovv_secretary_get_information_', conditions=[can_get_information_evaluation],on_error = 'failed', permission = '')
    def get_information_evaluation(self):
        print('the mccr is transitioning from ovv_accept_dp to ovv_secretary_get_information_')

        #send notification and logic .

        pass

    def can_evaluate_mccr(self):
        # Transition condition logic goes here
        # Verify current state
        # - ovv_upload_evaluation
        #target -> ovv_reject_dp, ovv_accept_dp, ovv_request_changes_dp
        return self.fsm_state == 'ovv_secretary_get_information_'
    
    @transition(field= 'fsm_state', source = 'ovv_secretary_get_information_', target = 'mccr_on_evaluation_by_secretary', conditions=[can_evaluate_mccr],on_error = 'failed', permission = '')
    def evaluate_mccr(self):
        print('the mccr is transitioning from ovv_secretary_get_information_ to mccr_on_evaluation_by_secretary')

        #send notification and logic .

        pass
    
    def can_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - ovv_upload_evaluation
        #target -> ovv_reject_dp, ovv_accept_dp, ovv_request_changes_dp
        return self.fsm_state == 'mccr_on_evaluation_by_secretary'
    
    @transition(field= 'fsm_state', source = 'mccr_on_evaluation_by_secretary', target = 'end', conditions=[can_end],on_error = 'failed', permission = '')
    def end(self):
        print('the mccr is transitioning from mccr_on_evaluation_by_secretary to end')

        #send notification and logic .

        pass
    

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