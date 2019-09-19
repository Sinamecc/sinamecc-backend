from django.test import TestCase, Client
from django.utils import timezone
from users.models import CustomUser
from django.contrib.auth.models import Group
from mitigation_action.services import MitigationActionService
from django.urls import reverse
from datetime import datetime
from mitigation_action.models import *
from mitigation_action.serializers import *

# initialize the APIClient app
client = Client()


class MitigationActionFormTest(TestCase):

    def setUp(self):

        self.superUser = CustomUser.objects.get_or_create(username='admin', is_superuser=True)[0]
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]
        client.force_login(self.superUser)

        self.registration_type = RegistrationType.objects.create(type_es='registration_type_es', type_en ='registration_type_en', type_key='type_key')
        self.institution = Institution.objects.create(name='SINAMECC')
        self.contact = Contact.objects.create(full_name='Test_full_name', job_title='Secretary', email='test@gmail.com', phone='77777777')
        self.initiative_contact = Contact.objects.create(full_name='full name', job_title='Secretary initiative', email='initiative@gmail.com', phone='88888888')

        self.status = Status.objects.create(status_es = "mitigation_action_status_es", status_en = 'mitigation_action_status_en')
        self.progress_indicator = ProgressIndicator.objects.create( name = 'progress_indicator', type= 'progress_indicator_type', unit= 'progress_indicator_unit' , start_date = datetime(2005, 11, 5, 18, 00))

        self.finance_source_type = FinanceSourceType.objects.create(name_es = 'finance_source_type_es', name_en = 'finance_source_type_en')
        self.finance_status = FinanceStatus.objects.create(name_es='finance_status_es', name_en='finance_status_en')
        self.initiative_finance = InitiativeFinance.objects.create(status = self.finance_status, finance_source_type= self.finance_source_type, source='initiative_finance_source')
        self.finance = Finance.objects.create(status=self.finance_status, source='finance_source')

        self.ingei_compliance = IngeiCompliance.objects.create(name_es='ingei_compliance_es', name_en='ingei_compliance_en')
        self.ingei_compliance_2 = IngeiCompliance.objects.create(name_es='ingei_compliance_es_2', name_en='ingei_compliance_en_2')

        self.geographic_scale = GeographicScale.objects.create(name_es='geographic_scale_es', name_en='geographic_scale_en')
        self.location = Location.objects.create(geographical_site='location_geographical_site', is_gis_annexed=True)
        self.initiative_type = InitiativeType.objects.create(initiative_type_es='initiative_type_es', initiative_type_en='initiative_type_en')

        self.initiative = Initiative.objects.create(name='initiative_name', objective='initiative_objective', description='initiative_description', goal='initiative_goal', initiative_type=self.initiative_type, entity_responsible='initiative_entity_responsible', contact=self.initiative_contact, budget=999999999.99, finance=self.initiative_finance, status=self.status)

        self.mitigation_action = Mitigation.objects.create(
            strategy_name='mitigation_action_strategy_name',
            name= 'mitigation_action_name',
            purpose = 'mitigation_action_purpose',
            start_date = datetime(2002, 10, 5, 18, 00),
            end_date = datetime(2003, 11, 6, 17, 12),
            gas_inventory = 'mitigation_action_gas',
            emissions_source = 'mitigation_action_emission_source',
            carbon_sinks = 'mitigation_action_carbon_sinks',
            impact_plan = 'mitigation_action_impact_plan',
            impact = 'mitigation_action_impact',
            calculation_methodology = 'mitigation_action_calculation_methodology',
            is_international = True,
            international_participation = 'mitigation_action_internation_participation',
            registration_type = self.registration_type,
            initiative = self.initiative,
            institution = self.institution,
            contact = self.contact,
            status = self.status,
            progress_indicator = self.progress_indicator,
            finance = self.finance,
            geographic_scale = self.geographic_scale,
            location = self.location,
            user=self.superUser
        )

        self.mitigation_action.ingei_compliances.add(self.ingei_compliance, self.ingei_compliance_2)

    

    def test_get_one_mitigation_action(self):
        pass



    def test_get_all_mitigations(self):
        client.force_login(self.superUser)
        response_data = client.get(reverse('get_mitigation', args=['en'])).data
        mitigation = Mitigation.objects.all()
        serialiezed_mitigation = MitigationSerializer(mitigation, many=True).data

        for i in range(mitigation.count()):
               
            self.assertEqual(str(response_data[i].get('id')), str(serialiezed_mitigation[i].get('id')))
            self.assertEqual(str(response_data[i].get('strategy_name')), str(serialiezed_mitigation[i].get('strategy_name')))
            self.assertEqual(str(response_data[i].get('name')), str(serialiezed_mitigation[i].get('name')))
            self.assertEqual(str(response_data[i].get('purpose')), str(serialiezed_mitigation[i].get('purpose')))
            self.assertEqual(str(response_data[i].get('quantitative_purpose')), str(serialiezed_mitigation[i].get('quantitative_purpose')))
            self.assertEqual(str(response_data[i].get('start_date')), str(serialiezed_mitigation[i].get('start_date')))
            self.assertEqual(str(response_data[i].get('end_date')), str(serialiezed_mitigation[i].get('end_date')))
            self.assertEqual(str(response_data[i].get('gas_inventory')), str(serialiezed_mitigation[i].get('gas_inventory')))
            self.assertEqual(str(response_data[i].get('emissions_source')), str(serialiezed_mitigation[i].get('emissions_source')))
            self.assertEqual(str(response_data[i].get('carbon_sinks')), str(serialiezed_mitigation[i].get('carbon_sinks')))
            self.assertEqual(str(response_data[i].get('impact_plan')), str(serialiezed_mitigation[i].get('impact_plan')))
            self.assertEqual(str(response_data[i].get('impact')), str(serialiezed_mitigation[i].get('impact')))
            self.assertEqual(str(response_data[i].get('bibliographic_sources')), str(serialiezed_mitigation[i].get('bibliographic_sources')))
            self.assertEqual(str(response_data[i].get('is_international')), str(serialiezed_mitigation[i].get('is_international')))
            self.assertEqual(str(response_data[i].get('international_participation')), str(serialiezed_mitigation[i].get('international_participation')))
            self.assertEqual(str(response_data[i].get('sustainability')), str(serialiezed_mitigation[i].get('sustainability')))
            self.assertEqual(str(response_data[i].get('question_ucc')), str(serialiezed_mitigation[i].get('question_ucc')))
            self.assertEqual(str(response_data[i].get('question_ovv')), str(serialiezed_mitigation[i].get('question_ovv')))
            self.assertEqual(str(response_data[i].get('review_count')), str(serialiezed_mitigation[i].get('review_count')))

            ## registration type level 
            registration_type = RegistrationTypeSerializer(RegistrationType.objects.get(id=serialiezed_mitigation[i].get('registration_type'))).data
            self.assertEqual(str(response_data[i].get('registration_type').get('id')), str(registration_type.get('id')))
            self.assertEqual(str(response_data[i].get('registration_type').get('type')), str(registration_type.get('type_en')))
            
            ## institution
            institution = InstitutionSerializer(Institution.objects.get(id=serialiezed_mitigation[i].get('institution'))).data
            self.assertEqual(str(response_data[i].get('institution').get('id')), str(institution.get('id')))
            self.assertEqual(str(response_data[i].get('institution').get('name')), str(institution.get('name')))

            ## contact
            contact = ContactSerializer(Contact.objects.get(id=serialiezed_mitigation[i].get('contact'))).data
            self.assertEqual(str(response_data[i].get('contact').get('id')), str(contact.get('id')))
            self.assertEqual(str(response_data[i].get('contact').get('full_name')), str(contact.get('full_name')))
            self.assertEqual(str(response_data[i].get('contact').get('job_title')), str(contact.get('job_title')))
            self.assertEqual(str(response_data[i].get('contact').get('phone')), str(contact.get('phone')))
            self.assertEqual(str(response_data[i].get('contact').get('email')), str(contact.get('email')))

            ## status
            status = StatusSerializer(Status.objects.get(id=serialiezed_mitigation[i].get('status'))).data
            self.assertEqual(str(response_data[i].get('status').get('id')), str(status.get('id')))
            self.assertEqual(str(response_data[i].get('status').get('status')), str(status.get('status_en')))

            ## progress_indicator
            progress_indicator = ProgressIndicatorSerializer(ProgressIndicator.objects.get(id=serialiezed_mitigation[i].get('progress_indicator'))).data
            self.assertEqual(str(response_data[i].get('progress_indicator').get('id')), str(progress_indicator.get('id')))
            self.assertEqual(str(response_data[i].get('progress_indicator').get('name')), str(progress_indicator.get('name')))
            self.assertEqual(str(response_data[i].get('progress_indicator').get('type')), str(progress_indicator.get('type')))
            self.assertEqual(str(response_data[i].get('progress_indicator').get('unit')), str(progress_indicator.get('unit')))
            self.assertEqual(str(response_data[i].get('progress_indicator').get('start_date')), str(progress_indicator.get('start_date')))

     
            ## finance
            finance = FinanceSerializer(Finance.objects.get(id=serialiezed_mitigation[i].get('finance'))).data
            self.assertEqual(str(response_data[i].get('finance').get('id')), str(finance.get('id')))
            self.assertEqual(str(response_data[i].get('finance').get('source')), str(finance.get('source')))

            ## finance source type
            finance_status = FinanceStatusSerializer(FinanceStatus.objects.get(id=finance.get('status'))).data
            self.assertEqual(str(response_data[i].get('finance').get('status').get('id')), str(finance_status.get('id')))
            self.assertEqual(str(response_data[i].get('finance').get('status').get('name')), str(finance_status.get('name_en')))

            ## ingei_compliances missing


            ## geographic_scale
            geographic_scale = GeographicScaleSerializer(GeographicScale.objects.get(id=serialiezed_mitigation[i].get('geographic_scale'))).data
            self.assertEqual(str(response_data[i].get('geographic_scale').get('id')), str(geographic_scale.get('id')))
            self.assertEqual(str(response_data[i].get('geographic_scale').get('name')), str(geographic_scale.get('name_en')))
        
            ## location
            location = LocationSerializer(Location.objects.get(id=serialiezed_mitigation[i].get('location'))).data
            self.assertEqual(str(response_data[i].get('location').get('id')), str(location.get('id')))
            self.assertEqual(str(response_data[i].get('location').get('geographical_site')), str(location.get('geographical_site')))
            self.assertEqual(str(response_data[i].get('location').get('is_gis_annexed')), str(location.get('is_gis_annexed')))


            ## initiative
            initiative = InitiaveSerializer(Initiative.objects.get(id=serialiezed_mitigation[i].get('initiative'))).data
            self.assertEqual(str(response_data[i].get('initiative').get('id')), str(initiative.get('id')))
            self.assertEqual(str(response_data[i].get('initiative').get('name')), str(initiative.get('name')))
            self.assertEqual(str(response_data[i].get('initiative').get('objective')), str(initiative.get('objective')))
            self.assertEqual(str(response_data[i].get('initiative').get('description')), str(initiative.get('description')))
            self.assertEqual(str(response_data[i].get('initiative').get('goal')), str(initiative.get('goal')))
            self.assertEqual(str(response_data[i].get('initiative').get('entity_responsible')), str(initiative.get('entity_responsible')))
            self.assertEqual(str(response_data[i].get('initiative').get('budget')), str(initiative.get('budget')))
            self.assertEqual(str(response_data[i].get('initiative').get('entity_responsible')), str(initiative.get('entity_responsible')))

            ## initiative_type
            initiative_type = InitiativeTypeSerializer(InitiativeType.objects.get(id=initiative.get('initiative_type'))).data
            self.assertEqual(str(response_data[i].get('initiative').get('initiative_type').get('id')), str(initiative_type.get('id')))
            self.assertEqual(str(response_data[i].get('initiative').get('initiative_type').get('initiative_type')), str(initiative_type.get('initiative_type_en')))

            ## inittiative status
            initiative_status = StatusSerializer(Status.objects.get(id=initiative.get('status'))).data
            self.assertEqual(str(response_data[i].get('initiative').get('status').get('id')), str(initiative_status.get('id')))
            self.assertEqual(str(response_data[i].get('initiative').get('status').get('status')), str(initiative_status.get('status_en')))

            ## initiative contact
            initiative_contact = ContactSerializer(Contact.objects.get(id=initiative.get('contact'))).data
            self.assertEqual(str(response_data[i].get('initiative').get('contact').get('id')), str(initiative_contact.get('id')))
            self.assertEqual(str(response_data[i].get('initiative').get('contact').get('full_name')), str(initiative_contact.get('full_name')))
            self.assertEqual(str(response_data[i].get('initiative').get('contact').get('job_title')), str(initiative_contact.get('job_title')))
            self.assertEqual(str(response_data[i].get('initiative').get('contact').get('phone')), str(initiative_contact.get('phone')))
            self.assertEqual(str(response_data[i].get('initiative').get('contact').get('email')), str(initiative_contact.get('email'))) 


            ## initiative finanance 
            initiative_finance = InitiativeFinanceSerializer(InitiativeFinance.objects.get(id=initiative.get('finance'))).data
            self.assertEqual(str(response_data[i].get('initiative').get('finance').get('id')), str(initiative_finance.get('id')))
            self.assertEqual(str(response_data[i].get('initiative').get('finance').get('source')), str(initiative_finance.get('source')))

            ## initiative finance source type
            initiative_finance_status = FinanceStatusSerializer(FinanceStatus.objects.get(id=initiative_finance.get('status'))).data
            self.assertEqual(str(response_data[i].get('initiative').get('finance').get('status').get('id')), str(initiative_finance_status.get('id')))
            self.assertEqual(str(response_data[i].get('initiative').get('finance').get('status').get('name')), str(initiative_finance_status.get('name_en')))
































            datetime_create_response = datetime.strptime(str(response_data[i].get('created')), '%Y-%m-%d %H:%M:%S.%f+00:00')
            datetime_create_serializer = datetime.strptime(str(serialiezed_mitigation[i].get('created')), '%Y-%m-%dT%H:%M:%S.%fZ')
            self.assertEqual(datetime_create_response, datetime_create_serializer)

            datetime_updated_response = datetime.strptime(str(response_data[i].get('updated')), '%Y-%m-%d %H:%M:%S.%f+00:00')
            datetime_updated_serializer = datetime.strptime(str(serialiezed_mitigation[i].get('updated')), '%Y-%m-%dT%H:%M:%S.%fZ')
            self.assertEqual(datetime_updated_response,datetime_updated_serializer)
           
       
    