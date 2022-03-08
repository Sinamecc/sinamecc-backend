import json
from rest_framework import status
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser

# initialize the APIClient app
client = Client()

class GetAllReportFilesTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
       ...
