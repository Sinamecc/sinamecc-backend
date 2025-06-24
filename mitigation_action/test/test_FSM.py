import datetime
import json
import uuid
from datetime import datetime

import boto3
from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from moto import mock_ses
from rest_framework import status

from mitigation_action._services import MitigationActionService
from mitigation_action.models import MitigationAction
from users.models import CustomUser
from workflow.models import Comment, ReviewStatus

# initialize the APIClient app
client = Client()

class MitigationActionFSMTest(TestCase):

    def setUp(self):
        self.superUser = CustomUser.objects.get_or_create(username='test_super_user', email='izcar1@grupoincocr.com', is_superuser=True)[0]
        self.user = CustomUser.objects.get_or_create(username='admin')[0]
        self.group_list = Group.objects.filter(name__in=['dcc_mitigation_action_responsible', 'dcc_executive_secretary', 'mitigation_action_provider']).all()
        self.mitigation_service = MitigationActionService()
        self.AWS_REGION_SES = "us-east-1"
    
    # test flow from from to in_evaluation_by_DCC
    @mock_ses ## In this test sending notification by SES
    def test_new_to_in_evaluation_by_DCC(self):
        connection = boto3.client('ses', region_name=self.AWS_REGION_SES)

    """missing test"""
