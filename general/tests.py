from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import logging
import logging.config
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
import json
from rest_framework import status
from django.contrib.auth.models import User
from general.services import EmailServices

client = Client()

class UrlsTest(TestCase):
    def test_url(self):
        userList = ['admin', 'admin_1', 'admin-1', 'admin.1', 'admin.1.ab', 'foo_bar_1']
        for user in userList:
            self.user = User.objects.get_or_create(username=user)[0]
            client.force_login(self.user)
            path = reverse( "get_user_info_by_name" , args=[self.user.username])
            response = client.get(path)
            self.assertEqual(response.status_code, 200)
            assert response




class EmailServicesTest(TestCase):

    def setUp(self):
        self.emailServicesInstance = EmailServices("izcar@grupoincocr.com")
        self.recipient_list =["Izcarmt95@gmail.com", "sleyter@grupoincocr.com"] 
        self.subject = "UNIT-TEST, AWS - SES"
        self.message_body = "Test, send to notification"

    def test_send_notification_to_multiple_contacts(self):
        
        recipient_list = self.recipient_list
        subject = self.subject
        message_body = self.message_body

        emailServices = self.emailServicesInstance

        response = emailServices.send_notification(recipient_list, subject, message_body)
        
        self.assertEqual(response[0], True)
    
    def test_send_notification_to_a_contact(self):
        
        recipient_list = self.recipient_list[:1]
        subject = self.subject
        message_body = self.message_body

        emailServices = self.emailServicesInstance

        response = emailServices.send_notification(recipient_list, subject, message_body)
        
        self.assertEqual(response[0], True)


    def test_send_notification_contact_empty(self):

        recipient_list = []
        subject = self.subject
        message_body = self.message_body

        emailServices = self.emailServicesInstance

        response = emailServices.send_notification(recipient_list, subject, message_body)
        
        self.assertEqual(response[0], False)