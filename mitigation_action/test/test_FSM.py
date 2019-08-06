from django.test import TestCase, Client
from django.utils import timezone
from rest_framework import status
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth.models import Group
from mitigation_action.services import MitigationActionService
import json
import uuid
import datetime 
from datetime import datetime
from workflow.models import Comment, ReviewStatus
from mitigation_action.models import Mitigation
# initialize the APIClient app
client = Client()

class MitigationActionFSMTest(TestCase):

    def setUp(self):
        self.superUser = CustomUser.objects.get_or_create(username='test_super_user', email='izcar@grupoincocr.com', is_superuser=True)[0]
        self.user = CustomUser.objects.get_or_create(username='admin')[0]
        self.group_list = Group.objects.filter(name__in=['dcc_mitigation_action_responsible', 'dcc_executive_secretary', 'mitigation_action_provider']).all()

        self.mitigation_service = MitigationActionService()
    
    # test flow from from to in_evaluation_by_DCC
    def test_new_to_in_evaluation_by_DCC(self):
        flow = ['submitted','in_evaluation_by_DCC']
        
        client.force_login(self.superUser)
        self.model = Mitigation(user=self.superUser, name='name - test', strategy_name='name - strategy_name')
    
        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model, self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    
    # test wrong flow from from to in_evaluation_by_DCC
    def test_wrong_new_to_in_evaluation_by_DCC(self):
        target = 'in_evaluation_by_DCC'

        client.force_login(self.superUser)
        self.model = Mitigation(user=self.superUser)

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state.target)

    # test flow from in_evaluation_by_DCC to evaluation_by_DCC
    def test_evaluation_by_DCC_to_updating_by_request(self):   
        flow=['in_evaluation_by_DCC','decision_step_DCC','changes_requested_by_DCC','updating_by_request']

        client.force_login(self.superUser)
        self.model = Mitigation(user=self.superUser,fsm_state='submitted')
        
        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    # test wrong flow from in_evaluation_by_DCC to evaluation_by_DCC
    def test_wrong_evaluation_by_DCC_to_updating_by_request(self):
        points = [
            ['in_evaluation_by_DCC','updating_by_request'],
            ['in_evaluation_by_DCC','changes_requested_by_DCC'],
            ['decision_step_DCC','updating_by_request']
        ]

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='in_evaluation_by_DCC')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1],state)
            self.mitigation_service.update_fsm_state(point[0], self.model,self.superUser)
    
    # test flow from in_evaluation_by_DCC to submitted_INGEI_changes_proposal_evaluation
    def test_in_evaluation_by_DCC_to_submitted_INGEI_changes_proposal_evaluation(self):

        flow = ['in_evaluation_by_DCC','registering','in_evaluation_INGEI_by_DCC_IMN','submit_INGEI_harmonization_required'
        ,'INGEI_harmonization_required','updating_INGEI_changes_proposal','submitted_INGEI_changes_proposal_evaluation',
        'in_evaluation_INGEI_changes_proposal_by_DCC_IMN','submit_INGEI_changes_proposal_evaluation_result']
        
        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='submitted')

        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)


    # test wrong flow from in_evaluation_by_DCC to submitted_INGEI_changes_proposal_evaluation
    def test_wrong_in_evaluation_by_DCC_to_submitted_INGEI_changes_proposal_evaluation(self):
        points = [
            ['in_evaluation_by_DCC','submit_INGEI_changes_proposal_evaluation_result'],
            ['in_evaluation_by_DCC','in_evaluation_INGEI_by_DCC_IMN'],
            ['registering','submit_INGEI_harmonization_required'],
            ['in_evaluation_INGEI_by_DCC_IMN','INGEI_harmonization_required'],
            ['in_evaluation_INGEI_by_DCC_IMN','updating_INGEI_changes_proposal'],
            ['submit_INGEI_harmonization_required','updating_INGEI_changes_proposal'],
            ['submit_INGEI_harmonization_required','submitted_INGEI_changes_proposal_evaluation'],
            ['INGEI_harmonization_required','submitted_INGEI_changes_proposal_evaluation'],
            ['updating_INGEI_changes_proposal','in_evaluation_INGEI_changes_proposal_by_DCC_IMN'],
            ['updating_INGEI_changes_proposal','submit_INGEI_changes_proposal_evaluation_result'],
            ['submitted_INGEI_changes_proposal_evaluation','submit_INGEI_changes_proposal_evaluation_result']
        ]
        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='in_evaluation_by_DCC')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1],state)
            self.mitigation_service.update_fsm_state(point[0], self.model,self.superUser)

    # test flow from submit_INGEI_changes_proposal_evaluation_result to decision_step_DCC_proposal
    def test_submit_INGEI_changes_proposal_evaluation_result_to_decision_step_DCC_proposal(self):
        
        flow = ['submit_INGEI_changes_proposal_evaluation_result','INGEI_changes_proposal_rejected_by_DCC_IMN','submitted_SINAMECC_conceptual_proposal_integration'
        ,'in_evaluation_conceptual_proposal_by_DCC','decision_step_DCC_proposal']

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='in_evaluation_INGEI_changes_proposal_by_DCC_IMN')
        
        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    # test wrong flow from submit_INGEI_changes_proposal_evaluation_result to decision_step_DCC_proposal
    def test_wrong_submit_INGEI_changes_proposal_evaluation_result_to_decision_step_DCC_proposal(self):
        points = [
            ['submit_INGEI_changes_proposal_evaluation_result','decision_step_DCC_proposal'],
            ['submit_INGEI_changes_proposal_evaluation_result','submitted_SINAMECC_conceptual_proposal_integration'],
            ['INGEI_changes_proposal_rejected_by_DCC_IMN','in_evaluation_conceptual_proposal_by_DCC'],
            ['INGEI_changes_proposal_rejected_by_DCC_IMN','decision_step_DCC_proposal'],
            ['submitted_SINAMECC_conceptual_proposal_integration','decision_step_DCC_proposal']
        ]

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='submit_INGEI_changes_proposal_evaluation_result')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1],state)
            self.mitigation_service.update_fsm_state(point[0], self.model,self.superUser)

    # test flow from submit_INGEI_changes_proposal_evaluation_result to submitted_SINAMECC_conceptual_proposal_integration
    def test_submit_INGEI_changes_proposal_evaluation_result_to_submitted_SINAMECC_conceptual_proposal_integration(self):
        flow = ['submit_INGEI_changes_proposal_evaluation_result','INGEI_changes_proposal_accepted_by_DCC_IMN','implementing_INGEI_changes'
        ,'submitted_SINAMECC_conceptual_proposal_integration']

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='in_evaluation_INGEI_changes_proposal_by_DCC_IMN')

        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    # test wrong flow from submit_INGEI_changes_proposal_evaluation_result to submitted_SINAMECC_conceptual_proposal_integration
    def test_wrong_submit_INGEI_changes_proposal_evaluation_result_to_submitted_SINAMECC_conceptual_proposal_integration(self):
        points = [
            ['submit_INGEI_changes_proposal_evaluation_result','implementing_INGEI_changes'],
            ['submit_INGEI_changes_proposal_evaluation_result','submitted_SINAMECC_conceptual_proposal_integration'],
            ['INGEI_changes_proposal_accepted_by_DCC_IMN','submitted_SINAMECC_conceptual_proposal_integration'],
        ]

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='submit_INGEI_changes_proposal_evaluation_result')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1],state)
            self.mitigation_service.update_fsm_state(point[0], self.model,self.superUser)

    # test flow from submit_INGEI_changes_proposal_evaluation_result to in_evaluation_INGEI_changes_proposal_by_DCC_IMN
    def test_submit_INGEI_changes_proposal_evaluation_result_to_in_evaluation_INGEI_changes_proposal_by_DCC_IMN(self):
        flow = ['submit_INGEI_changes_proposal_evaluation_result','INGEI_changes_proposal_changes_requested_by_DCC_IMN','updating_INGEI_changes_proposal_by_request_of_DCC_IMN','in_evaluation_INGEI_changes_proposal_by_DCC_IMN']

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='in_evaluation_INGEI_changes_proposal_by_DCC_IMN')

        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    # test wrong flow from submit_INGEI_changes_proposal_evaluation_result to in_evaluation_INGEI_changes_proposal_by_DCC_IMN
    def test_wrong_submit_INGEI_changes_proposal_evaluation_result_to_in_evaluation_INGEI_changes_proposal_by_DCC_IMN(self):
        points = [
            ['submit_INGEI_changes_proposal_evaluation_result','updating_INGEI_changes_proposal_by_request_of_DCC_IMN'],
            ['submit_INGEI_changes_proposal_evaluation_result','in_evaluation_INGEI_changes_proposal_by_DCC_IMN'],
            ['INGEI_changes_proposal_changes_requested_by_DCC_IMN','in_evaluation_INGEI_changes_proposal_by_DCC_IMN']
        ]

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='submit_INGEI_changes_proposal_evaluation_result')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1],state)
            self.mitigation_service.update_fsm_state(point[0], self.model,self.superUser)


    # test flow from decision_step_DCC_proposal to submitted_SINAMECC_conceptual_proposal_integration
    def test_decision_step_DCC_proposal_to_submitted_SINAMECC_conceptual_proposal_integration(self):
        flow = ['decision_step_DCC_proposal','changes_requested_to_conceptual_proposal',
        'submitted_conceptual_proposal_changes','submitted_SINAMECC_conceptual_proposal_integration']

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='in_evaluation_conceptual_proposal_by_DCC')

        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    # test wrong flow from decision_step_DCC_proposal to submitted_SINAMECC_conceptual_proposal_integration
    def test_wrong_decision_step_DCC_proposal_to_submitted_SINAMECC_conceptual_proposal_integration(self):
        points = [
            ['decision_step_DCC_proposal','submitted_SINAMECC_conceptual_proposal_integration'],
            ['decision_step_DCC_proposal','submitted_conceptual_proposal_changes'],
            ['changes_requested_to_conceptual_proposal','submitted_SINAMECC_conceptual_proposal_integration']
        ]

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='in_evaluation_conceptual_proposal_by_DCC')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1],state)
            self.mitigation_service.update_fsm_state(point[0], self.model,self.superUser)

    # test flow from decision_step_DCC_proposal to decision_step_SINAMEC
    def test_decision_step_DCC_proposal_to_decision_step_SINAMEC(self):
        flow = ['decision_step_DCC_proposal','conceptual_proposal_approved','planning_integration_with_SINAMECC','decision_step_SINAMEC']

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='in_evaluation_conceptual_proposal_by_DCC')

        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

    # test wrong flow from decision_step_DCC_proposal to decision_step_SINAMEC
    def test_wrong_decision_step_DCC_proposal_to_decision_step_SINAMEC(self):
        points = [
            ['decision_step_DCC_proposal','decision_step_SINAMEC'],
            ['decision_step_DCC_proposal','planning_integration_with_SINAMECC'],
            ['conceptual_proposal_approved','decision_step_SINAMEC']
        ]

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='decision_step_DCC_proposal')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1],state)
            self.mitigation_service.update_fsm_state(point[0], self.model,self.superUser)

    # test flow from decision_step_SINAMEC to planning_integration_with_SINAMECC
    def test_decision_step_SINAMEC_to_planning_integration_with_SINAMECC(self):
        flow = ['decision_step_SINAMEC','SINAMECC_integration_changes_requested','submitted_SINAMECC_integration_changes','planning_integration_with_SINAMECC']
        
        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='planning_integration_with_SINAMECC')

        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)


    # test wrong flow from decision_step_SINAMEC to planning_integration_with_SINAMECC
    def test_wrong_decision_step_SINAMEC_to_planning_integration_with_SINAMECC(self):
        points = [
            ['decision_step_SINAMEC','planning_integration_with_SINAMECC'],
            ['decision_step_SINAMEC','submitted_SINAMECC_integration_changes'],
            ['SINAMECC_integration_changes_requested','planning_integration_with_SINAMECC']
        ]

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='decision_step_SINAMEC')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1],state)
            self.mitigation_service.update_fsm_state(point[0], self.model,self.superUser)

    # test flow from decision_step_SINAMEC to end
    def test_decision_step_SINAMEC_to_end(self):
        flow = ['decision_step_SINAMEC','SINAMECC_integration_approved','implementing_SINAMECC_changes','end']

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='planning_integration_with_SINAMECC')

        for state in flow:
            self.mitigation_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)


    def test_wrong_decision_step_SINAMEC_to_end(self):
        points = [
            ['decision_step_SINAMEC','end'],
            ['decision_step_SINAMEC','implementing_SINAMECC_changes'],
            ['SINAMECC_integration_approved','end']
        ]

        client.force_login(self.superUser)

        self.model = Mitigation(user=self.superUser,fsm_state='decision_step_SINAMEC')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1],state)
            self.mitigation_service.update_fsm_state(point[0], self.model,self.superUser)
        