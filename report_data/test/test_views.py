import json
from rest_framework import status
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from report_data.models import ReportFile, ReportFileVersion
from report_data.serializers import ReportFileSerializer
from users.models import CustomUser

# initialize the APIClient app
client = Client()

class GetAllReportFilesTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        user = CustomUser.objects.get_or_create(username='admin')[0]
        client.force_login(user)
        self.report1 = ReportFile.objects.create(
            name='file1', user=user)
        ReportFileVersion.objects.create(user=user, version='1', active=True, file='/tmp/foofile', report_file=self.report1)

    def test_get_all_report_files(self):
        # get API response
        response = client.get(reverse('get_post_report_files'))
        # get data from db
        report_files = ReportFile.objects.all()
        serializer = ReportFileSerializer(report_files, many=True)
        self.assertTrue(len(report_files) > 0, "You should have at least 1 report file created")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_report_file(self):
        response = client.get(
            reverse('get_delete_update_report_file', kwargs={'pk': self.report1.pk}))
        report = ReportFile.objects.get(pk=self.report1.pk)
        serializer = ReportFileSerializer(report)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_report_file(self):
        response = client.get(
            reverse('get_delete_update_report_file', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewReportFileTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.get_or_create(username='admin')[0]
        client.force_login(user)
        self.invalid_payload = {
            'name': '',
            'file': '/foo/bar/reportX'
        }

    def test_create_invalid_report_file(self):
        response = client.post(
            reverse('get_post_report_files'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleReportFileTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.get_or_create(username='admin')[0]
        client.force_login(self.user )
        self.report1 = ReportFile.objects.create(
            name='file1', user=self.user)
        ReportFileVersion.objects.create(user=self.user, version='1', active=True, file='/tmp/foofile', report_file=self.report1)

        self.report2 = ReportFile.objects.create(
            name='file2', user=self.user)
        ReportFileVersion.objects.create(user=self.user, version='2', active=True, file='/tmp/foofile',
                                         report_file=self.report2)

        self.valid_payload = {
            'name': 'file1',
            'user': self.user.id,
        }
        self.invalid_payload = {
            'name': '',
            'file': '/foo/bar/reportX'
        }

    '''
    def test_valid_update_report_file(self):
        response = client.put(
            reverse('get_delete_update_report_file', kwargs={'pk': self.report1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    '''
    
    def test_invalid_update_report_file(self):
        response = client.put(
            reverse('get_delete_update_report_file', kwargs={'pk': self.report2.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleReportFileTest(TestCase):

    def setUp(self):
        user = CustomUser.objects.get_or_create(username='admin')[0]
        client.force_login(user)
        self.report1 = ReportFile.objects.create(
            name='file1', user=user)
        ReportFileVersion.objects.create(user=user, version='1', active=True, file='/tmp/foofile', report_file=self.report1)

    def test_valid_delete_report_file(self):
        response = client.delete(
            reverse('get_delete_update_report_file', kwargs={'pk': self.report1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_delete_report_file(self):
        response = client.delete(
            reverse('get_delete_update_report_file', kwargs={'pk': '0000112'}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

