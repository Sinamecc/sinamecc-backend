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

    
    def test_get_all_mitigation_action(self):
        pass