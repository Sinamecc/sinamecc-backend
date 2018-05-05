from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, Finance, IngeiCompliance, GeographicScale, Location, Mitigation
from mitigation_action.serializers import FinanceSerializer, LocationSerializer, ProgressIndicatorSerializer, ContactSerializer, MitigationSerializer
import uuid

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_mitigation(request, pk):
    try:
        mitigation = Mitigation.objects.get(pk=pk)
    except Mitigation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single report_file
    if request.method == 'GET':
        content = {
            'id': mitigation.id,
            'strategy_name': mitigation.strategy_name,
            'name': mitigation.name,
            'purpose': mitigation.purpose,
            'quantitative_purpose': mitigation.quantitative_purpose,
            'start_date': mitigation.start_date,
            'end_date': mitigation.end_date,
            'gas_inventory': mitigation.gas_inventory,
            'emissions_source': mitigation.emissions_source,
            'carbon_sinks': mitigation.carbon_sinks,
            'impact_plan': mitigation.impact_plan,
            'impact': mitigation.impact,
            'bibliographic_sources': mitigation.bibliographic_sources,
            'is_international': mitigation.is_international,
            'international_participation': mitigation.international_participation,
            'sustainability': mitigation.sustainability,
            'question_ucc': mitigation.question_ucc,
            'user': {
                'id': mitigation.user.id,
                'username': mitigation.user.username,
                'email': mitigation.user.email
            },
            'registration_type': {
                'id': mitigation.registration_type.id,
                'type': mitigation.registration_type.type
            },
            'institution': {
                'id': mitigation.institution.id,
                'name': mitigation.institution.name
            },
            'contact': {
                'id': mitigation.contact.id,
                'full_name': mitigation.contact.full_name,
                'job_title': mitigation.contact.job_title,
                'email': mitigation.contact.email,
                'phone': mitigation.contact.phone
            },
            'status': {
                'id': mitigation.status.id,
                'status': mitigation.status.status
            },
            'progress_indicator': {
                'id': mitigation.progress_indicator.id,
                'name': mitigation.progress_indicator.name,
                'type': mitigation.progress_indicator.type,
                'unit': mitigation.progress_indicator.unit,
                'start_date': mitigation.progress_indicator.start_date
            },
            'finance': {
                'id': mitigation.finance.id,
                'name': mitigation.finance.name,
                'source': mitigation.finance.source
            },
            'ingei_compliances': [
                {
                   'id': ingei.id,
                   'name': ingei.name
                } for ingei in mitigation.ingei_compliances.all()
            ],
            'geographic_scale': {
                'id': mitigation.geographic_scale.id,
                'name': mitigation.geographic_scale.name
            },
            'location': {
                'id': mitigation.location.id,
                'geographical_site': mitigation.location.geographical_site,
                'is_gis_annexed': mitigation.location.is_gis_annexed
            },
            'created': mitigation.created,
            'updated': mitigation.updated
        }
        return Response(content)
    # delete a single mitigation
    elif request.method == 'DELETE':
        mitigation.ingei_compliances.clear()
        mitigation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update details of a single report_file
    elif request.method == 'PUT':
        contact_id = request.data.get('contact[id]')
        progress_indicator_id = request.data.get('progress_indicator[id]')
        location_id = request.data.get('location[id]')
        finance_id = request.data.get('finance[id]')
        contact = Contact.objects.get(pk=contact_id)
        progress_indicator = ProgressIndicator.objects.get(pk=progress_indicator_id)
        location = Location.objects.get(pk=location_id)
        finance = Finance.objects.get(pk=finance_id)
        contact_data = {
            'full_name': request.data.get('contact[full_name]'),
            'job_title': request.data.get('contact[job_title]'),
            'email': request.data.get('contact[email]'),
            'phone': request.data.get('contact[phone]'),
        }
        progress_indicator_data = {
            'name': request.data.get('progress_indicator[name]'),
            'type': request.data.get('progress_indicator[type]'),
            'unit': request.data.get('progress_indicator[unit]'),
            'start_date': request.data.get('progress_indicator[start_date]')
        }
        location_data = {
            'geographical_site': request.data.get('location[geographical_site]'),
            'is_gis_annexed': request.data.get('location[is_gis_annexed]')
        }
        finance_data = {
            'name': request.data.get('finance[name]'),
            'source': request.data.get('finance[source]'),
        }
        contact_serializer = ContactSerializer(contact, data=contact_data)
        progress_indicator_serializer = ProgressIndicatorSerializer(progress_indicator, data=progress_indicator_data)
        location_serializer = LocationSerializer(location, data=location_data)
        finance_serializer = FinanceSerializer(finance, data=finance_data)

        if contact_serializer.is_valid() and progress_indicator_serializer.is_valid() and location_serializer.is_valid() and finance_serializer.is_valid():
            contact_serializer.save()
            progress_indicator_serializer.save()
            location_serializer.save()
            finance_serializer.save()
            mitigation_data = {
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
                'question_ucc': request.data.get('question_ucc'),
                'user': request.data.get('user'),
                'registration_type': request.data.get('registration_type'),
                'institution': request.data.get('institution'),
                'contact': contact_id,
                'status': request.data.get('status'),
                'progress_indicator': progress_indicator_id,
                'finance': finance_id,
                'ingei_compliance': request.data.get('ingei_compliance'),
                'geographic_scale': request.data.get('geographic_scale'),
                'location': location_id
            }
            mitigation_serializer = MitigationSerializer(mitigation, data=mitigation_data)
            if mitigation_serializer.is_valid():
                mitigation = mitigation_serializer.save()
                # Clear INGEI associations
                mitigation.ingei_compliances.clear()
                # Assign INGEI Compliances
                ingei_ids_str = request.data.get('ingei_compliances')
                ingei_ids_array = list(map(int, ingei_ids_str.split(',')))
                for id in ingei_ids_array:
                    try:
                        ingei = IngeiCompliance.objects.get(pk=id)
                    except IngeiCompliance.DoesNotExist:
                        error = {
                            'status': status.HTTP_404_NOT_FOUND,
                            'error': 'One or More INGEI Compliances not found.'
                        }
                        return Response(error)
                    mitigation.ingei_compliances.add(ingei)
                return Response(mitigation_serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response('Bad Request', status=status.HTTP_400_BAD_REQUEST)

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
            'institutions': [
                {
                    'id': i.id,
                    'name': i.name
                } for i in Institution.objects.all()
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
        # serializer = MitigationSerializer(mitigations, many=True)
        content = [
            {
                'id': m.id,
                'strategy_name': m.strategy_name,
                'name': m.name,
                'purpose': m.purpose,
                'quantitative_purpose': m.quantitative_purpose,
                'start_date': m.start_date,
                'end_date': m.end_date,
                'gas_inventory': m.gas_inventory,
                'emissions_source': m.emissions_source,
                'carbon_sinks': m.carbon_sinks,
                'impact_plan': m.impact_plan,
                'impact': m.impact,
                'bibliographic_sources': m.bibliographic_sources,
                'is_international': m.is_international,
                'international_participation': m.international_participation,
                'sustainability': m.sustainability,
                'question_ucc': m.question_ucc,
                'user': {
                    'id': m.user.id,
                    'username': m.user.username,
                    'email': m.user.email
                },
                'registration_type': {
                    'id': m.registration_type.id,
                    'type': m.registration_type.type
                },
                'institution': {
                    'id': m.institution.id,
                    'name': m.institution.name
                },
                'contact': {
                    'id': m.contact.id,
                    'full_name': m.contact.full_name,
                    'job_title': m.contact.job_title,
                    'email': m.contact.email,
                    'phone': m.contact.phone
                },
                'status': {
                    'id': m.status.id,
                    'status': m.status.status
                },
                'progress_indicator': {
                    'id': m.progress_indicator.id,
                    'name': m.progress_indicator.name,
                    'type': m.progress_indicator.type,
                    'unit': m.progress_indicator.unit,
                    'start_date': m.progress_indicator.start_date
                },
                'finance': {
                    'id': m.finance.id,
                    'name': m.finance.name,
                    'source': m.finance.source
                },
                'ingei_compliances': [
                    {
                    'id': ingei.id,
                    'name': ingei.name
                    } for ingei in m.ingei_compliances.all()
                ],
                'geographic_scale': {
                    'id': m.geographic_scale.id,
                    'name': m.geographic_scale.name
                },
                'location': {
                    'id': m.location.id,
                    'geographical_site': m.location.geographical_site,
                    'is_gis_annexed': m.location.is_gis_annexed
                },
                'created': m.created,
                'updated': m.updated
            } for m in Mitigation.objects.all()
        ]
        return Response(content)
    # insert a new record for a mitigation
    elif request.method == 'POST':
        contact_data = {
            'full_name': request.data.get('contact[full_name]'),
            'job_title': request.data.get('contact[job_title]'),
            'email': request.data.get('contact[email]'),
            'phone': request.data.get('contact[phone]'),
        }
        progress_indicator_data = {
            'name': request.data.get('progress_indicator[name]'),
            'type': request.data.get('progress_indicator[type]'),
            'unit': request.data.get('progress_indicator[unit]'),
            'start_date': request.data.get('progress_indicator[start_date]')
        }
        location_data = {
            'geographical_site': request.data.get('location[geographical_site]'),
            'is_gis_annexed': request.data.get('location[is_gis_annexed]')
        }
        finance_data = {
            'name': request.data.get('finance[name]'),
            'source': request.data.get('finance[source]'),
        }
        contact_serializer = ContactSerializer(data=contact_data)
        progress_indicator_serializer = ProgressIndicatorSerializer(data=progress_indicator_data)
        location_serializer = LocationSerializer(data=location_data)
        finance_serializer = FinanceSerializer(data=finance_data)
        if contact_serializer.is_valid() and progress_indicator_serializer.is_valid() and location_serializer.is_valid() and finance_serializer.is_valid():
            contact = contact_serializer.save()
            progress_indicator = progress_indicator_serializer.save()
            location = location_serializer.save()
            finance = finance_serializer.save()
            mitigation_data = {
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
                'question_ucc': request.data.get('question_ucc'),
                'user': request.data.get('user'),
                'registration_type': request.data.get('registration_type'),
                'institution': request.data.get('institution'),
                'contact': contact.id,
                'status': request.data.get('status'),
                'progress_indicator': progress_indicator.id,
                'finance': finance.id,
                'geographic_scale': request.data.get('geographic_scale'),
                'location': location.id,
                'review_count': 0, # TODO: Change to a null = true field and add default to zero.
                'review_status': 1 # TODO: Create service to determine the status.
            }
            mitigation_serializer = MitigationSerializer(data=mitigation_data)
            if mitigation_serializer.is_valid():
                mitigation = mitigation_serializer.save()
                # Assign INGEI Compliances
                ingei_ids_str = request.data.get('ingei_compliances')
                ingei_ids_array = list(map(int, ingei_ids_str.split(',')))
                for id in ingei_ids_array:
                    try:
                        ingei = IngeiCompliance.objects.get(pk=id)
                    except IngeiCompliance.DoesNotExist:
                        error = {
                            'status': status.HTTP_404_NOT_FOUND,
                            'error': 'One or More INGEI Compliances not found.'
                        }
                        return Response(error)
                    mitigation.ingei_compliances.add(ingei)
                return Response(mitigation_serializer.data, status=status.HTTP_201_CREATED)
        return Response('Bad Request', status=status.HTTP_400_BAD_REQUEST)
