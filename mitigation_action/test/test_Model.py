from django.test import TestCase, Client
from django.utils import timezone
from users.models import CustomUser
from django.contrib.auth.models import Group
from mitigation_action.services import MitigationActionService

from datetime import datetime
from mitigation_action.models import *
from mitigation_action.serializers import *

# initialize the APIClient app
client = Client()


class MitigationActionModelTest(TestCase):

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
    

    def test_registration_type(self):

        field_type_es = self.registration_type.type_es
        field_type_en = self.registration_type.type_en
        field_type_key = self.registration_type.type_key

        self.assertEquals(field_type_es, 'registration_type_es')
        self.assertEquals(field_type_en, 'registration_type_en')
        self.assertEquals(field_type_key, 'type_key')

    def test_institution(self):
        
        field_institution = self.institution.name

        self.assertEqual(field_institution, 'SINAMECC')

    def test_contact(self):
 
        field_full_name = self.contact.full_name
        field_job_title = self.contact.job_title
        field_email = self.contact.email
        field_phone = self.contact.phone

        self.assertEquals(field_full_name, 'Test_full_name')
        self.assertEquals(field_job_title, 'Secretary')
        self.assertEquals(field_email, 'test@gmail.com')
        self.assertEquals(field_phone, '77777777')

    def test_status(self):
        
        field_status_es = self.status.status_es
        field_status_en = self.status.status_en

        self.assertEqual(field_status_es, 'mitigation_action_status_es')
        self.assertEqual(field_status_en, 'mitigation_action_status_en')

    def test_progress_indicator(self):

        field_name = self.progress_indicator.name
        field_type = self.progress_indicator.type
        field_unit = self.progress_indicator.unit
        field_start_date = self.progress_indicator.start_date

        self.assertEqual(field_name, 'progress_indicator')
        self.assertEqual(field_type, 'progress_indicator_type')
        self.assertEqual(field_unit, 'progress_indicator_unit')
        self.assertEqual(field_start_date, datetime(2005, 11, 5, 18, 00))

    def test_finance_source_type(self):
        field_name_es = self.finance_source_type.name_es
        field_name_en = self.finance_source_type.name_en

        self.assertEqual(field_name_es, 'finance_source_type_es')
        self.assertEqual(field_name_en, 'finance_source_type_en')

    def test_finance_source_type(self):
        field_name_es = self.finance_status.name_es
        field_name_en = self.finance_status.name_en

        self.assertEqual(field_name_es, 'finance_status_es')
        self.assertEqual(field_name_en, 'finance_status_en')
    
    def test_initiative_finance(self):
        field_finance_status = self.initiative_finance.status
        field_finance_source_type = self.initiative_finance.finance_source_type
        field_source = self.initiative_finance.source

        self.assertEqual(field_finance_status, self.finance_status)
        self.assertEqual(field_finance_source_type, self.finance_source_type)
        self.assertEqual(field_source, 'initiative_finance_source')
    
    def test_finance(self):
        field_finance_status = self.finance.status
        field_source = self.finance.source

        self.assertEqual(field_finance_status, self.finance_status)
        self.assertEqual(field_source, 'finance_source')
    
    def test_ingei_compliance(self):

        field_name_es = self.ingei_compliance.name_es
        field_name_en = self.ingei_compliance.name_en

        self.assertEqual(field_name_es, 'ingei_compliance_es')
        self.assertEqual(field_name_en, 'ingei_compliance_en')

    def test_geographic_scale(self):

        field_name_es = self.geographic_scale.name_es
        field_name_en = self.geographic_scale.name_en

        self.assertEqual(field_name_es, 'geographic_scale_es')
        self.assertEqual(field_name_en, 'geographic_scale_en')
    
    def test_location(self):

        field_geographical_site = self.location.geographical_site
        field_is_gis_annexed = self.location.is_gis_annexed

        self.assertEqual(field_geographical_site, 'location_geographical_site')
        self.assertEqual(field_is_gis_annexed, True)

    def test_initiative_type(self):

        field_initiative_type_es = self.initiative_type.initiative_type_es
        field_initiative_type_en = self.initiative_type.initiative_type_en

        self.assertEqual(field_initiative_type_es, 'initiative_type_es')
        self.assertEqual(field_initiative_type_en, 'initiative_type_en')

    def test_initiative(self):

        field_name = self.initiative.name
        field_objective = self.initiative.objective
        field_description = self.initiative.description
        field_goal = self.initiative.goal
        field_initiative_type = self.initiative.initiative_type
        field_entity_responsible = self.initiative.entity_responsible
        field_contact = self.initiative.contact
        field_budget = self.initiative.budget
        field_finance = self.initiative.finance
        field_status = self.initiative.status

        self.assertEqual(field_name, 'initiative_name')
        self.assertEqual(field_objective, 'initiative_objective')
        self.assertEqual(field_description, 'initiative_description')
        self.assertEqual(field_goal, 'initiative_goal')
        self.assertEqual(field_initiative_type, self.initiative_type)
        self.assertEqual(field_entity_responsible, 'initiative_entity_responsible')
        self.assertEqual(field_contact, self.initiative_contact)
        self.assertEqual(field_budget, 999999999.99)
        self.assertEqual(field_finance, self.initiative_finance)
        self.assertEqual(field_status, self.status)

    def test_mitigation_action(self):

        field_strategy_name= self.mitigation_action.strategy_name
        field_name = self.mitigation_action.name
        field_purpose = self.mitigation_action.purpose
        field_start_date = self.mitigation_action.start_date
        field_end_date = self.mitigation_action.end_date
        field_gas_inventory = self.mitigation_action.gas_inventory
        field_emissions_source = self.mitigation_action.emissions_source
        field_carbon_sinks = self.mitigation_action.carbon_sinks
        field_impact_plan = self.mitigation_action.impact_plan
        field_impact = self.mitigation_action.impact
        field_calculation_methodology = self.mitigation_action.calculation_methodology
        field_is_international = self.mitigation_action.is_international
        field_international_participation = self.mitigation_action.international_participation
        field_registration_type = self.mitigation_action.registration_type
        field_initiative = self.mitigation_action.initiative
        field_institution = self.mitigation_action.institution
        field_contact = self.mitigation_action.contact
        field_status = self.mitigation_action.status
        field_progress_indicator = self.mitigation_action.progress_indicator
        field_finance = self.mitigation_action.finance
        field_geographic_scale =self.mitigation_action.geographic_scale
        field_location = self.mitigation_action.location
        field_user = self.mitigation_action.user

        self.assertEqual(field_strategy_name, 'mitigation_action_strategy_name')
        self.assertEqual(field_name, 'mitigation_action_name')
        self.assertEqual(field_purpose, 'mitigation_action_purpose')
        self.assertEqual(field_start_date, datetime(2002, 10, 5, 18, 00))
        self.assertEqual(field_end_date, datetime(2003, 11, 6, 17, 12))
        self.assertEqual(field_gas_inventory, 'mitigation_action_gas')
        self.assertEqual(field_emissions_source, 'mitigation_action_emission_source')
        self.assertEqual(field_carbon_sinks, 'mitigation_action_carbon_sinks')
        self.assertEqual(field_impact_plan, 'mitigation_action_impact_plan')
        self.assertEqual(field_impact, 'mitigation_action_impact')
        self.assertEqual(field_calculation_methodology, 'mitigation_action_calculation_methodology')
        self.assertEqual(field_is_international, True)
        self.assertEqual(field_international_participation, 'mitigation_action_internation_participation')
        self.assertEqual(field_registration_type, self.registration_type)
        self.assertEqual(field_initiative, self.initiative)
        self.assertEqual(field_institution, self.institution)
        self.assertEqual(field_contact, self.contact)
        self.assertEqual(field_status, self.status)
        self.assertEqual(field_progress_indicator, self.progress_indicator)
        self.assertEqual(field_finance, self.finance)
        self.assertEqual(field_geographic_scale, self.geographic_scale)
        self.assertEqual(field_location, self.location)
        self.assertEqual(field_user, self.superUser)
      