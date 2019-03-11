from django.test import TestCase, Client
from django.utils import timezone
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
import datetime
from datetime import datetime
from ppcn.models import *
from ppcn.serializers import *
from mitigation_action.models import Contact
from io import BytesIO
from general.services import EmailServices
from ppcn.email_services import PPCNEmailServices

from users.models import CustomUser
from ppcn.services import PpcnService

import json

import os
# initialize the APIClient app
client = Client()
User = get_user_model()
ses_service = EmailServices()
class PPCNTest(TestCase):

    def setUp(self):
        user = User.objects.get_or_create(username='testuser')[0]
        User.objects.get_or_create(username='dcc_user')
        client.force_login(user)
        self.geographic_level = GeographicLevel.objects.create(level_es = "Nacional" , level_en = "National")
        self.required_level = RequiredLevel.objects.create(level_type_es = "Solicitud inicial", level_type_en = "Initial Request")
        self.recognition_type = RecognitionType.objects.create(recognition_type_es = "Carbono Inventario", recognition_type_en = "Carbon Inventary")
        self.contact = Contact.objects.create(full_name='Marco', job_title = 'Manager', email='marco@mail.com', phone ='88888888')
        self.organization = Organization.objects.create(name="CNP", representative_name="Andres",phone_organization = "77777777", postal_code="112233", fax="22051000", address="Calle 36, San José", contact = self.contact, ciiu = "1234")
        self.sector = Sector.objects.create(name_es = "Energía", name_en = "Energy", geographicLevel = self.geographic_level)
        self.sub_sector = SubSector.objects.create(name_es = "Distribución de energía", name_en = "Energy Distribution", sector = self.sector)
        self.ppcn = PPCN.objects.create(
            user = user,
            organization = self.organization,
            geographic_level = self.geographic_level,
            required_level = self.required_level,
            recognition_type = self.recognition_type,
            review_count = 0,
            fsm_state = "sumitted",
            created = timezone.now(),
            updated = timezone.now()
        )
        self.ppcn.comments.create(comment = 'Test comment')
        self.change_log = ChangeLog.objects.create(ppcn = self.ppcn, previous_status = "new", current_status = "sumitted", user = user)
        self.file = os.path.join(os.path.dirname(__file__), '@get_token')
        self.ppcn_file = PPCNFile.objects.create( user = user, file = self.file, ppcn_form= self.ppcn)

        self.ppcn_data = {
            "user": self.ppcn.user.id,
            "organization":
                {
                    "name": self.ppcn.organization.name,
                    "representative_name": self.ppcn.organization.representative_name,
                    "phone_organization": self.ppcn.organization.phone_organization,
                    "postal_code": self.ppcn.organization.postal_code,
                    "fax": self.ppcn.organization.fax,
                    "ciiu": self.ppcn.organization.ciiu,
                    "address": self.ppcn.organization.address,
                    "contact": {
                        "full_name": self.ppcn.organization.contact.full_name,
                        "job_title": self.ppcn.organization.contact.job_title,
                        "email": self.ppcn.organization.contact.email,
                        "phone": self.ppcn.organization.contact.phone
                    }
                },
            "geographicLevel": self.ppcn.geographic_level.id,
            "requiredLevel": self.ppcn.required_level.id,
            "subsector": self.sub_sector.id,
            "sector": self.sector.id,
            "base_year": "2018-04-03",
            "recognitionType": self.ppcn.recognition_type.id
        }

        self.emailServicesInstance = EmailServices("sinamec@grupoincocr.com")
        self.recipient_list = ["sinamec@grupoincocr.com","izcar@grupoincocr.com"]
        self.subject = "UNIT-TEST, AWS - SES"
        self.message_body = "Test, send to notification"

    def test_get_valid_all_ppcn(self):
        response = client.get(reverse('get_post_ppcn'), kwargs={'language':'en'})
        serializer = PPCNSerializer(PPCN.objects.all(), many=True)
        for serial in serializer.data:
            for resp in response.data:
                org = OrganizationSerializer(Organization.objects.get(id=serial.get('organization'))).data
                self.assertEqual(str(resp.get('organization')['id']), str(org.get('id')))
                self.assertEqual(str(resp.get('organization')['name']), str(org.get('name')))
                self.assertEqual(str(resp.get('organization')['representative_name']), str(org.get('representative_name')))
                self.assertEqual(str(resp.get('organization')['phone_organization']), str(org.get('phone_organization')))
                self.assertEqual(str(resp.get('organization')['postal_code']), str(org.get('postal_code')))
                self.assertEqual(str(resp.get('organization')['fax']), str(org.get('fax')))
                self.assertEqual(str(resp.get('organization')['address']), str(org.get('address')))
                self.assertEqual(str(resp.get('organization')['ciiu']), str(org.get('ciiu')))

                contact = ContactSerializer(Contact.objects.get(id=org.get('contact'))).data
                self.assertEqual(str(resp.get('organization')['contact']['id']), str(contact.get('id')))
                self.assertEqual(str(resp.get('organization')['contact']['full_name']), str(contact.get('full_name')))
                self.assertEqual(str(resp.get('organization')['contact']['job_title']), str(contact.get('job_title')))
                self.assertEqual(str(resp.get('organization')['contact']['email']), str(contact.get('email')))
                self.assertEqual(str(resp.get('organization')['contact']['phone']), str(contact.get('phone')))

                self.assertEqual(str(resp.get('geographic_level')['id']), str(serial.get('geographic_level')))
                self.assertEqual(str(resp.get('required_level')['id']), str(serial.get('required_level')))

                self.assertEqual(str(resp.get('recognition_type')['id']), str(serial.get('recognition_type')))
                self.assertEqual(str(resp.get('base_year')), str(serial.get('base_year')))
                self.assertEqual(str(resp.get('fsm_state')), str(serial.get('fsm_state')))

                datetime_create_response = datetime.strptime(str(resp.get('created')), '%Y-%m-%d %H:%M:%S.%f+00:00')
                datetime_create_serializer = datetime.strptime(str(serial.get('created')), '%Y-%m-%dT%H:%M:%S.%fZ')
                self.assertEqual(datetime_create_response, datetime_create_serializer)

                datetime_updated_response = datetime.strptime(str(resp.get('updated')), '%Y-%m-%d %H:%M:%S.%f+00:00')
                datetime_updated_serializer = datetime.strptime(str(serial.get('updated')), '%Y-%m-%dT%H:%M:%S.%fZ')
                self.assertEqual(datetime_updated_response, datetime_updated_serializer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response

    def test_get_valid_request_ppcn(self):
        response = client.get(reverse('get_one_ppcn', args=[self.ppcn.id, 'en']))
        serial = PPCNSerializer(PPCN.objects.get(id=self.ppcn.id)).data

        org = OrganizationSerializer(Organization.objects.get(id=serial.get('organization'))).data
        self.assertEqual(str(response.data.get('organization')['id']), str(org.get('id')))
        self.assertEqual(str(response.data.get('organization')['name']), str(org.get('name')))
        self.assertEqual(str(response.data.get('organization')['representative_name']), str(org.get('representative_name')))
        self.assertEqual(str(response.data.get('organization')['phone_organization']), str(org.get('phone_organization')))
        self.assertEqual(str(response.data.get('organization')['postal_code']), str(org.get('postal_code')))
        self.assertEqual(str(response.data.get('organization')['fax']), str(org.get('fax')))
        self.assertEqual(str(response.data.get('organization')['address']), str(org.get('address')))
        self.assertEqual(str(response.data.get('organization')['ciiu']), str(org.get('ciiu')))

        contact = ContactSerializer(Contact.objects.get(id=org.get('contact'))).data
        self.assertEqual(str(response.data.get('organization')['contact']['full_name']), str(contact.get('full_name')))
        self.assertEqual(str(response.data.get('organization')['contact']['job_title']), str(contact.get('job_title')))
        self.assertEqual(str(response.data.get('organization')['contact']['email']), str(contact.get('email')))
        self.assertEqual(str(response.data.get('organization')['contact']['phone']), str(contact.get('phone')))

        self.assertEqual(str(response.data.get('geographic_level')['id']), str(serial.get('geographic_level')))
        self.assertEqual(str(response.data.get('geographic_level')['id']), str(serial.get('geographic_level')))
        self.assertEqual(str(response.data.get('recognition_type')['id']), str(serial.get('recognition_type')))
        self.assertEqual(str(response.data.get('base_year')), str(serial.get('base_year')))
        self.assertEqual(str(response.data.get('fsm_state')), str(serial.get('fsm_state')))

        datetime_create_response = datetime.strptime(str(response.data.get('created')), '%Y-%m-%d %H:%M:%S.%f+00:00')
        datetime_create_serializer = datetime.strptime(str(serial.get('created')), '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEqual(datetime_create_response, datetime_create_serializer)

        datetime_updated_response = datetime.strptime(str(response.data.get('updated')), '%Y-%m-%d %H:%M:%S.%f+00:00')
        datetime_updated_serializer = datetime.strptime(str(serial.get('updated')), '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEqual(datetime_updated_response, datetime_updated_serializer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response

    def test_get_post_ppcn(self):
        response = client.post(
            reverse('get_post_ppcn', kwargs={'language': 'en'}),
            data=json.dumps(self.ppcn_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED )
        assert response

    def get_delete_put_patch_ppcn(self):
        response = client.delete(reverse('put_delete_patch_ppcn', kwargs={'id': self.ppcn.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response

    def test_send_notification_to_multiple_contacts(self):
        recipient_list = self.recipient_list
        subject = self.subject
        message_body = self.message_body
        emailServices = self.emailServicesInstance
        response = emailServices.send_notification(recipient_list, subject, message_body)
        self.assertEqual(response[0], True)
        assert response

    def test_send_notification_to_a_contact(self):
        recipient_list = self.recipient_list[:1]
        subject = self.subject
        message_body = self.message_body
        emailServices = self.emailServicesInstance
        response = emailServices.send_notification(recipient_list, subject, message_body)
        self.assertEqual(response[0], True)
        assert response

    def test_send_notification_contact_empty(self):
        recipient_list = []
        subject = self.subject
        message_body = self.message_body
        emailServices = self.emailServicesInstance
        response = emailServices.send_notification(recipient_list, subject, message_body)
        self.assertEqual(response[0], False)
        assert response

    def test_send_notification_to_dcc_user(self):
        ppcn_services = PPCNEmailServices(ses_service)
        response = ppcn_services.sendStatusNotification(self.ppcn, 'dcc_user')
        self.assertEqual(response[0], False)
        assert response


class PPCNFSMTest(TestCase):
    def setUp(self):

        self.superUser = CustomUser.objects.get_or_create(username='test_super_user')[0]
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]
        self.group_list = Group.objects.filter(name__in=['dcc_ppcn_responsible', 'dcc_executive_secretary', 'ppcn_responsible']).all()
        
        self.ppcn_service = PpcnService()

    #test flow from PPCN_new to PPCN_decision_step_DCC:
    def test_PPCN_new_to_PPCN_decision_step_DCC(self):

        flow = ['PPCN_submitted','PPCN_evaluation_by_DCC','PPCN_decision_step_DCC']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser)

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model, self.superUser)
            self.assertEqual(self.model.fsm_state, state)
        
        self.superUser.groups.clear()

    #test wrong flow from PPCN_new to PPCN_decision_step_DCC:
    def test_wrong_PPCN_new_to_PPCN_decision_step_DCC(self):

        points = [
            ['PPCN_new','PPCN_decision_step_DCC'],
            ['PPCN_new','PPCN_evaluation_by_DCC'],
            ['PPCN_submitted','PPCN_decision_step_DCC']
        ]
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser)

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                self.assertNotEquals(point[1], state.target)
            self.ppcn_service.update_fsm_state(point[0], self.model, self.superUser)
        
        self.superUser.groups.clear()


     # test flow from PPCN_decision_step_DCC to PPCN_evaluation_by_DCC :
    def test_PPCN_decision_step_DCC_to_PPCN_evaluation_by_DCC(self):
        flow = ['PPCN_decision_step_DCC','PPCN_changes_requested_by_DCC','PPCN_updating_by_request_DCC','PPCN_evaluation_by_DCC']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_DCC')

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model, self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

    # test wrong flow from PPCN_decision_step_DCC to PPCN_evaluation_by_DCC :
    def test_wrong_PPCN_decision_step_DCC_to_PPCN_evaluation_by_DCC(self):
        points = [
            ['PPCN_decision_step_DCC','PPCN_evaluation_by_DCC'],
            ['PPCN_decision_step_DCC','PPCN_updating_by_request_DCC'],
            ['PPCN_changes_requested_by_DCC','PPCN_evaluation_by_DCC']
        ]
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_DCC')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
               
                 self.assertNotEquals(point[1],state.target)
            self.ppcn_service.update_fsm_state(point[0], self.model, self.superUser)

        self.superUser.groups.clear()

     # Test flow from PPCN_decision_step_DCC to PPCN_decision_step_CA
    def test_PPCN_decision_step_DCC_to_PPCN_decision_step_CA(self):
        flow = ['PPCN_decision_step_DCC','PPCN_accepted_request_by_DCC','PPCN_evaluation_by_CA','PPCN_decision_step_CA']
        for group in self.group_list: 
            self.superUser.groups.add(group)
        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_DCC')

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model, self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

    # Test wrong flow from PPCN_decision_step_DCC to PPCN_decision_step_CA
    def test_wrong_PPCN_decision_step_DCC_to_PPCN_decision_step_CA(self):
        points = [
            ['PPCN_decision_step_DCC','PPCN_decision_step_CA'],
            ['PPCN_decision_step_DCC','PPCN_evaluation_by_CA'],
            ['PPCN_accepted_request_by_DCC','PPCN_decision_step_CA']
        ]

        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_DCC')

        for point in points:
            transitions = list(self.model.get_available_fsm_state_transitions())
            for state in transitions:
                 self.assertNotEquals(point[1],state.target)
            self.ppcn_service.update_fsm_state(point[0], self.model, self.superUser)
            
        self.superUser.groups.clear()

    # test flow from PPCN_decision_step_CA to PPCN_end:
    def test_PPCN_decision_step_CA_to_PPCN_end(self):
        flow = ['PPCN_decision_step_CA','PPCN_rejected_request_by_CA','PPCN_end']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_CA')

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

    # test wrong flow from PPCN_decision_step_CA to PPCN_end:
    def test_wrong_PPCN_decision_step_CA_to_PPCN_end(self):
        target = 'PPCN_end'

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_CA')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state.target)


    #test flow from PPCN_decision_step_CA to PPCN_send_recognition_certificate:
    def test_PPCN_decision_step_CA_to_PPCN_send_recognition_certificate(self):
        flow = ['PPCN_decision_step_CA','PPCN_accepted_request_by_CA','PPCN_send_recognition_certificate']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_CA')

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

    #test wrong flow from PPCN_decision_step_CA to PPCN_send_recognition_certificate:
    def test_wrong_PPCN_decision_step_CA_to_PPCN_send_recognition_certificate(self):
        target = 'PPCN_send_recognition_certificate'

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_CA')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state.target)

    #test flow from PPCN_decision_step_DCC to PPCN_end:
    def test_PPCN_decision_step_DCC_to_PPCN_end(self):
        flow = ['PPCN_decision_step_DCC','PPCN_rejected_request_by_DCC','PPCN_end']
        for group in self.group_list: 
            self.superUser.groups.add(group)

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_evaluation_by_DCC')

        for state in flow:
            self.ppcn_service.update_fsm_state(state, self.model,self.superUser)
            self.assertEqual(self.model.fsm_state, state)

        self.superUser.groups.clear()

     #test wrong flow from PPCN_decision_step_DCC to PPCN_end:
    def test_wrong_PPCN_decision_step_DCC_to_PPCN_end(self):
        target = 'PPCN_end'

        client.force_login(self.superUser)
        self.model = PPCN(user=self.superUser,fsm_state='PPCN_decision_step_DCC')

        transitions = list(self.model.get_available_fsm_state_transitions())
        for state in transitions:
            self.assertNotEquals(target,state.target)
