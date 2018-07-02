from django.test import TestCase, Client
from django.utils import timezone
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

import json
import uuid
import datetime 
from datetime import datetime
from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, FinanceSourceType, Finance, IngeiCompliance, GeographicScale, Location, Mitigation, ChangeLog
from mitigation_action.serializers import RegistrationTypeSerializer, ContactSerializer, StatusSerializer, ProgressIndicatorSerializer, FinanceSourceTypeSerializer, FinanceSerializer, IngeiComplianceSerializer, GeographicScaleSerializer, LocationSerializer, MitigationSerializer
from workflow.models import Comment, ReviewStatus

# initialize the APIClient app
client = Client()

class MitigationActionTest(TestCase):

    def setUp(self):
        user = User.objects.get_or_create(username='testuser')[0]
        client.force_login(user)
        self.progress_indicator = ProgressIndicator.objects.create( name = 'Carbon reduction', type= 'kl', unit= '5' , start_date = datetime(2005, 11, 5, 18, 00))
        self.resgistrationType = RegistrationType.objects.create(type_es = 'Inscripción por primera vez', type_en = 'Registration for the first time')
        self.contact = Contact.objects.create(full_name = 'Marco', job_title = 'Manager', email = 'mail@mail.com', phone = '88888888')
        self.finance_source_type = FinanceSourceType.objects.create(name_es = 'Por obtener', name_en = 'to obtain')
        self.finance = Finance.objects.create(finance_source_type = self.finance_source_type, source = 'SINAMECC')
        self.ingei_compliances = IngeiCompliance.objects.create(name_es = 'Engei es', name_en = 'Engie en')
        self.geographic_scale = GeographicScale.objects.create(name_es = 'Nacional', name_en = 'National')
        self.location = Location.objects.create(geographical_site = 'CR', is_gis_annexed = False)
        self.status = Status.objects.create(status_es = "Planeación", status_en = 'Planning')
        self.review_status = ReviewStatus.objects.create(status = 'Status')
        self.institution = Institution.objects.create(name = 'SINAMECC')
        self.comments = Comment.objects.create(comment = 'My comment')
        self.mitigation = Mitigation.objects.create(
            strategy_name = 'Strategy name', 
            name = 'Chemical pollution', 
            purpose = 'Reduce chemical pollution', 
            quantitative_purpose = 'Porpuse', 
            start_date = datetime(2002, 10, 5, 18, 00), 
            end_date = datetime(2009, 10, 5, 18, 00), 
            gas_inventory = 'Gas', 
            emissions_source = 'Cars', 
            carbon_sinks = 'forests of CR', 
            impact_plan = 'Impact plan', 
            impact = 'Impacto', 
            bibliographic_sources = 'UCR', 
            is_international = True, 
            international_participation = 'ONU', 
            sustainability = 'Yes',
            question_ucc = '5',
            question_ovv = 'MINAET',
            user = user,
            registration_type = self.resgistrationType,
            institution = self.institution,
            contact = self.contact,
            status = self.status, 
            progress_indicator = self.progress_indicator,
            finance = self.finance,
            geographic_scale = self.geographic_scale,
            location = self.location,
            review_count = 1,
            review_status = self.review_status,
            created = timezone.now(),
            updated = timezone.now()
        )

        self.mitigation.ingei_compliances.create(name_es = 'Engei es', name_en = 'Engie en')
        self.mitigation.comments.create(comment = 'My comment')

        self.changeLog = ChangeLog.objects.create(date = timezone.now(), mitigation_action = self.mitigation, previous_status =  self.review_status, current_status = self.review_status, user = user )

    def test_get_valid_single_mitigations(self):
        response = client.get(reverse('get_delete_update__patch_mitigation', kwargs={'pk': self.mitigation.pk}))
        mitigation = Mitigation.objects.get(pk=self.mitigation.pk)
        serializer = MitigationSerializer(mitigation)
        uuidStr = uuid.UUID(str(response.data.get('id'))).hex
        uuidSerializer = uuid.UUID(str(serializer.data.get('id'))).hex

        self.assertEqual(uuidStr, uuidSerializer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(str(response.data.get('strategy_name')), str(serializer.data.get('strategy_name')))
        self.assertEqual(str(response.data.get('name')), str(serializer.data.get('name')))
        self.assertEqual(str(response.data.get('purpose')), str(serializer.data.get('purpose')))
        self.assertEqual(str(response.data.get('quantitative_purpose')), str(serializer.data.get('quantitative_purpose')))
        self.assertEqual(str(response.data.get('start_date')), str(serializer.data.get('start_date')))
        self.assertEqual(str(response.data.get('end_date')), str(serializer.data.get('end_date')))
        self.assertEqual(str(response.data.get('gas_inventory')), str(serializer.data.get('gas_inventory')))
        self.assertEqual(str(response.data.get('emissions_source')), str(serializer.data.get('emissions_source')))
        self.assertEqual(str(response.data.get('carbon_sinks')), str(serializer.data.get('carbon_sinks')))
        self.assertEqual(str(response.data.get('impact_plan')), str(serializer.data.get('impact_plan')))
        self.assertEqual(str(response.data.get('impact')), str(serializer.data.get('impact')))
        self.assertEqual(str(response.data.get('bibliographic_sources')), str(serializer.data.get('bibliographic_sources')))
        self.assertIs(str(response.data.get('is_international')), str(serializer.data.get('is_international')))
        self.assertEqual(str(response.data.get('sustainability')), str(serializer.data.get('sustainability')))
        self.assertEqual(str(response.data.get('question_ucc')), str(serializer.data.get('question_ucc')))
        self.assertEqual(str(response.data.get('question_ovv')), str(serializer.data.get('question_ovv')))
        self.assertEqual(str(response.data.get('user')['id']), str(serializer.data.get('user')))
        self.assertEqual(str(response.data.get('registration_type')['id']), str(serializer.data.get('registration_type')))
        self.assertEqual(str(response.data.get('institution')['id']), str(serializer.data.get('institution')))
        self.assertEqual(str(response.data.get('contact')['id']), str(serializer.data.get('contact')))
        self.assertEqual(str(response.data.get('status')['id']), str(serializer.data.get('status')))
        self.assertEqual(str(response.data.get('progress_indicator')['id']), str(serializer.data.get('progress_indicator')))
        self.assertEqual(str(response.data.get('finance')['id']), str(serializer.data.get('finance')))
        self.assertEqual(str(response.data.get('geographic_scale')['id']), str(serializer.data.get('geographic_scale')))
        self.assertEqual(str(response.data.get('location')['id']), str(serializer.data.get('location')))
        self.assertEqual(str(response.data.get('review_count')), str(serializer.data.get('review_count')))
        self.assertEqual(str(response.data.get('review_status')['id']), str(serializer.data.get('review_status')))
        self.assertEqual(str(response.data.get('comments')[0]['id']), str(serializer.data.get('comments')[0]))

        datetime_create_response = datetime.strptime(str(response.data.get('created')), '%Y-%m-%d %H:%M:%S.%f+00:00')
        datetime_create_serializer = datetime.strptime(str(serializer.data.get('created')), '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEqual(datetime_create_response, datetime_create_serializer)

        datetime_updated_response = datetime.strptime(str(response.data.get('updated')), '%Y-%m-%d %H:%M:%S.%f+00:00')
        datetime_updated_serializer = datetime.strptime(str(serializer.data.get('updated')), '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEqual(datetime_updated_response,datetime_updated_serializer)
        

    def test_get_all_mitigations(self):
        response = client.get(reverse('get_post_mitigations'))
        mitigation = Mitigation.objects.all()
        serializer = MitigationSerializer(mitigation, many=True)
        for serial in serializer.data:
            for resp in response.data:
                self.assertEqual(str(resp.get('strategy_name')), str(serial.get('strategy_name')))
                self.assertEqual(str(resp.get('name')), str(serial.get('name')))
                self.assertEqual(str(resp.get('purpose')), str(serial.get('purpose')))
                self.assertEqual(str(resp.get('quantitative_purpose')), str(serial.get('quantitative_purpose')))
                self.assertEqual(str(resp.get('start_date')), str(serial.get('start_date')))
                self.assertEqual(str(resp.get('end_date')), str(serial.get('end_date')))
                self.assertEqual(str(resp.get('gas_inventory')), str(serial.get('gas_inventory')))
                self.assertEqual(str(resp.get('emissions_source')), str(serial.get('emissions_source')))
                self.assertEqual(str(resp.get('carbon_sinks')), str(serial.get('carbon_sinks')))
                self.assertEqual(str(resp.get('impact_plan')), str(serial.get('impact_plan')))
                self.assertEqual(str(resp.get('impact')), str(serial.get('impact')))
                self.assertEqual(str(resp.get('bibliographic_sources')), str(serial.get('bibliographic_sources')))
                self.assertIs(str(resp.get('is_international')), str(serial.get('is_international')))
                self.assertEqual(str(resp.get('sustainability')), str(serial.get('sustainability')))
                self.assertEqual(str(resp.get('question_ucc')), str(serial.get('question_ucc')))
                self.assertEqual(str(resp.get('question_ovv')), str(serial.get('question_ovv')))
                self.assertEqual(str(resp.get('user')['id']), str(serial.get('user')))
                self.assertEqual(str(resp.get('registration_type')['id']), str(serial.get('registration_type')))
                self.assertEqual(str(resp.get('institution')['id']), str(serial.get('institution')))
                self.assertEqual(str(resp.get('contact')['id']), str(serial.get('contact')))
                self.assertEqual(str(resp.get('status')['id']), str(serial.get('status')))
                self.assertEqual(str(resp.get('progress_indicator')['id']), str(serial.get('progress_indicator')))
                self.assertEqual(str(resp.get('finance')['id']), str(serial.get('finance')))
                self.assertEqual(str(resp.get('geographic_scale')['id']), str(serial.get('geographic_scale')))
                self.assertEqual(str(resp.get('location')['id']), str(serial.get('location')))
                self.assertEqual(str(resp.get('review_count')), str(serial.get('review_count')))
                self.assertEqual(str(resp.get('review_status')['id']), str(serial.get('review_status')))
                self.assertEqual(str(resp.get('comments')[0]['id']), str(serial.get('comments')[0]))

                datetime_create_response = datetime.strptime(str(resp.get('created')), '%Y-%m-%d %H:%M:%S.%f+00:00')
                datetime_create_serializer = datetime.strptime(str(serial.get('created')), '%Y-%m-%dT%H:%M:%S.%fZ')
                self.assertEqual(datetime_create_response, datetime_create_serializer)

                datetime_updated_response = datetime.strptime(str(resp.get('updated')), '%Y-%m-%d %H:%M:%S.%f+00:00')
                datetime_updated_serializer = datetime.strptime(str(serial.get('updated')), '%Y-%m-%dT%H:%M:%S.%fZ')
                self.assertEqual(datetime_updated_response,datetime_updated_serializer)

        self.assertEqual( str(serializer.data[0].get('strategy_name')), 'Strategy name')
        self.assertTrue(len(mitigation) > 0, "You should have at least a mitigation")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_url_form_es_en(self):
        self.user = User.objects.get_or_create(username='testuser')[0]
        client.force_login(self.user)
        path = reverse( "get_mitigations_form_es_en" , kwargs={'language': 'es'})
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
        assert response
    def test_get_post_mitigations(self):
        user = User.objects.get_or_create(username='testuser')[0]
        client.force_login(user)
        
        response = client.get(reverse('get_post_mitigations'))
        mitigation = Mitigation.objects.all()
        seralizer = MitigationSerializer(mitigation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_delete_update_mitigation(self):
        response = client.delete(reverse('get_delete_update__patch_mitigation', kwargs={'pk': self.mitigation.pk} ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_get_delete_update_mitigation(self):
        response = client.delete(reverse('get_delete_update__patch_mitigation', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_url_form_es_en(self):
        self.user = User.objects.get_or_create(username='testuser')[0]
        client.force_login(self.user)
        path = reverse( "get_mitigations_form_es_en" , kwargs={'language': 'es'})
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
        assert response