from django.test import TestCase, Client
from ppcn.models import *
from ppcn.serializers import *
from mitigation_action.models import Contact
from users.models import CustomUser
from django.contrib.auth.models import Group
from ppcn.services import PpcnService
from django.urls import reverse
from rest_framework import status
import datetime as dt, json
from datetime import datetime

# initialize the APIClient app
client = Client() ## create tests with it 
ses_service = EmailServices()

class PPCNFormTest(TestCase):

    def setUp(self):
        self.superUser = CustomUser.objects.get_or_create(username='admin', is_superuser=True, email='sinamec@grupoincocr.com')[0]
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]
        self.ppcn_service = PpcnService()
        self.contact = Contact.objects.create(full_name='Test_full_name', job_title='Secretary', email='test@gmail.com', phone='77777777')
        self.organization = Organization.objects.create(name='organization-name', legal_identification='303030303012', representative_legal_identification='404040404021',
        representative_name='representative-name', phone_organization = '88888888', postal_code='40101', fax='88778877', address='address-testing', contact = self.contact)
        
        self.ciiu_code_1 = CIIUCode.objects.create(ciiu_code='CODETEST_1', organization=self.organization)
        self.ciiu_code_2 = CIIUCode.objects.create(ciiu_code='CODETEST_2', organization=self.organization)
        self.ciiu_code_list = [self.ciiu_code_1, self.ciiu_code_2]

        self.required_level = RequiredLevel.objects.create(level_type_es= 'required_level_es', level_type_en= 'required_level_en')
        self.recognition_type = RecognitionType.objects.create( recognition_type_es='recognition_type_es', recognition_type_en='recognition_type_en')
        self.organization_classification = OrganizationClassification.objects.create(emission_quantity=1000, buildings_number=10000, data_inventory_quantity=1000, required_level=self.required_level
                                                                    ,recognition_type=self.recognition_type)



        self.cantonal_geographic_level = GeographicLevel.objects.create(level_es='Cantonal', level_en='Cantonal')
        self.organizational_geographic_level = GeographicLevel.objects.create(level_es='Organizational', level_en='Organizacional')
    
        self.cantonal_sector = Sector.objects.create(name_en='cantonal_sector_en', name_es='cantonal_sector_es', geographicLevel=self.cantonal_geographic_level)
        self.organizational_sector = Sector.objects.create(name_en='organizational_sector_en', name_es='organizational_sector_es', geographicLevel=self.organizational_geographic_level)
        self.cantonal_sub_sector = SubSector.objects.create(name_es='cantonal_sub_sector_es', name_en='cantonal_sub_sector_en', sector=self.cantonal_sector)
        self.organizational_sub_sector = SubSector.objects.create(name_es='organizational_sub_sector_es', name_en='organizational_sub_sector_en', sector=self.organizational_sector)

        
        self.ovv = OVV.objects.create(name='name_ovv', email='ovv@fake.com', phone='22332233')
        self.gei_organization = GeiOrganization.objects.create(ovv =self.ovv,  emission_ovv_date=dt.date(2007, 1, 1), report_year=2019, base_year=2018)

        self.cantonal_gei_organization = GeiOrganization.objects.create(ovv =self.ovv,  emission_ovv_date=dt.date(2007, 1, 1), report_year=2019, base_year=2018)

        self.organizational_gei_organization = GeiOrganization.objects.create(ovv =self.ovv,  emission_ovv_date=dt.date(2007, 1, 1), report_year=2019, base_year=2018)
        
        self.cantonal_gei_activity_type = GeiActivityType.objects.create(gei_organization=self.cantonal_gei_organization, activity_type='activity_type', sub_sector=self.cantonal_sub_sector, sector=self.cantonal_sector)
        self.organizational_gei_activity_type_1 = GeiActivityType.objects.create(gei_organization=self.organizational_gei_organization, activity_type='activity_type', sub_sector=self.organizational_sub_sector, sector=self.organizational_sector)
        self.organizational_gei_activity_type_2 = GeiActivityType.objects.create(gei_organization=self.organizational_gei_organization, activity_type='activity_type', sub_sector=self.organizational_sub_sector, sector=self.organizational_sector)

        self.ppcn_cantonal = PPCN.objects.create(user= self.superUser, confidential= 'confidential', organization=self.organization, geographic_level=self.cantonal_geographic_level, 
                                                    gei_organization=self.cantonal_gei_organization, organization_classification= self.organization_classification)

        self.ppcn_organizational = PPCN.objects.create(user= self.superUser, confidential='partially_confidential', confidential_fields="test - field", organization=self.organization,
                                                    organization_classification= self.organization_classification, geographic_level=self.organizational_geographic_level, gei_organization=self.organizational_gei_organization)

        self.ppcn_data = {
            "confidential": 'no_confidential',
            "organization" : 
            {	
                "name": "test name",
                "representative_name": "test representative_name",
                "representative_legal_identification": "3000300012",
                "legal_identification": "3000300012",
                "phone_organization" : "27643606",
                "postal_code": "40101",
                "fax": "",
                "ciiu_code_list": [
                    {"ciiu_code":"test ciiu"}, 
                    {"ciiu_code":"test ciiu 2"}
                ],
                "address": "test address",
                "contact": 
                {
        
                    "full_name": "test full_name",
                    "job_title": "test_update job_tiqtle",
                    "email": "test2@email.com", 
                    "phone": "27643636"
                }
                
            },
            "organization_classification":
            {
                'emission_quantity': 100000,
                'buildings_number': 10000,
                'data_inventory_quantity': 1000,
                'required_level': self.required_level.id,
                'recognition_type': self.recognition_type.id,
                "reduction" :[{
                    "proyect": "test",
                    "activity": "Test activity",
                    "detail_reduction": "test reduction detail", 
                    "emission": "10000", 
                    "total_emission": "10000", 
                    "investment": "1000000", 
                    "investment_currency": "USD", 
                    "total_investment": "10000", 
                    "total_investment_currency": "CRC"
                }],
                "carbon_offset":
                [{
                    "offset_scheme" : "UCC", 
                    "project_location" : "Project Location", 
                    "certificate_identification" : "CRSD-123214", 
                    "total_carbon_offset" : "80000 carbon OFFSET", 
                    "offset_cost" : "5000", 
                    "offset_cost_currency" : "USD", 
                    "period" : "May period", 
                    "total_offset_cost" : "5000", 
                    "total_offset_cost_currency":"CRC"
                }]
            },
            "gei_organization":
            {	
                "ovv":1,
                "emission_ovv_date":"2018-04-14",
                "report_year":"2018",
                "base_year":"2018",
                "gas_report":{
                    "other_gases": "test gases test gases",
                    "biogenic_emission": {

                        "total": "3323323",
                        "scope_1": "scope 1",
                        "scope_2": "scope 2"
                    },
                    "cost_ghg_inventory":3030303,
                    "cost_ghg_inventory_currency":"CRC",
                    "cost_ovv_process":3030303,
                    "cost_ovv_process_currency":"USD"
                },
                "gei_activity_types":[
                    {
                        "activity_type": "activity type test 1",
                        "sub_sector":self.organizational_sub_sector.id,
                        "sector":self.organizational_sector.id
                    },
                    {
                        "activity_type": "activity type test 2",
                        "sub_sector":self.organizational_sub_sector.id,
                        "sector":self.organizational_sector.id
                    }
                ],
            },
            
            "geographic_level": self.organizational_geographic_level.id,
            "required_level":self.required_level.id, 
            "recognition_type":self.recognition_type.id,
            "user":self.superUser.id
        }

    ## GET ENDPOITNS
    def test_get_all_ppcn(self):
        client.force_login(self.superUser)
        response = client.get(reverse('get_post_ppcn'), kwargs={'language':'en'})
        response_data = response.data
        serialized_ppcn = PPCNSerializer(PPCN.objects.all(), many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(len(serialized_ppcn)):
            self.assertEquals(serialized_ppcn[i].get('id'), response_data[i].get('id'))
            self.assertEquals(serialized_ppcn[i].get('confidential'), response_data[i].get('confidential'))
            self.assertEquals(serialized_ppcn[i].get('confidential_fields'), response_data[i].get('confidential_fields'))
            ## organization level
            organization = OrganizationSerializer(Organization.objects.get(id=serialized_ppcn[i].get('organization'))).data
            self.assertEqual(str(response_data[i].get('organization').get('id')), str(organization.get('id')))
            self.assertEqual(str(response_data[i].get('organization').get('name')), str(organization.get('name')))
            self.assertEqual(str(response_data[i].get('organization').get('legal_identification')), str(organization.get('legal_identification')))
            self.assertEqual(str(response_data[i].get('organization').get('representative_name')), str(organization.get('representative_name')))
            self.assertEqual(str(response_data[i].get('organization').get('representative_legal_identification')), str(organization.get('representative_legal_identification')))
            self.assertEqual(str(response_data[i].get('organization').get('phone_organization')), str(organization.get('phone_organization')))
            self.assertEqual(str(response_data[i].get('organization').get('postal_code')), str(organization.get('postal_code')))
            self.assertEqual(str(response_data[i].get('organization').get('fax')), str(organization.get('fax')))
            self.assertEqual(str(response_data[i].get('organization').get('address')), str(organization.get('address')))
            
            ciiu_code_list = CIIUCodeSerializer(CIIUCode.objects.filter(organization__id=organization.get('id')).all(), many=True).data
            for ciiu_code_request, ciiu_code_test in zip(response_data[i].get('organization').get('ciiu_code'), ciiu_code_list):
                self.assertEquals(str(ciiu_code_test.get('id')), str(ciiu_code_request.get('id')))
                self.assertEquals(str(ciiu_code_test.get('ciiu_code')), str(ciiu_code_request.get('ciiu_code')))
                self.assertEquals(str(ciiu_code_test.get('organization')), str(ciiu_code_request.get('organization')))


            contact = ContactSerializer(Contact.objects.get(id=organization.get('contact'))).data
            self.assertEqual(str(response_data[i].get('organization').get('contact').get('id')), str(contact.get('id')))
            self.assertEqual(str(response_data[i].get('organization').get('contact').get('full_name')), str(contact.get('full_name')))
            self.assertEqual(str(response_data[i].get('organization').get('contact').get('job_title')), str(contact.get('job_title')))
            self.assertEqual(str(response_data[i].get('organization').get('contact').get('email')), str(contact.get('email')))
            self.assertEqual(str(response_data[i].get('organization').get('contact').get('phone')), str(contact.get('phone')))

            self.assertEqual(str(response_data[i].get('base_year')), str(serialized_ppcn[i].get('base_year')))
            self.assertEqual(str(response_data[i].get('fsm_state')), str(serialized_ppcn[i].get('fsm_state')))

            datetime_create_response = datetime.strptime(str(response_data[i].get('created')), '%Y-%m-%dT%H:%M:%S.%fZ')
            datetime_create_serializer = datetime.strptime(str(serialized_ppcn[i].get('created')), '%Y-%m-%dT%H:%M:%S.%fZ')
            self.assertEqual(datetime_create_response, datetime_create_serializer)

            datetime_updated_response = datetime.strptime(str(response_data[i].get('updated')), '%Y-%m-%dT%H:%M:%S.%fZ')
            datetime_updated_serializer = datetime.strptime(str(serialized_ppcn[i].get('updated')), '%Y-%m-%dT%H:%M:%S.%fZ')
            self.assertEqual(datetime_updated_response, datetime_updated_serializer)


    def test_get_ppcn_organizational(self):

        client.force_login(self.superUser)
        response = client.get(reverse('get_one_ppcn', args=[self.ppcn_organizational.id, 'en']))
        data = response.data
        organization_data = data.get('organization')
        gei_organization = data.get('gei_organization')

        self.assertEquals(data.get('id'), self.ppcn_organizational.id)
        self.assertEquals(data.get('user'), self.superUser.id)
        self.assertEquals(data.get('confidential'), 'partially_confidential')

        
        ## organization
        self.assertEquals(organization_data.get('id'), self.organization.id)
        self.assertEquals(organization_data.get('name'), self.organization.name)
        self.assertEquals(organization_data.get('legal_identification'), self.organization.legal_identification)
        self.assertEquals(organization_data.get('representative_name'), self.organization.representative_name)
        self.assertEquals(organization_data.get('representative_legal_identification'), self.organization.representative_legal_identification)
        self.assertEquals(organization_data.get('phone_organization'), self.organization.phone_organization)
        self.assertEquals(organization_data.get('postal_code'), self.organization.postal_code)
        self.assertEquals(organization_data.get('fax'), self.organization.fax)
        self.assertEquals(organization_data.get('address'), self.organization.address)
        self.assertEquals(len(organization_data.get('ciiu_code')), len(self.ciiu_code_list))

        ciiu_code_list_request = sorted(organization_data.get('ciiu_code'), key = lambda i: i['id'])
        ciiu_code_list_test = sorted(self.ciiu_code_list, key = lambda i: i.id)

        for ciiu_code_request, ciiu_code_test in zip(ciiu_code_list_request, ciiu_code_list_test):
            self.assertEquals(ciiu_code_test.id, ciiu_code_request.get('id'))
            self.assertEquals(ciiu_code_test.ciiu_code, ciiu_code_request.get('ciiu_code'))
            self.assertEquals(ciiu_code_test.organization.id, ciiu_code_request.get('organization'))

        ## organiztion ->contact
        self.assertEquals(organization_data.get('contact').get('id'), self.contact.id)
        self.assertEquals(organization_data.get('contact').get('full_name'), self.contact.full_name)
        self.assertEquals(organization_data.get('contact').get('job_title'), self.contact.job_title)
        self.assertEquals(organization_data.get('contact').get('email'), self.contact.email)
        self.assertEquals(organization_data.get('contact').get('phone'), self.contact.phone)

        ## catalogs
        ## geographic_level
        self.assertEquals(data.get('geographic_level').get('id'), self.organizational_geographic_level.id)
        self.assertEquals(data.get('geographic_level').get('level'), self.organizational_geographic_level.level_en) 


        ## gei_organization
        self.assertEquals(gei_organization.get('id'), self.organizational_gei_organization.id)
        self.assertEquals(datetime.strptime(str(gei_organization.get('emission_ovv_date')), '%Y-%m-%d').date(), self.organizational_gei_organization.emission_ovv_date)
        self.assertEquals(gei_organization.get('report_year'), 2019)
        self.assertEquals(gei_organization.get('base_year'), 2018)

        ## gei_organization - ovv
        self.assertEquals(gei_organization.get('ovv').get('id'), self.organizational_gei_organization.ovv.id)
        self.assertEquals(gei_organization.get('ovv').get('name'), self.organizational_gei_organization.ovv.name)
        self.assertEquals(gei_organization.get('ovv').get('email'), self.organizational_gei_organization.ovv.email)
        
        ## gei_organization_ gei_activity_types
        gei_activity_1 = self.organizational_gei_organization.gei_activity_type.all()[0]
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('id'), gei_activity_1.id)
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('activity_type'), gei_activity_1.activity_type)

        ## gei_organization[0] - sector
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('sector').get('id'), gei_activity_1.sector.id)
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('sector').get('name'), gei_activity_1.sector.name_en)

        ## gei_organization[0] - subsector
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('sub_sector').get('id'), gei_activity_1.sub_sector.id)
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('sub_sector').get('name'), gei_activity_1.sub_sector.name_en)
        

        ## gei_organization_ gei_activity_types
        gei_activity_2 = self.organizational_gei_organization.gei_activity_type.all()[1]
        self.assertEquals(gei_organization.get('gei_activity_type')[1].get('id'), gei_activity_2.id)
        self.assertEquals(gei_organization.get('gei_activity_type')[1].get('activity_type'), gei_activity_2.activity_type)

        ## gei_organization[1] - sector
        self.assertEquals(gei_organization.get('gei_activity_type')[1].get('sector').get('id'), gei_activity_2.sector.id)
        self.assertEquals(gei_organization.get('gei_activity_type')[1].get('sector').get('name'), gei_activity_2.sector.name_en)

        ## gei_organization[1] - subsector
        self.assertEquals(gei_organization.get('gei_activity_type')[1].get('sub_sector').get('id'), gei_activity_2.sub_sector.id)
        self.assertEquals(gei_organization.get('gei_activity_type')[1].get('sub_sector').get('name'), gei_activity_2.sub_sector.name_en)


        
    def test_get_ppcn_cantonal(self):
        client.force_login(self.superUser)
        response = client.get(reverse('get_one_ppcn', args=[self.ppcn_cantonal.id, 'en']))

        data = response.data
       
        organization_data = data.get('organization')
        gei_organization = data.get('gei_organization')

        self.assertEquals(data.get('id'), self.ppcn_cantonal.id)
        self.assertEquals(data.get('user'), self.superUser.id)
        self.assertEquals(data.get('confidential'), 'confidential')
        
        ## organization
        self.assertEquals(organization_data.get('id'), self.organization.id)
        self.assertEquals(organization_data.get('name'), self.organization.name)
        self.assertEquals(organization_data.get('legal_identification'), self.organization.legal_identification)
        self.assertEquals(organization_data.get('representative_name'), self.organization.representative_name)
        self.assertEquals(organization_data.get('representative_legal_identification'), self.organization.representative_legal_identification)
        self.assertEquals(organization_data.get('phone_organization'), self.organization.phone_organization)
        self.assertEquals(organization_data.get('postal_code'), self.organization.postal_code)
        self.assertEquals(organization_data.get('fax'), self.organization.fax)
        self.assertEquals(organization_data.get('address'), self.organization.address)
        self.assertEquals(len(organization_data.get('ciiu_code')), len(self.ciiu_code_list))

        ciiu_code_list_request = sorted(organization_data.get('ciiu_code'), key = lambda i: i['id'])
        ciiu_code_list_test = sorted(self.ciiu_code_list, key = lambda i: i.id)

        for ciiu_code_request, ciiu_code_test in zip(ciiu_code_list_request, ciiu_code_list_test):
            self.assertEquals(ciiu_code_test.id, ciiu_code_request.get('id'))
            self.assertEquals(ciiu_code_test.ciiu_code, ciiu_code_request.get('ciiu_code'))
            self.assertEquals(ciiu_code_test.organization.id, ciiu_code_request.get('organization'))

        ## organiztion ->contact
        self.assertEquals(organization_data.get('contact').get('id'), self.contact.id)
        self.assertEquals(organization_data.get('contact').get('full_name'), self.contact.full_name)
        self.assertEquals(organization_data.get('contact').get('job_title'), self.contact.job_title)
        self.assertEquals(organization_data.get('contact').get('email'), self.contact.email)
        self.assertEquals(organization_data.get('contact').get('phone'), self.contact.phone)

        ## catalogs
        ## geographic_level
        self.assertEquals(data.get('geographic_level').get('id'), self.cantonal_geographic_level.id)
        self.assertEquals(data.get('geographic_level').get('level'), self.cantonal_geographic_level.level_en) 


        ## gei_organization
        self.assertEquals(gei_organization.get('id'), self.cantonal_gei_organization.id)
        self.assertEquals(datetime.strptime(str(gei_organization.get('emission_ovv_date')), '%Y-%m-%d').date(), self.organizational_gei_organization.emission_ovv_date)
        self.assertEquals(gei_organization.get('report_year'), self.cantonal_gei_organization.report_year)
        self.assertEquals(gei_organization.get('base_year'), self.cantonal_gei_organization.base_year)

        ## gei_organization - ovv
        self.assertEquals(gei_organization.get('ovv').get('id'), self.organizational_gei_organization.ovv.id)
        self.assertEquals(gei_organization.get('ovv').get('name'), self.organizational_gei_organization.ovv.name)
        self.assertEquals(gei_organization.get('ovv').get('email'), self.organizational_gei_organization.ovv.email)
        
        ## gei_organization_ gei_activity_types
        gei_activity_1 = self.cantonal_gei_organization.gei_activity_type.all()[0]
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('id'), gei_activity_1.id)
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('activity_type'), gei_activity_1.activity_type)

        ## gei_organization[0] - sector
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('sector').get('id'), gei_activity_1.sector.id)
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('sector').get('name'), gei_activity_1.sector.name_en)

        ## gei_organization[0] - subsector
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('sub_sector').get('id'), gei_activity_1.sub_sector.id)
        self.assertEquals(gei_organization.get('gei_activity_type')[0].get('sub_sector').get('name'), gei_activity_1.sub_sector.name_en)
        

    ## POST ENDPOINTS

    def test_get_post_ppcn(self):
        client.force_login(self.superUser)
        response = client.post(
            reverse('get_post_ppcn', kwargs={'language': 'en'}),
            data=json.dumps(self.ppcn_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED )
