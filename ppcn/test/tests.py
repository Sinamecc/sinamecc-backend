from django.test import TestCase, Client
from django.utils import timezone
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

import json
import uuid
import datetime
from datetime import datetime
from ppcn.models import Organization, Level, RequestPpcn
from ppcn.serializers import OrganizationSerializer, RequestPpcnSerializer, ContactSerializer
from mitigation_action.models import Contact
# initialize the APIClient app
client = Client()

class PPCNTest(TestCase):
    def setUp(self):
        user = User.objects.get_or_create(username='testuser')[0]
        client.force_login(user)
        self.level = Level.objects.create(level_es="Nacional", level_en="National")
        self.contact = Contact.objects.create(full_name='Marco', job_title='Manager', email='marco@mail.com', phone='88888888')
        self.organization = Organization.objects.create(name="CNP", representative_name="Andres", postal_code="112233", fax="22051000", adress="Calle 36, San José", level=self.level, contact=self.contact)
        TEST_FILE = os.path.join(os.path.dirname(__file__), 'data.html')
        self.request_ppcn = RequestPpcn.objects.create(organization=self.organization, TEST_FILE, created=timezone.now(), updated=timezone.now())

    def test_get_valid_organization(self):
        response = client.get(reverse('get_delete_update_organization'), kwargs={'id': self.organization.id})
        organization = Organization.objects.create(id=self.organization.id)
        serializer = OrganizationSerializer(organization)
        id = str(response.data.get('id'))
        idSerializer = str(serializer.data.get('id'))
        self.assertEqual(id, idSerializer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_organizations(self):
        response = client.get(reverse('get_post_organization'))
        organization = Organization.objects.all()
        serializer = OrganizationSerializer(organization, many=True)
        for serial in serializer.data:
            for resp in response.data:
                self.assertEqual(str(resp.get('name')), str(serial.get('name')))
                self.assertEqual(str(resp.get('representative_name')), str(serial.get('representative_name')))
                self.assertEqual(str(resp.get('postal_code')), str(serial.get('postal_code')))
                self.assertEqual(str(resp.get('fax')), str(serial.get('fax')))
                self.assertEqual(str(resp.get('address')), str(serial.get('address')))
                self.assertEqual(str(resp.get('ciiu')), str(serial.get('ciiu')))
                self.assertEqual(str(resp.get('level')), str(serial.get('level')))
                self.assertEqual(str(resp.get('contact')[id]), str(serial.get('contact')))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_request_ppcn(self):
        response = client.get(reverse('get_delete_update_request_ppcn'), kwargs={'id': self.request_ppcn.id})
        requestPpcn = Organization.objects.create(id=self.request_ppcn.id)
        serializer = RequestPpcnSerializer(requestPpcn)
        id = str(response.data.get('id'))
        idSerializer = str(serializer.data.get('id'))
        self.assertEqual(id, idSerializer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_recuest_ppcn(self):
        response = client.get(reverse('get_post_request_ppcn'), kwargs={'id': self.organization.id})
        request_ppcn = RequestPpcn.objects.all()
        serializer = OrganizationSerializer(request_ppcn, many=True)
        for serial in serializer.data:
            for resp in response.data:
                self.assertEqual(str(resp.get('organization')), str(serial.get('organization')))
                self.assertEqual(str(resp.get('file')), str(serial.get('file')))
                self.assertEqual(str(resp.get('created')), str(serial.get('created')))
                self.assertEqual(str(resp.get('updated')), str(serial.get('updated')))

        self.assertEqual(response.status_code, status.HTTP_200_OK)