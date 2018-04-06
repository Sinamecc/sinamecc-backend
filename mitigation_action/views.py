from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, Finance, IngeiCompliance, GeographicScale, Location, Mitigation
from mitigation_action.serializers import MitigationSerializer

@api_view(['GET'])
def mitigation_action_test_request(request):
    if request.method == 'GET':
        return Response({'status': 'OK'})

@api_view(['GET'])
def get_mitigations_form(request):
    if request.method == 'GET':
        # get pre loaded mitigation form options
        content = {
            'registration_types': [
                {
                    'id': rt.id,
                    'type': rt.type
                } for rt in RegistrationType.objects.all()
            ],
            'statuses': [
                {
                    'id': st.id,
                    'status': st.status
                } for st in Status.objects.all()
            ],
            'finances': [
                {
                    'id': f.id,
                    'name': f.name,
                    'source': f.source
                } for f in Finance.objects.all()
            ],
            'ingei_compliances': [
                {
                    'id': i.id,
                    'name': i.name
                } for i in IngeiCompliance.objects.all()
            ],
            'geographic_scales': [
                {
                    'id': g.id,
                    'name': g.name
                } for g in GeographicScale.objects.all()
            ]
        }
        return Response(content)

@api_view(['GET', 'POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_mitigations(request):
    # get all mitigation_actions
    if request.method == 'GET':
        mitigations = Mitigation.objects.all()
        serializer = MitigationSerializer(mitigations, many=True)
        return Response(serializer.data)