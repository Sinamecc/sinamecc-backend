from django.test import TestCase, Client
from adaptation_action.models import *
from adaptation_action.serializers import *
from users.models import CustomUser
from general.models import District, Canton
from django.urls import reverse
from rest_framework import status

client = Client()

class AdaptationActionTest(TestCase):

    def setUp(self):
        self.superUser = CustomUser.objects.get_or_create(username='admin', is_superuser=True, email='sinamec@grupoincocr.com')[0]
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]

        self.report_organization_type = ReportOrganizationType.objects.get(id=1)
        self.contact = Contact.objects.create(contact_name='contact_name_test', contact_position='contact_position_test', email='contact_email_test', phone='contact_phone_test',
            address='contact_address_test', institution='contact_institution_test', user=self.superUser)
        self.report_organization = ReportOrganization.objects.create(responsible_entity='responsible_entity_test', legal_identification='404440444', elaboration_date='2022-11-10',
            entity_address='entity_address_test', report_organization_type=self.report_organization_type, other_report_organization_type='other_report_organization_type_test', contact=self.contact)
        self.adaptation_action_type = AdaptationActionType.objects.get(id=1)
        self.ODS = [ODS.objects.get(id=1)]
        self.adaptation_action_information = AdaptationActionInformation.objects.create(name='name_test', objective='objetive_test', description='description_test', meta='meta_test',
            adaptation_action_type=self.adaptation_action_type)
        self.adaptation_action_information.ods.set(self.ODS)
        self.districts = [District.objects.get(id=1), District.objects.get(id=2)]
        self.canton = [Canton.objects.get(id=1), Canton.objects.get(id=2)]
        self.address = Address.objects.create(app_scale=1, description="description_test", GIS="gis_test")
        self.address.district.set(self.districts)
        self.address.canton.set(self.canton)
        self.activity = [Activity.objects.get(id=1)]
        self.instrument = Instrument.objects.create(name="name_test")
        self.type_climated_threat = [TypeClimateThreat.objects.get(id=3)]
        self.climate_threat = ClimateThreat.objects.create(other_type_climate_threat="other type climate threat test", description_climate_threat="description climate threat test",
            vulnerability_climate_threat="vulnerability climate threat test", exposed_elements="exposed elements test")
        self.climate_threat.type_climate_threat.set(self.type_climated_threat)
        self.implementation = Implementation.objects.create(start_date="2022-07-07", end_date="2022-07-14", responsible_entity="responsible entity test", other_entity="other entity test", action_code="AA0")
        self.status = FinanceStatus.objects.create(code=1, name="name test")
        self.mideplan = Mideplan.objects.create(registry="02", name="name test", entity="entity test")
        self.source = [FinanceSourceType.objects.get(id=1), FinanceSourceType.objects.get(id=2)]
        self.finance_instrument = [FinanceInstrument.objects.get(id=1), FinanceInstrument.objects.get(id=2)]
        self.finance = FinanceAdaptation.objects.create(administration="administration test", budget="20000", year="1999", status=self.status, mideplan = self.mideplan, instrument_name="instrument name test")
        self.finance.source.set(self.source)
        self.finance.finance_instrument.set(self.finance_instrument)
        
        self.adaptation_action = AdaptationAction.objects.create(user=self.user, report_organization=self.report_organization, address=self.address, adaptation_action_information=self.adaptation_action_information,
            instrument=self.instrument, climate_threat=self.climate_threat, implementation=self.implementation, finance=self.finance)
        self.adaptation_action.activity.set(self.activity)


    def test_get_all_adaptation_action(self):
        client.force_login(self.superUser)
        response = client.get(reverse('get_post_adaptation_action'))
        response_data = response.data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)