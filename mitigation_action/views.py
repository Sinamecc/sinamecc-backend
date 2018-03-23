from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status

@api_view(['GET'])
def mitigation_action_test_request(request)
    if request.method == 'GET':
        return Response({'status': 'OK'})
