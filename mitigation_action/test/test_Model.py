from django.test import TestCase, Client
from django.utils import timezone
from users.models import CustomUser
from django.contrib.auth.models import Group
from mitigation_action.services import MitigationActionService

from datetime import datetime
from mitigation_action.models import *
from mitigation_action.serializers import *

# initialize the APIClient app
client = Client()


class MitigationActionModelTest(TestCase):

    def setUp(self):

        pass
      