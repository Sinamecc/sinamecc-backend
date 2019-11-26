from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from general.serializers import UserSerializer
from django.contrib.auth.models import  Group
from django.urls import reverse
client = Client()
User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        user = User.objects.get_or_create(username='admin')[0]
        client.force_login(user)
        self.user1 = User.objects.create(username="admin_user", password="cambiame", is_superuser=True, first_name="Izacar", last_name="Muños", email="izacar@mail.com", is_staff=True, is_active=True, date_joined="2018-11-02T15:07:02.653Z", last_login= None )
        

    def test_user_info(self):
        response = client.get(reverse('get_user_info_by_name', kwargs={'username': 'admin_user'}))
        user_serial = User.objects.get(username=self.user1.username)
        serial = UserSerializer(user_serial)

        self.assertEqual(str(response.data.get('id')), str(serial.data.get('id')))
        self.assertEqual(str(response.data.get('username')), str(serial.data.get('username')))
        self.assertEqual(str(response.data.get('email')), str(serial.data.get('email')))
        self.assertEqual(str(response.data.get('is_active')), str(serial.data.get('is_active')))


    ## missing more tests