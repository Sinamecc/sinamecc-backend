from django.test import TestCase, Client
from mccr.models import *
from mitigation_action.models import Mitigation
from users.models import CustomUser
from mccr.services import MCCRService


client = Client()

class MCCRFormTest(TestCase):

    def setUp(self):
        self.superUser = CustomUser.objects.get_or_create(username='admin', is_superuser=True)[0]
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]
        client.force_login(self.superUser)

        self.user_type = MCCRUserType.objects.create(name='user_type_name')
        self.mitigation_action = Mitigation.objects.create(user=self.superUser)
        self.mccr_registry = MCCRRegistry.objects.create(status='mccr_status', user_type=self.user_type, mitigation=self.mitigation_action, user = self.superUser)
        self.ovv = OVV.objects.create(name='ovv_name', email='ovv@email.com', phone=89898989)
        self.ovv_2 = OVV.objects.create(name='ovv_name_2', email='ovv2@email.com', phone=77777777)
        self.ovv_mccr_related_1 = MCCRRegistryOVVRelation.objects.create(ovv=self.ovv, mccr=self.mccr_registry, status='ovv_mccr_status')
        self.ovv_mccr_related_2 = MCCRRegistryOVVRelation.objects.create(ovv=self.ovv_2, mccr=self.mccr_registry)
    def test_user_type(self):

        field_name = self.user_type.name

        self.assertEqual(field_name, 'user_type_name')
    
    def test_mccr_registry(self):

        field_user_type = self.mccr_registry.user_type
        field_status =self.mccr_registry.status
        field_mitigation = self.mccr_registry.mitigation
        field_user = self.mccr_registry.user
        field_fsm_state = self.mccr_registry.fsm_state
        
        self.assertEqual(field_user_type, self.user_type)
        self.assertEqual(field_status, 'mccr_status')
        self.assertEqual(field_mitigation, self.mitigation_action)
        self.assertEqual(field_user, self.superUser)
        self.assertEqual(field_fsm_state, 'new')
    
    def test_ovv(self):

        field_name = self.ovv.name
        field_email = self.ovv.email
        field_phone = self.ovv.phone

        self.assertEqual(field_name, 'ovv_name')
        self.assertEqual(field_email, 'ovv@email.com')
        self.assertEqual(field_phone, 89898989)

    def test_mccr_ovv_related(self):

        field_mccr_1 = self.ovv_mccr_related_1.mccr
        field_mccr_2 = self.ovv_mccr_related_2.mccr 

        field_ovv_1 = self.ovv_mccr_related_1.ovv
        field_ovv_2 = self.ovv_mccr_related_2.ovv

        field_status_1 = self.ovv_mccr_related_1.status
        field_status_2 = self.ovv_mccr_related_2.status


        self.assertEqual(field_mccr_1, self.mccr_registry)
        self.assertEqual(field_mccr_2, self.mccr_registry)
        self.assertEqual(field_ovv_1, self.ovv)
        self.assertEqual(field_ovv_2, self.ovv_2)
        self.assertEqual(field_status_1, 'ovv_mccr_status')
        self.assertEqual(field_status_2, None)

        