from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import logging
import logging.config
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
import json
from rest_framework import status
from django.contrib.auth.models import User

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
