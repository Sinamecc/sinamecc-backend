from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, Finance, IngeiCompliance, GeographicScale, Location, Mitigation
from mitigation_action.serializers import MitigationSerializer
import uuid

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
    # insert a new record for a mitigation
    elif request.method == 'POST':
        data = {
            'id': str(uuid.uuid4()),
            'strategy_name': request.data.get('strategy_name'),
            'name': request.data.get('name'),
            'purpose': request.data.get('purpose'),
            'quantitative_purpose': request.data.get('quantitative_purpose'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'gas_inventory': request.data.get('gas_inventory'),
            'emissions_source': request.data.get('emissions_source'),
            'carbon_sinks': request.data.get('carbon_sinks'),
            'impact_plan': request.data.get('impact_plan'),
            'impact': request.data.get('impact'),
            'bibliographic_sources': request.data.get('bibliographic_sources'),
            'is_international': request.data.get('is_international'),
            'international_participation': request.data.get('international_participation'),
            'sustainability': request.data.get('sustainability'),
            'user': request.data.get('user'),
            'registration_type': request.data.get('registration_type'),
            'institution': request.data.get('institution'),
            'contact': request.data.get('contact'),
            'status': request.data.get('status'),
            'progress_indicator': request.data.get('progress_indicator'),
            'finance': request.data.get('finance'),
            'ingei_compliance': request.data.get('ingei_compliance'),
            'geographic_scale': request.data.get('geographic_scale'),
            'location': request.data.get('location')
        }
        serializer = MitigationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        