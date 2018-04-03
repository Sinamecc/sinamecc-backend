from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from mitigation_action.models import MitigationAction
from mitigation_action.serializers import MitigationActionSerializer

@api_view(['GET'])
def mitigation_action_test_request(request):
    if request.method == 'GET':
        return Response({'status': 'OK'})

@api_view(['GET', 'POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_mitigation_actions(request):
    # get all mitigation_actions
    if request.method == 'GET':
        mitigation_actions = MitigationAction.objects.all()
        serializer = MitigationActionSerializer(mitigation_actions, many=True)
        return Response(serializer.data)