from datetime import datetime
from typing import ClassVar

from django.contrib.auth.models import Group
from django.db.models import fields
from django.test import Client, TestCase
from django.utils import timezone

from mitigation_action._services import MitigationActionService
from mitigation_action.models import *
from mitigation_action.serializers import *
from users.models import CustomUser

# initialize the APIClient app
client = Client()


class MitigationActionModelTest(TestCase):

    def setUp(self):

       ...
    
