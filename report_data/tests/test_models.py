from django.test import TestCase
from ..models import ReportFile


class ReportFileTest(TestCase):
    def setUp(self):
        ReportFile.objects.create(
            name='file1', file="/foo/bar/file1")


    def test_puppy_breed(self):
        file1 = ReportFile.objects.get(name='file1')
        self.assertEqual(
            file1.file_name, "/foo/bar/file1")
