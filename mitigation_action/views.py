from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from general.helpers.views import ViewHelper
from django.shortcuts import redirect
from mitigation_action.services import MitigationActionService

from rolepermissions.decorators import has_permission_decorator
service = MitigationActionService()
view_helper = ViewHelper(service)




