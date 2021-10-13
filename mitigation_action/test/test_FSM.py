from django.test import TestCase, Client
from django.utils import timezone
from rest_framework import status
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth.models import Group
from mitigation_action.services import MitigationActionService
import json, uuid, datetime, boto3
from datetime import datetime
from workflow.models import Comment, ReviewStatus
from mitigation_action.models import MitigationAction
from moto import mock_ses
# initialize the APIClient app
client = Client()

class MitigationActionFSMTest(TestCase):

    def setUp(self):
        ...

    """missing test"""