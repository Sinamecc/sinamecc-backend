import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import ReportFile
from ..serializers import ReportFileSerializer


# initialize the APIClient app
client = Client()

class GetAllReportFilesTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        ReportFile.objects.create(
            name='file1', file_name="/foo/bar/file1")
        ReportFile.objects.create(
            name='file2', file_name="/foo/bar/file2")
        ReportFile.objects.create(
            name='file3', file_name="/foo/bar/file3")

    def test_get_all_report_files(self):
        # get API response
        response = client.get(reverse('get_post_report_files'))
        # get data from db
        report_files = ReportFile.objects.all()
        serializer = ReportFileSerializer(report_files, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleReportFileTest(TestCase):
    def setUp(self):
        self.report1 = ReportFile.objects.create(
            name='file1', file_name="/foo/bar/file1")
        self.report2 = ReportFile.objects.create(
            name='file2', file_name="/foo/bar/file2")
        self.report3 = ReportFile.objects.create(
            name='file3', file_name="/foo/bar/file3")

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

class CreateNeReportFileTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            'name': 'report1',
            'file_name': '/foo/bar/report1'
        }
        self.invalid_payload = {
            'name': '',
            'file_name': '/foo/bar/reportX'
        }

    def test_create_valid_report_file(self):
        response = client.post(
            reverse('get_post_report_files'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_puppy(self):
        response = client.post(
            reverse('get_post_report_files'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleReportFileTest(TestCase):

    def setUp(self):
        self.report1 = ReportFile.objects.create(
            name='file1', file_name="/foo/bar/file1")
        self.report2 = ReportFile.objects.create(
            name='file2', file_name="/foo/bar/file2")
        self.valid_payload = {
            'name': 'file1',
            'file_name': '/foo/bar/file1'
        }
        self.invalid_payload = {
            'name': '',
            'file_name': '/foo/bar/reportX'
        }

    def test_valid_update_report_file(self):
        response = client.put(
            reverse('get_delete_update_report_file', kwargs={'pk': self.report1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_report_file(self):
        response = client.put(
            reverse('get_delete_update_report_file', kwargs={'pk': self.report2.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleReportFileTest(TestCase):

    def setUp(self):
        self.report1 = ReportFile.objects.create(
            name='file1', file_name="/foo/bar/file1")

    def test_valid_delete_report_file(self):
        response = client.delete(
            reverse('get_delete_update_report_file', kwargs={'pk': self.report1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_report_file(self):
        response = client.delete(
            reverse('get_delete_update_report_file', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
