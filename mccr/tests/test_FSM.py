from django.test import TestCase, Client
from mccr.models import *

from users.models import CustomUser
from mccr.services import MCCRService
from mccr.models import MCCRRegistry,MCCRRegistryOVVRelation,OVV,MCCRUserType

from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from mccr.email_services import MCCREmailServices

from django.contrib.auth.models import Group

ses_service = EmailServices()

# initialize the APIClient app
client = Client()
class MCCRFSMTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]
        self.mccr_service = MCCRService()
        self.user_type=MCCRUserType.objects.create(name='Registrator')
        self.mitigation = Mitigation.objects.create(
            user = self.user,
        )
        self.superUser = CustomUser.objects.get_or_create(username='admin', is_superuser=True)[0]
        self.group_list = Group.objects.filter(name__in=['executive_committee_mccr', 'validating_organizations_mccr', 'mccr_responsible','dcc_mccr_responsible','mccr_provider']).all()

        client.force_login(self.superUser)

    #test flow from new to mccr_ovv_assigned_first_review:
    def test_new_to_mccr_ovv_accept_reject(self):
        flow = ['mccr_submitted','mccr_ovv_assigned_first_review']
        

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='new')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    def test_wrong_way_new_to_mccr_ovv_assigned_first_review(self):

        target = 'mccr_ovv_assigned_first_review'

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id)
        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state)


    def test_mccr_ovv_assigned_first_review_to_mccr_ovv_assigned_notification(self):

         flow = ['mccr_ovv_assigned_first_review','mccr_ovv_assigned_notification']
         
         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_ovv_assigned_first_review')

         ovv = OVV.objects.create(name='test',email='test@test.com',phone='12345678')
         ovv_relation=MCCRRegistryOVVRelation.objects.create(mccr=self.model,ovv=ovv)

         for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)


    def test_mccr_ovv_accept_reject_to_mccr_ovv_assigned_first_review(self):
         flow = ['mccr_ovv_accept_reject','mccr_ovv_reject_assignation','mccr_ovv_assigned_first_review']
         
         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_ovv_accept_reject')
         
         for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    
    def test_wrong_mccr_ovv_accept_reject_to_mccr_ovv_assigned_first_review(self):
        target = 'mccr_ovv_assigned_first_review'

        
        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_ovv_accept_reject')
        
        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state)
        
        self.superUser.groups.clear()
            

    def test_mccr_ovv_accept_assignation_to_mccr_ovv_upload_evaluation(self):
         flow = ['mccr_ovv_accept_assignation','mccr_ovv_upload_evaluation']

         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_ovv_accept_assignation')

         for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)


    def test_mccr_ovv_upload_evaluation_to_mccr_ovv_accept_assignation(self):
         flow = ['mccr_ovv_upload_evaluation','mccr_ovv_request_changes_dp','mccr_updating_dp_by_ovv_request','mccr_ovv_accept_assignation']

         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_ovv_upload_evaluation')

         for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)


    def test_wrong_mccr_ovv_upload_evaluation_to_mccr_ovv_accept_assignation(self):
         points = ['mccr_ovv_upload_evaluation','mccr_ovv_request_changes_dp']
         target =  'mccr_ovv_accept_assignation'

         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_ovv_upload_evaluation')

         
         for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                 self.assertNotEquals(target,state)
            self.mccr_service.update_fsm_state(point, self.model,self.superUser)


    def test_mccr_ovv_upload_evaluation_to_mccr_end(self):
         flow = ['mccr_ovv_upload_evaluation','mccr_ovv_reject_dp','mccr_end']

         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_ovv_upload_evaluation')

         for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    def test_wrong_mccr_ovv_upload_evaluation_to_mccr_end(self):
        target = 'mccr_end'

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_ovv_upload_evaluation')
        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state)

    def test_mccr_ovv_upload_evaluation_to_mccr_ovv_accept_dp(self):
        flow = ['mccr_ovv_upload_evaluation','mccr_ovv_accept_dp']

        
        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_ovv_upload_evaluation')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    def test_mccr_on_dp_evaluation_by_secretary_to_mccr_secretary_can_proceed_dp(self):
        flow = ['mccr_on_dp_evaluation_by_secretary','mccr_secretary_can_proceed_dp']

        
        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_on_dp_evaluation_by_secretary')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    def test_mccr_secretary_can_proceed_dp_to_mccr_secretary_reject_dp_environmental_concerns(self):
        flow = ['mccr_secretary_can_proceed_dp','mccr_secretary_reject_dp_environmental_concerns']

        
        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_on_dp_evaluation_by_secretary')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    def test_mccr_secretary_can_proceed_dp_to_mccr_in_exec_committee_evaluation(self):
        flow = ['mccr_secretary_can_proceed_dp','mccr_refer_validation_dp_report','mccr_in_exec_committee_evaluation']

        
        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_on_dp_evaluation_by_secretary')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)
        

    def test_wrong_mccr_secretary_can_proceed_dp_to_mccr_in_exec_committee_evaluation(self):

        target = 'mccr_in_exec_committee_evaluation'

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_on_dp_evaluation_by_secretary')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state)


    def test_mccr_in_exec_committee_evaluation_to_mccr_exec_committee_reject(self):
        flow = ['mccr_in_exec_committee_evaluation','mccr_exec_committee_reject']
        
        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_in_exec_committee_evaluation')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    def test_mccr_in_exec_committee_evaluation_to_mccr_communicate_conditions(self):
    
        flow = ['mccr_in_exec_committee_evaluation','mccr_communicate_conditions']

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_in_exec_committee_evaluation')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    
    def test_mccr_in_exec_committee_evaluation_to_mccr_decision_step_ovv_evaluation_monitoring(self):
        flow = ['mccr_in_exec_committee_evaluation','mccr_project_monitoring','mccr_upload_report_sinamecc','mccr_ovv_assigned'
        ,'mccr_ovv_accept_reject_monitoring','mccr_ovv_accept_assignation_monitoring','mccr_ovv_upload_evaluation_monitoring'
        ,'mccr_decision_step_ovv_evaluation_monitoring']

        
        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_in_exec_committee_evaluation')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    def test_wrong_mccr_in_exec_committee_evaluation_to_mccr_decision_step_ovv_evaluation_monitoring(self):
         points = [
         ['mccr_in_exec_committee_evaluation','mccr_decision_step_ovv_evaluation_monitoring'],
         ['mccr_project_monitoring','mccr_ovv_accept_reject_monitoring'],
         ['mccr_upload_report_sinamecc','mccr_ovv_accept_reject_monitoring'],
         ['mccr_ovv_assigned','mccr_ovv_upload_evaluation_monitoring'],
         ['mccr_ovv_accept_reject_monitoring','mccr_decision_step_ovv_evaluation_monitoring'],
         ['mccr_ovv_accept_assignation_monitoring','mccr_decision_step_ovv_evaluation_monitoring']]


         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_in_exec_committee_evaluation')

         
         for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                 self.assertNotEquals(point[1],state)
            self.mccr_service.update_fsm_state(point[0], self.model,self.superUser)


    def test_mccr_decision_step_ovv_evaluation_monitoring_to_mccr_updating_report_by_ovv_request(self):
        flow = ['mccr_decision_step_ovv_evaluation_monitoring','mccr_ovv_request_changes_monitoring','mccr_updating_report_by_ovv_request']

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_decision_step_ovv_evaluation_monitoring')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)


    def test_wrong_mccr_decision_step_ovv_evaluation_monitoring_to_mccr_updating_report_by_ovv_request(self):

        target = 'mccr_updating_report_by_ovv_request'

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_decision_step_ovv_evaluation_monitoring')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state)


    def test_mccr_secretary_get_report_information_to_mccr_secretary_can_proceed_report(self):

        flow = ['mccr_secretary_get_report_information','mccr_on_report_evaluation_by_secretary','mccr_secretary_can_proceed_report']

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_secretary_get_report_information')

        for state in flow:
            self.mccr_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    def test_wrong_secretary_get_report_information_to_mccr_secretary_can_proceed_report(self):

        target = 'mccr_secretary_can_proceed_report'

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_secretary_get_report_information')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state)


    def test_mccr_secretary_can_proceed_report_to_mccr_decision_step_emit_ucc(self):

         flow = ['mccr_secretary_can_proceed_report','mccr_refer_validation_monitoring_report','mccr_ucc_in_exec_committee_evaluation','mccr_decision_step_emit_ucc']

         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_secretary_can_proceed_report')

         for state in flow:
             self.mccr_service.update_fsm_state(state, self.model,self.superUser)
             self.assertEqual(self.model.fsm_state, state)

    def test_wrong_mccr_secretary_can_proceed_report_to_mccr_decision_step_emit_ucc(self):

        target = 'mccr_ucc_in_exec_committee_evaluation'

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_secretary_can_proceed_report')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state)

    def test_mccr_decision_step_emit_ucc_to_mccr_end(self):
         flow = ['mccr_decision_step_emit_ucc','mccr_ucc_reject','mccr_end']

         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_decision_step_emit_ucc')

         for state in flow:
             self.mccr_service.update_fsm_state(state, self.model,self.superUser)
             self.assertEqual(self.model.fsm_state, state)

    def test_wrong_mccr_decision_step_emit_ucc_to_mccr_end(self):

        target = 'mccr_end'

        self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
        fsm_state='mccr_decision_step_emit_ucc')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state)
        

    def test_mccr_decision_step_emit_ucc_to_mccr_end_by_mccr_ucc_accept(self):

         flow = ['mccr_decision_step_emit_ucc','mccr_ucc_accept','mccr_end']

         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_decision_step_emit_ucc')

         for state in flow:
             self.mccr_service.update_fsm_state(state, self.model,self.superUser)
             self.assertEqual(self.model.fsm_state, state)

    def test_mccr_decision_step_emit_ucc_to_mccr_communicate_ucc_conditions(self):

         flow = ['mccr_decision_step_emit_ucc','mccr_communicate_ucc_conditions']

         self.model = MCCRRegistry(user=self.superUser,mitigation_id=self.mitigation.pk,user_type_id=self.user_type.id,
         fsm_state='mccr_decision_step_emit_ucc')

         for state in flow:
             self.mccr_service.update_fsm_state(state, self.model,self.superUser)
             self.assertEqual(self.model.fsm_state, state)


