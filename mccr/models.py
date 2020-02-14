from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from general.storages import PrivateMediaStorage
from mitigation_action.models import Mitigation
from workflow.models import Comment, ReviewStatus
from django_fsm import FSMField, transition
import uuid
from mccr.email_services import MCCREmailServices
from general.services import EmailServices
from general.permissions import PermissionsHelper
User =  get_user_model()
ses_service = EmailServices()
permission = PermissionsHelper()

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

        permissions = (

            ("user_dcc_permission", "user DCC permision MCCR"),
            ("user_executive_secretary_permission", "user executive secretary permission MCCR"),
            ("user_validating_organizations_permission", "User Validating Organizations MCCR"),
            ("can_provide_information", "Can provide information MCCR"),
            ("user_executive_committee_permissions","User Executive Committee MCCR") 

        )

    def __unicode__(self):
        return smart_unicode(self.id)

    # FSM Annotated Methods (Transitions) and Ordinary Conditions
    # --- Transition ---
    # new -> mccr_submitted
    def can_submit(self):
        # Transition condition logic goes here
        # Verify current state
        # self.notify_submission_dcc
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

    @transition(field= 'fsm_state', source = 'mccr_submitted', target = 'mccr_ovv_assigned_first_review',conditions=[can_assign_ovv_for_first_review], on_error = 'failed', permission='')
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

    @transition(field= 'fsm_state', source = 'mccr_ovv_assigned_first_review', target = 'mccr_ovv_assigned_notification',conditions=[can_ovv_assigned_send_notification],  on_error = 'failed', permission='')
    def assigned_send_notification(self):
        print('The MCCR is transitioning from mccr_ovv_assigned_first_review to mccr_ovv_assigned_notification')
        # Additional logic goes here.
        # We need to identify ovv  
        mccr_ovv = MCCRRegistryOVVRelation.objects.filter(mccr = self.id).latest('id')
        ovv = mccr_ovv.ovv
        email_services = MCCREmailServices(ses_service)
        result = email_services.notify_submission_ovv(self, ovv)
        return result
        

    # --- Transition ---
    # mccr_ovv_assigned_notification -> mccr_ovv_accept_reject
    def can_ovv_accept_reject(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_assigned_notification
        return self.fsm_state == 'mccr_ovv_assigned_notification'

    @transition(field= 'fsm_state', source = 'mccr_ovv_assigned_notification', target = 'mccr_ovv_accept_reject',conditions=[can_ovv_accept_reject], on_error = 'failed', permission='')
    def ovv_accept_reject(self):
        print('The MCCR is transitioning from mccr_ovv_assigned_notification to mccr_ovv_accept_reject')
        # Additional logic goes here.
        # self.notify()
    # --- Transition ---
    # mccr_ovv_accept_reject -> mccr_ovv_accept_assignation
    def can_ovv_accept_assignation(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_reject
        return self.fsm_state == 'mccr_ovv_accept_reject'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_reject', target = 'mccr_ovv_accept_assignation',conditions=[can_ovv_accept_assignation], on_error = 'failed', permission='')
    def ovv_accept_assignation(self):
        print('The MCCR is transitioning from mccr_ovv_accept_reject to mccr_ovv_accept_assignation')
        # Additional logic goes here.
      


    # --- Transition ---
    # mccr_ovv_accept_reject -> mccr_ovv_reject_assignation
    def can_ovv_reject_assignation(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_reject
        return self.fsm_state == 'mccr_ovv_accept_reject'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_reject', target = 'mccr_ovv_reject_assignation',conditions=[can_ovv_reject_assignation], on_error = 'failed', permission='')
    def reject_assignation(self):
        print('The MCCR is transitioning from mccr_ovv_accept_reject to mccr_ovv_reject_assignation')
        # Additional logic goes here.
       
    # --- Transition ---
    # mccr_ovv_accept_assignation -> mccr_ovv_upload_evaluation
    def can_ovv_upload_evaluation(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_assignation
        return self.fsm_state == 'mccr_ovv_accept_assignation'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_assignation', target = 'mccr_ovv_upload_evaluation',conditions=[can_ovv_upload_evaluation], on_error = 'failed', permission='')
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

    @transition(field= 'fsm_state', source = 'mccr_ovv_reject_assignation', target = 'mccr_ovv_assigned_first_review',conditions=[can_ovv_assigned_first_review], on_error = 'failed', permission='')
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

    @transition(field= 'fsm_state', source = 'mccr_ovv_upload_evaluation', target = 'mccr_ovv_accept_dp',conditions=[can_ovv_accept_dp], on_error = 'failed', permission='')
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

    @transition(field= 'fsm_state', source = 'mccr_ovv_upload_evaluation', target = 'mccr_ovv_reject_dp',conditions=[can_ovv_reject_dp], on_error = 'failed', permission='')
    def ovv_reject_dp(self):
        print('The MCCR is transitioning from mccr_ovv_upload_evaluation to mccr_ovv_reject_dp')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_reject_dp -> mccr_end
    def can_ovv_dp_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_reject_dp
        return self.fsm_state == 'mccr_ovv_reject_dp'

    @transition(field= 'fsm_state', source = 'mccr_ovv_reject_dp', target = 'mccr_end',conditions=[can_ovv_dp_end], on_error = 'failed', permission='')
    def ovv_dp_end(self):
        print('The MCCR is transitioning from mccr_ovv_reject_dp to mccr_end')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_upload_evaluation -> mccr_ovv_request_changes_dp
    def can_ovv_request_changes_dp(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_upload_evaluation
        return self.fsm_state == 'mccr_ovv_upload_evaluation'

    @transition(field= 'fsm_state', source = 'mccr_ovv_upload_evaluation', target = 'mccr_ovv_request_changes_dp',conditions=[can_ovv_request_changes_dp], on_error = 'failed', permission='')
    def ovv_request_changes_dp(self):
        print('The MCCR is transitioning from mccr_ovv_upload_evaluation to mccr_ovv_request_changes_dp')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_request_changes_dp -> mccr_updating_dp_by_ovv_request
    def can_update_dp_by_ovv_request(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_request_changes_dp
        return self.fsm_state == 'mccr_ovv_request_changes_dp'

    @transition(field='fsm_state', source='mccr_ovv_request_changes_dp', target='mccr_updating_dp_by_ovv_request', conditions=[can_update_dp_by_ovv_request], on_error='failed', permission='')
    def updating_dp_by_ovv_request(self):
        print('The MCCR is transitioning from mccr_ovv_request_changes_dp to mccr_updating_dp_by_ovv_request')
      
        # Additional logic goes here.
        pass


    # --- Transition ---
    # mccr_updating_dp_by_ovv_request -> mccr_ovv_accept_assignation
    def can_ovv_download_updated_dp(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_updating_dp_by_ovv_request
        return self.fsm_state == 'mccr_updating_dp_by_ovv_request'

    @transition(field= 'fsm_state', source = 'mccr_updating_dp_by_ovv_request', target = 'mccr_ovv_accept_assignation',conditions=[can_ovv_download_updated_dp], on_error = 'failed', permission='')
    def ovv_download_updated_dp(self):
        print('The MCCR is transitioning from mccr_updating_dp_by_ovv_request to mccr_ovv_accept_assignation')
        # Additional logic goes here.
       

    # --- Transition ---
    # mccr_ovv_accept_dp -> mccr_secretary_get_dp_information
    def can_secretary_get_dp_information(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_dp
        return self.fsm_state == 'mccr_ovv_accept_dp'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_dp', target = 'mccr_secretary_get_dp_information',conditions=[can_secretary_get_dp_information], on_error = 'failed', permission='')
    def secretary_get_dp_information(self):
        print('The MCCR is transitioning from mccr_ovv_accept_dp to mccr_secretary_get_dp_information')
        # Additional logic goes here.
        
    # --- Transition ---
    # mccr_secretary_get_dp_information -> mccr_on_dp_evaluation_by_secretary
    def can_evaluate_dp_by_secretary(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_secretary_get_dp_information
        return self.fsm_state == 'mccr_secretary_get_dp_information'

    @transition(field= 'fsm_state', source = 'mccr_secretary_get_dp_information', target = 'mccr_on_dp_evaluation_by_secretary',conditions=[can_evaluate_dp_by_secretary], on_error = 'failed', permission='')
    def evaluate_dp_by_secretary(self):
        print('The MCCR is transitioning from mccr_secretary_get_dp_information to mccr_on_dp_evaluation_by_secretary')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_on_dp_evaluation_by_secretary -> mccr_secretary_can_proceed_dp
    def can_secretary_proceed_dp(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_on_dp_evaluation_by_secretary
        return self.fsm_state == 'mccr_on_dp_evaluation_by_secretary'

    @transition(field= 'fsm_state', source = 'mccr_on_dp_evaluation_by_secretary', target = 'mccr_secretary_can_proceed_dp',conditions=[can_secretary_proceed_dp], on_error = 'failed', permission='')
    def secretary_can_proceed_dp(self):
        print('The MCCR is transitioning from mccr_on_dp_evaluation_by_secretary to mccr_secretary_can_proceed_dp')
        # Additional logic goes here.
        pass

    
    # --- Transition ---
    # mccr_on_dp_evaluation_by_secretary -> mccr_end
    def can_secretary_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_on_dp_evaluation_by_secretary
        return self.fsm_state == 'mccr_on_dp_evaluation_by_secretary'

    @transition(field= 'fsm_state', source = 'mccr_on_dp_evaluation_by_secretary', target = 'mccr_end', conditions=[can_secretary_end], on_error = 'failed', permission='')
    def secretary_end(self):
        print('The MCCR is transitioning from mccr_on_dp_evaluation_by_secretary to mccr_end')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_secretary_can_proceed_dp -> mccr_secretary_reject_dp_environmental_concerns
    def can_secretary_reject_dp_environmental_concerns(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_secretary_can_proceed_dp
        return self.fsm_state == 'mccr_secretary_can_proceed_dp'

    @transition(field= 'fsm_state', source = 'mccr_secretary_can_proceed_dp', target = 'mccr_secretary_reject_dp_environmental_concerns', conditions=[can_secretary_reject_dp_environmental_concerns], on_error = 'failed', permission='')
    def secretary_reject_dp_environmental_concerns(self):
        print('The MCCR is transitioning from mccr_secretary_can_proceed_dp to mccr_secretary_reject_dp_environmental_concerns')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_secretary_reject_dp_environmental_concerns -> mccr_end
    def can_secretary_dp_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_secretary_reject_dp_environmental_concerns
        return self.fsm_state == 'mccr_secretary_reject_dp_environmental_concerns'

    @transition(field= 'fsm_state', source = 'mccr_secretary_reject_dp_environmental_concerns', target = 'mccr_end', conditions=[can_secretary_dp_end], on_error = 'failed', permission='')
    def secretary_dp_end(self):
        print('The MCCR is transitioning from mccr_secretary_reject_dp_environmental_concerns to mccr_end')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_secretary_can_proceed_dp -> mccr_refer_validation_dp_report
    def can_refer_validation_dp_report(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_secretary_can_proceed_dp
        return self.fsm_state == 'mccr_secretary_can_proceed_dp'

    @transition(field= 'fsm_state', source = 'mccr_secretary_can_proceed_dp', target = 'mccr_refer_validation_dp_report', conditions=[can_refer_validation_dp_report], on_error = 'failed', permission='')
    def refer_validation_dp_report(self):
        print('The MCCR is transitioning from mccr_secretary_can_proceed_dp to mccr_refer_validation_dp_report')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_refer_validation_dp_report -> mccr_in_exec_committee_evaluation
    def can_exec_committee_evaluate(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_refer_validation_report
        return self.fsm_state == 'mccr_refer_validation_dp_report'

    @transition(field= 'fsm_state', source = 'mccr_refer_validation_dp_report', target = 'mccr_in_exec_committee_evaluation', conditions=[can_exec_committee_evaluate], on_error = 'failed', permission='')
    def exec_committee_evaluate(self):
        print('The MCCR is transitioning from mccr_refer_validation_dp_report to mccr_in_exec_committee_evaluation')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_in_exec_committee_evaluation -> mccr_communicate_conditions
    def can_communicate_conditions(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_in_exec_committee_evaluation
        return self.fsm_state == 'mccr_in_exec_committee_evaluation'

    @transition(field= 'fsm_state', source = 'mccr_in_exec_committee_evaluation', target = 'mccr_communicate_conditions', conditions=[can_communicate_conditions], on_error = 'failed', permission='')
    def communicate_conditions(self):
        print('The MCCR is transitioning from mccr_in_exec_committee_evaluation to mccr_communicate_conditions')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_in_exec_committee_evaluation -> mccr_exec_committee_reject
    def can_committee_reject(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_in_exec_committee_evaluation
        return self.fsm_state == 'mccr_in_exec_committee_evaluation'

    @transition(field= 'fsm_state', source = 'mccr_in_exec_committee_evaluation', target = 'mccr_exec_committee_reject', conditions=[can_committee_reject], on_error = 'failed', permission='')
    def committee_reject(self):
        print('The MCCR is transitioning from mccr_in_exec_committee_evaluation to mccr_exec_committee_reject')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_in_exec_committee_evaluation -> mccr_project_monitoring
    def can_monitor_project(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_in_exec_committee_evaluation
        return self.fsm_state == 'mccr_in_exec_committee_evaluation'

    @transition(field= 'fsm_state', source = 'mccr_in_exec_committee_evaluation', target = 'mccr_project_monitoring', conditions=[can_monitor_project], on_error = 'failed', permission='')
    def monitor_project(self):
        print('The MCCR is transitioning from mccr_in_exec_committee_evaluation to mccr_project_monitoring')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_exec_committee_reject -> mccr_end
    def can_committee_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_exec_committee_reject
        return self.fsm_state == 'mccr_exec_committee_reject'

    @transition(field= 'fsm_state', source = 'mccr_exec_committee_reject', target = 'mccr_end', conditions=[can_committee_end], on_error = 'failed', permission='')
    def committee_end(self):
        print('The MCCR is transitioning from mccr_exec_committee_reject to mccr_end')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_project_monitoring -> mccr_upload_report_sinamecc
    def can_upload_report_sinamecc(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_project_monitoring
        return self.fsm_state == 'mccr_project_monitoring'

    @transition(field= 'fsm_state', source = 'mccr_project_monitoring', target = 'mccr_upload_report_sinamecc', conditions=[can_upload_report_sinamecc], on_error = 'failed', permission='')
    def upload_report_sinamecc(self):
        print('The MCCR is transitioning from mccr_project_monitoring to mccr_upload_report_sinamecc')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_upload_report_sinamecc -> mccr_ovv_assigned
    def can_ovv_assign(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_upload_report_sinamecc
        return self.fsm_state == 'mccr_upload_report_sinamecc'

    @transition(field= 'fsm_state', source = 'mccr_upload_report_sinamecc', target = 'mccr_ovv_assigned', conditions=[can_ovv_assign], on_error = 'failed', permission='')
    def ovv_assign(self):
        print('The MCCR is transitioning from mccr_upload_report_sinamecc to mccr_ovv_assigned')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_assigned -> mccr_ovv_accept_reject
    def can_ovv_accept(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_assigned
        return self.fsm_state == 'mccr_ovv_assigned'

    @transition(field= 'fsm_state', source = 'mccr_ovv_assigned', target = 'mccr_ovv_accept_reject_monitoring', conditions=[can_ovv_accept], on_error = 'failed', permission='')
    def ovv_accept(self):
        print('The MCCR is transitioning from mccr_ovv_assigned to mccr_ovv_accept_reject_monitoring')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_accept_reject -> mccr_ovv_accept_assignation
    def can_ovv_accept_assignation_monitoring(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_reject
        return self.fsm_state == 'mccr_ovv_accept_reject_monitoring'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_reject_monitoring', target = 'mccr_ovv_accept_assignation_monitoring', conditions=[can_ovv_accept_assignation_monitoring], on_error = 'failed', permission='')
    def ovv_accept_assignation_monitoring(self):
        print('The MCCR is transitioning from mccr_ovv_accept_reject_monitoring to mccr_ovv_accept_assignation_monitoring')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_accept_assignation -> mccr_ovv_upload_evaluation
    def can_ovv_upload_evaluation_monitoring(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_assignation
        return self.fsm_state == 'mccr_ovv_accept_assignation_monitoring'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_assignation_monitoring', target = 'mccr_ovv_upload_evaluation_monitoring', conditions=[can_ovv_upload_evaluation_monitoring], on_error = 'failed', permission='')
    def ovv_upload_evaluation_monitoring(self):
        print('The MCCR is transitioning from mccr_ovv_accept_assignation_monitoring to mccr_ovv_upload_evaluation_monitoring')
        # Additional logic goes here.
        pass

    def can_decision_step_ovv_evaluation_monitoring(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_upload_evaluation_monitoring
        return self.fsm_state == 'mccr_ovv_upload_evaluation_monitoring'



    @transition(field= 'fsm_state', source = 'mccr_ovv_upload_evaluation_monitoring', target = 'mccr_decision_step_ovv_evaluation_monitoring', conditions=[can_decision_step_ovv_evaluation_monitoring], on_error = 'failed', permission='')
    def decision_step_ovv_evaluation_monitoring(self):
        print('The MCCR is transitioning from mccr_ovv_upload_evaluation_monitoring to mccr_decision_step_ovv_evaluation_monitoring')
        # Additional logic goes here.
        pass




    # --- Transition ---
    # mccr_ovv_upload_evaluation -> mccr_ovv_reject_monitoring
    def can_ovv_reject_monitoring(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_upload_evaluation
        return self.fsm_state == 'mccr_decision_step_ovv_evaluation_monitoring'

    @transition(field= 'fsm_state', source = 'mccr_decision_step_ovv_evaluation_monitoring', target = 'mccr_ovv_reject_monitoring', conditions=[can_ovv_reject_monitoring], on_error = 'failed', permission='')
    def ovv_reject_monitoring(self):
        print('The MCCR is transitioning from mccr_decision_step_ovv_evaluation_monitoring to mccr_ovv_reject_monitoring')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_upload_evaluation -> mccr_ovv_request_changes_monitoring
    def can_ovv_request_changes_monitoring(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_upload_evaluation
        return self.fsm_state == 'mccr_decision_step_ovv_evaluation_monitoring'
    
    @transition(field= 'fsm_state', source = 'mccr_decision_step_ovv_evaluation_monitoring', target = 'mccr_ovv_request_changes_monitoring', conditions=[can_ovv_request_changes_monitoring], on_error = 'failed', permission='')
    def ovv_request_changes_monitoring(self):
        print('The MCCR is transitioning from mccr_decision_step_ovv_evaluation_monitoring to mccr_ovv_request_changes_monitoring')
        # Additional logic goes here.
        pass

    

    # --- Transition ---
    # mccr_ovv_reject_monitoring -> mccr_end
    def can_ovv_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_reject_monitoring
        return self.fsm_state == 'mccr_ovv_reject_monitoring'

    @transition(field= 'fsm_state', source = 'mccr_ovv_reject_monitoring', target = 'mccr_end', conditions=[can_ovv_end], on_error = 'failed', permission='')
    def ovv_end(self):
        print('The MCCR is transitioning from mccr_ovv_reject_monitoring to mccr_end')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_ovv_request_changes_monitoring -> mccr_updating_report_by_ovv_request
    def can_update_report_by_ovv_request(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_request_changes_monitoring
        return self.fsm_state == 'mccr_ovv_request_changes_monitoring'

    @transition(field= 'fsm_state', source = 'mccr_ovv_request_changes_monitoring', target = 'mccr_updating_report_by_ovv_request', conditions=[can_update_report_by_ovv_request], on_error = 'failed', permission='')
    def update_report_by_ovv_request(self):
        print('The MCCR is transitioning from mccr_ovv_request_changes_monitoring to mccr_updating_report_by_ovv_request')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_updating_report_by_ovv_request -> mccr_ovv_accept_assignation_monitoring
    def can_ovv_download_updated_report(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_updating_report_by_ovv_request
        return self.fsm_state == 'mccr_updating_report_by_ovv_request'

    @transition(field= 'fsm_state', source = 'mccr_updating_report_by_ovv_request', target = 'mccr_ovv_accept_assignation_monitoring',conditions=[can_ovv_download_updated_report], on_error = 'failed', permission='')
    def ovv_download_updated_report(self):
        print('The MCCR is transitioning from mccr_updating_report_by_ovv_request to mccr_ovv_accept_assignation_monitoring')
        # Additional logic goes here.
     

    # --- Transition ---
    # mccr_ovv_upload_evaluation -> mccr_ovv_accept_monitoring
    def can_ovv_accept_monitoring(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_upload_evaluation_monitoring
        return self.fsm_state == 'mccr_decision_step_ovv_evaluation_monitoring'

    @transition(field= 'fsm_state', source = 'mccr_decision_step_ovv_evaluation_monitoring', target = 'mccr_ovv_accept_monitoring', conditions=[can_ovv_accept_monitoring], on_error = 'failed', permission='')
    def ovv_accept_monitoring(self):
        print('The MCCR is transitioning from mccr_decision_step_ovv_evaluation_monitoring to mccr_ovv_accept_monitoring')
        # Additional logic goes here.
        pass
    ## evaluation report sinamecc by secretary 



     # --- Transition ---
    # mccr_ovv_accept_monitoring -> mccr_secretary_get_report_information
    def can_secretary_get_report_information(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ovv_accept_monitoring
        return self.fsm_state == 'mccr_ovv_accept_monitoring'

    @transition(field= 'fsm_state', source = 'mccr_ovv_accept_monitoring', target = 'mccr_secretary_get_report_information',conditions=[can_secretary_get_report_information], on_error = 'failed', permission='')
    def secretary_get_report_information(self):
        print('The MCCR is transitioning from mccr_ovv_accept_monitoring to mccr_secretary_get_report_information')
        # Additional logic goes here.
        





    # --- Transition ---
    # mccr_secretary_get_report_information -> mccr_on_report_evaluation_by_secretary
    def can_evaluate_report_by_secretary(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_secretary_get_report_information
        return self.fsm_state == 'mccr_secretary_get_report_information'

    @transition(field= 'fsm_state', source = 'mccr_secretary_get_report_information', target = 'mccr_on_report_evaluation_by_secretary',conditions=[can_evaluate_report_by_secretary], on_error = 'failed', permission='')
    def evaluate_report_by_secretary(self):
        print('The MCCR is transitioning from mccr_secretary_get_report_information to mccr_on_report_evaluation_by_secretary')
        # Additional logic goes here.
        pass



    # --- Transition ---
    # mccr_on_report_evaluation_by_secretary -> mccr_secretary_can_proceed_report
    def can_secretary_proceed_report(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_on_report_evaluation_by_secretary
        return self.fsm_state == 'mccr_on_report_evaluation_by_secretary'

    @transition(field= 'fsm_state', source = 'mccr_on_report_evaluation_by_secretary', target = 'mccr_secretary_can_proceed_report',conditions=[can_secretary_proceed_report], on_error = 'failed', permission='')
    def secretary_can_proceed_report(self):
        print('The MCCR is transitioning from mccr_on_report_evaluation_by_secretary to mccr_secretary_can_proceed_report')
        # Additional logic goes here.
        pass


    # --- Transition ---
    # mccr_secretary_can_proceed_report -> mccr_secretary_reject_report_environmental_concerns
    def can_secretary_reject_report_environmental_concerns(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_secretary_can_proceed_report
        return self.fsm_state == 'mccr_secretary_can_proceed_report'

    @transition(field= 'fsm_state', source = 'mccr_secretary_can_proceed_report', target = 'mccr_secretary_reject_report_environmental_concerns', conditions=[can_secretary_reject_report_environmental_concerns], on_error = 'failed', permission='')
    def secretary_reject_report_environmental_concerns(self):
        print('The MCCR is transitioning from mccr_secretary_can_proceed_report to mccr_secretary_reject_report_environmental_concerns')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_secretary_reject_report_environmental_concerns -> mccr_end
    def can_secretary_report_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_secretary_reject_report_environmental_concerns
        return self.fsm_state == 'mccr_secretary_reject_report_environmental_concerns'

    @transition(field= 'fsm_state', source = 'mccr_secretary_reject_report_environmental_concerns', target = 'mccr_end', conditions=[can_secretary_report_end], on_error = 'failed', permission='')
    def secretary_report_end(self):
        print('The MCCR is transitioning from mccr_secretary_reject_report_environmental_concerns to mccr_end')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_secretary_can_proceed_report -> mccr_refer_validation_monitoring_report
    def can_refer_validation_monitoring_report(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_secretary_can_proceed_report
        return self.fsm_state == 'mccr_secretary_can_proceed_report'

    @transition(field= 'fsm_state', source = 'mccr_secretary_can_proceed_report', target = 'mccr_refer_validation_monitoring_report', conditions=[can_refer_validation_monitoring_report], on_error = 'failed', permission='')
    def refer_validation_monitoring_report(self):
        print('The MCCR is transitioning from mccr_secretary_can_proceed_report to mccr_refer_validation_monitoring_report')
        # Additional logic goes here.
        #send notification to executive committee
        pass


    ## UCC decision

    # --- Transition ---
    # mccr_refer_validation_monitoring_report -> mccr_ucc_in_exec_committee_evaluation
    def can_ucc_in_exec_committee_evaluation(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_refer_validation_monitoring_report
        return self.fsm_state == 'mccr_refer_validation_monitoring_report'

    @transition(field= 'fsm_state', source = 'mccr_refer_validation_monitoring_report', target = 'mccr_ucc_in_exec_committee_evaluation', conditions=[can_ucc_in_exec_committee_evaluation], on_error = 'failed', permission='')
    def ucc_in_exec_committee_evaluation(self):
        print('The MCCR is transitioning from mccr_refer_validation_monitoring_report to mccr_ucc_in_exec_committee_evaluation')
        # Additional logic goes here.
        pass
    
    # --- Transition ---
    # mccr_ucc_in_exec_committee_evaluation -> mccr_decision_step_emit_ucc
    def can_decision_step_emit_ucc(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ucc_in_exec_committee_evaluation
        return self.fsm_state == 'mccr_ucc_in_exec_committee_evaluation'

    @transition(field= 'fsm_state', source = 'mccr_ucc_in_exec_committee_evaluation', target = 'mccr_decision_step_emit_ucc', conditions=[can_decision_step_emit_ucc], on_error = 'failed', permission='')
    def decision_step_emit_ucc(self):
        print('The MCCR is transitioning from mccr_ucc_in_exec_committee_evaluation to mccr_decision_step_emit_ucc')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # mccr_decision_step_emit_ucc -> mccr_ucc_reject
    def can_ucc_reject(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_decision_step_emit_ucc
        return self.fsm_state == 'mccr_decision_step_emit_ucc'

    @transition(field= 'fsm_state', source = 'mccr_decision_step_emit_ucc', target = 'mccr_ucc_reject', conditions=[can_ucc_reject], on_error = 'failed', permission='')
    def ucc_reject(self):
        print('The MCCR is transitioning from mccr_decision_step_emit_ucc to mccr_ucc_reject')
        # Additional logic goes here.
        # send notification to applicant organization
        pass


    # --- Transition ---
    # mccr_ucc_reject -> mccr_end
    def can_ucc_reject_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ucc_reject
        return self.fsm_state == 'mccr_ucc_reject'

    @transition(field= 'fsm_state', source = 'mccr_ucc_reject', target = 'mccr_end', conditions=[can_ucc_reject_end], on_error = 'failed', permission='')
    def ucc_reject_end(self):
        print('The MCCR is transitioning from mccr_ucc_reject to mccr_end')
        # Additional logic goes here.
        pass


    # --- Transition ---
    # mccr_decision_step_emit_ucc -> mccr_communicate_ucc_conditions 
    def can_communicate_ucc_conditions(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_decision_step_emit_ucc
        return self.fsm_state == 'mccr_decision_step_emit_ucc'

    @transition(field= 'fsm_state', source = 'mccr_decision_step_emit_ucc', target = 'mccr_communicate_ucc_conditions', conditions=[can_communicate_ucc_conditions], on_error = 'failed', permission='')
    def communicate_ucc_conditions(self):
        print('The MCCR is transitioning from mccr_decision_step_emit_ucc to mccr_communicate_ucc_conditions')
        # Additional logic goes here.
        # send notification with the conditions
        pass

    # --- Transition ---
    # mccr_decision_step_emit_ucc -> mccr_ucc_accept
    def can_ucc_accept(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_decision_step_emit_ucc
        return self.fsm_state == 'mccr_decision_step_emit_ucc'

    @transition(field= 'fsm_state', source = 'mccr_decision_step_emit_ucc', target = 'mccr_ucc_accept', conditions=[can_ucc_accept], on_error = 'failed', permission='')
    def ucc_accept(self):
        print('The MCCR is transitioning from mccr_decision_step_emit_ucc to mccr_ucc_accept')
        # Additional logic goes here.
        # send notification to emit ucc
        pass

    # --- Transition ---
    # mccr_ucc_accept -> mccr_end
    def can_ucc_accept_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - mccr_ucc_accept
        return self.fsm_state == 'mccr_ucc_accept'

    @transition(field= 'fsm_state', source = 'mccr_ucc_accept', target = 'mccr_end', conditions=[can_ucc_accept_end], on_error = 'failed', permission='')
    def ucc_accept_end(self):
        print('The MCCR is transitioning from mccr_ucc_accept to mccr_end')
        # Additional logic goes here.
        pass


    


    
class ChangeLog(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=False)
    # Foreign Keys
    mccr = models.ForeignKey(MCCRRegistry, related_name='change_log')
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