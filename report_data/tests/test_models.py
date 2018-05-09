from django.test import TestCase, Client
from report_data.models import ReportFile
from django.contrib.auth.models import User

client = Client()

class ReportFileTest(TestCase):
    def setUp(self):
        self.user = User.objects.get_or_create(username='testuser')[0]
        client.force_login(self.user)
        ReportFile.objects.create(name='file1', user=self.user)


    def test_get_simple_report_file(self):
        file1 = ReportFile.objects.get(name='file1')
        self.assertEqual(file1.name, "file1")
        self.assertEqual(file1.user, self.user)
