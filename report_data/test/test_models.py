from django.test import TestCase, Client
from report_data.models import ReportFile
from users.models import CustomUser

client = Client()

class ReportFileTest(TestCase):
    def setUp(self):
        ...