from django.test import TestCase, Client
from django.utils import timezone
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
import datetime
from datetime import datetime
from ppcn.models import *
from ppcn.serializers import *
from mitigation_action.models import Contact
from io import BytesIO
from general.services import EmailServices
from ppcn.email_services import PPCNEmailServices

from users.models import CustomUser
from ppcn.services import PpcnService

import json

import os
# initialize the APIClient app
client = Client()
User = get_user_model()
ses_service = EmailServices()

class PPCNFSMTest(TestCase):
    def setUp(self):

        self.geographic_level_organizational = GeographicLevel.objects.get(level_es="Organizacional")
        self.superUser = CustomUser.objects.get_or_create(username='admin')[0]
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]
        self.group_list = Group.objects.filter(name__in=['dcc_ppcn_responsible', 'dcc_executive_secretary', 'ppcn_responsible', 'ppcn_provider']).all()
        
        self.ppcn_service = PpcnService()

    #test flow from PPCN_new to PPCN_decision_step_DCC:
    ## TODO: Fix Workflows PPC
    '''def test_PPCN_new_to_PPCN_decision_step_DCC(self):

        flow = ['PPCN_submitted','PPCN_evaluation_by_DCC','PPCN_decision_step_DCC']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser)

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model, self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        
        self.superUser.groups.clear()
    '''

    #test wrong flow from PPCN_new to PPCN_decision_step_DCC:
    ## TODO:  Fix Workflows PPC
    '''def test_wrong_PPCN_new_to_PPCN_decision_step_DCC(self):

        points = [
            ['PPCN_new','PPCN_decision_step_DCC'],
            ['PPCN_new','PPCN_evaluation_by_DCC'],
            ['PPCN_submitted','PPCN_decision_step_DCC']
        ]
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser)

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1], state.target)
            self.ppcn_service.update_fsm_state(point[0], self.model, self.superUser)
        
        self.superUser.groups.clear()
    '''

     # test flow from PPCN_decision_step_DCC to PPCN_evaluation_by_DCC :
    def test_PPCN_decision_step_DCC_to_PPCN_evaluation_by_DCC(self):
        flow = ['PPCN_decision_step_DCC','PPCN_changes_requested_by_DCC','PPCN_updating_by_request_DCC','PPCN_evaluation_by_DCC']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_DCC')

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model, self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

    # test wrong flow from PPCN_decision_step_DCC to PPCN_evaluation_by_DCC :
    def test_wrong_PPCN_decision_step_DCC_to_PPCN_evaluation_by_DCC(self):
        points = [
            ['PPCN_decision_step_DCC','PPCN_evaluation_by_DCC'],
            ['PPCN_decision_step_DCC','PPCN_updating_by_request_DCC'],
            ['PPCN_changes_requested_by_DCC','PPCN_evaluation_by_DCC']
        ]
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_DCC')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
               
                 self.assertNotEquals(point[1],state.target)
            self.ppcn_service.update_fsm_state(point[0], self.model, self.superUser)

        self.superUser.groups.clear()

     # Test flow from PPCN_decision_step_DCC to PPCN_decision_step_CA
    def test_PPCN_decision_step_DCC_to_PPCN_decision_step_CA(self):
        flow = ['PPCN_decision_step_DCC','PPCN_accepted_request_by_DCC','PPCN_evaluation_by_CA','PPCN_decision_step_CA']
        for group in self.group_list: 
            self.superUser.groups.add(group)
        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_DCC')
        self.model.geographic_level = self.geographic_level_organizational
        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model, self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

    ## We need to fix this test
    # Test wrong flow from PPCN_decision_step_DCC to PPCN_decision_step_CA
    # def test_wrong_PPCN_decision_step_DCC_to_PPCN_decision_step_CA(self):
    #     points = [
    #         ['PPCN_decision_step_DCC','PPCN_decision_step_CA'],
    #         ['PPCN_decision_step_DCC','PPCN_evaluation_by_CA'],
    #         ['PPCN_accepted_request_by_DCC','PPCN_decision_step_CA']
    #     ]

    #     for group in self.group_list: 
    #         self.superUser.groups.add(group)

    #     client.force_login(self.superUser)
    #     self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_DCC', geographic_level=self.geographic_level_c

    #     for point in points:
    #         transitions = list(self.model.get_available_fsm_state_transitions())
    #         for state in transitions:
    #              self.assertNotEquals(point[1],state.target)
    #         self.ppcn_service.update_fsm_state(point[0], self.model, self.superUser)
            
    #     self.superUser.groups.clear()

    # test flow from PPCN_decision_step_CA to PPCN_end:
    def test_PPCN_decision_step_CA_to_PPCN_end(self):
        flow = ['PPCN_decision_step_CA','PPCN_rejected_request_by_CA','PPCN_end']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_CA')

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

    # test wrong flow from PPCN_decision_step_CA to PPCN_end:
    def test_wrong_PPCN_decision_step_CA_to_PPCN_end(self):
        target = 'PPCN_end'

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_CA')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state.target)


    #test flow from PPCN_decision_step_CA to PPCN_send_recognition_certificate:
    def test_PPCN_decision_step_CA_to_PPCN_send_recognition_certificate(self):
        flow = ['PPCN_decision_step_CA','PPCN_accepted_request_by_CA','PPCN_send_recognition_certificate']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_CA')

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

    #test wrong flow from PPCN_decision_step_CA to PPCN_send_recognition_certificate:
    def test_wrong_PPCN_decision_step_CA_to_PPCN_send_recognition_certificate(self):
        target = 'PPCN_send_recognition_certificate'

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_CA')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state.target)

    #test flow from PPCN_decision_step_DCC to PPCN_end:
    def test_PPCN_decision_step_DCC_to_PPCN_end(self):
        flow = ['PPCN_decision_step_DCC','PPCN_rejected_request_by_DCC','PPCN_end']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_DCC')

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

     #test wrong flow from PPCN_decision_step_DCC to PPCN_end:
    def test_wrong_PPCN_decision_step_DCC_to_PPCN_end(self):
        target = 'PPCN_end'

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_DCC')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state.target)
