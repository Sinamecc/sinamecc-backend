from django.test import TestCase, Client
from django.urls import reverse
import logging
import logging.config
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
import json
from rest_framework import status
from general.services import EmailServices
from moto import mock_ses
client = Client()
User = get_user_model()

class EmailServicesTest(TestCase):

    def setUp(self):
        self.email_services_instance = EmailServices("sinamec@grupoincocr.com")
        self.recipient_list =["izcar@grupoincocr.com", "izcar@grupoincocr.com"] 
        self.subject = "UNIT-TEST, AWS - SES"
        self.message_body = "Test, send to notification"
        self.AWS_REGION_SES = "us-east-1"


    def test_send_notification_to_multiple_contacts(self):
        
        recipient_list = self.recipient_list
        subject = self.subject
        message_body = self.message_body

        emailServices = self.email_services_instance

        response = emailServices.send_notification(recipient_list, subject, message_body)

        self.assertEqual(response[0], True)

    def test_send_notification_to_a_contact(self):
        recipient_list = self.recipient_list[:1]
        subject = self.subject
        message_body = self.message_body

        emailServices = self.email_services_instance

        response = emailServices.send_notification(recipient_list, subject, message_body)
        
        self.assertEqual(response[0], True)


    def test_send_notification_contact_empty(self):
        recipient_list = []
        subject = self.subject
        message_body = self.message_body

        emailServices = self.email_services_instance

        response = emailServices.send_notification(recipient_list, subject, message_body)
  
        self.assertEqual(response[0], False)