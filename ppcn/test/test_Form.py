from django.test import TestCase, Client
from ppcn.models import *
from ppcn.serializers import *
from mitigation_action.models import Contact
from users.models import CustomUser
from django.contrib.auth.models import Group
from ppcn.services import PpcnService
from django.urls import reverse
import datetime

# initialize the APIClient app
client = Client() ## create tests with it 
ses_service = EmailServices()

class PPCNFormTest(TestCase):


    def setUp(self):
        self.superUser = CustomUser.objects.get_or_create(username='admin', is_superuser=True)[0]
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]
        self.group_list = Group.objects.filter(name__in=['dcc_ppcn_responsible', 'dcc_executive_secretary', 'ppcn_responsible']).all()
        client.force_login(self.user)
        self.ppcn_service = PpcnService()

        self.contact = Contact.objects.create(full_name='Test_full_name', job_title='Secretary', email='test@gmail.com', phone='77777777')
        self.organization = Organization.objects.create(name='organization-name', representative_name='representative-name',
        phone_organization = '88888888', postal_code='40101', fax='88778877', address='address-testing', 
        contact = self.contact, ciiu = 'CIIU-CODE')

        self.required_level = RequiredLevel.objects.create(level_type_es= 'required_level_es', level_type_en= 'required_level_en')
        self.recognition_type = RecognitionType.objects.create( recognition_type_es='recognition_type_es', recognition_type_en='recognition_type_en')

        self.cantonal_geographic_level = GeographicLevel.objects.create(level_es='Cantonal', level_en='Cantonal')
        self.organizational_geographic_level = GeographicLevel.objects.create(level_es='Organizational', level_en='Organizacional')

        self.cantonal_sector = Sector.objects.create(name_en='cantonal_sector_en', name_es='cantonal_sector_es', geographicLevel=self.cantonal_geographic_level)
        self.organizational_sector = Sector.objects.create(name_en='organizational_sector_en', name_es='organizational_sector_es', geographicLevel=self.organizational_geographic_level)
        self.cantonal_sub_sector = SubSector.objects.create(name_es='cantonal_sub_sector_es', name_en='cantonal_sub_sector_en', sector=self.cantonal_sector)
        self.organizational_sub_sector = SubSector.objects.create(name_es='organizational_sub_sector_es', name_en='organizational_sub_sector_en', sector=self.organizational_sector)

        self.cantonal_gei_activity_type = GeiActivityType.objects.create(activity_type='activity_type', sub_sector=self.cantonal_sub_sector, sector=self.cantonal_sector)
        self.organizational_gei_activity_type_1 = GeiActivityType.objects.create(activity_type='activity_type', sub_sector=self.organizational_sub_sector, sector=self.organizational_sector)
        self.organizational_gei_activity_type_2 = GeiActivityType.objects.create(activity_type='activity_type', sub_sector=self.organizational_sub_sector, sector=self.organizational_sector)

        self.ovv = OVV.objects.create(name='name_ovv', email='ovv@fake.com', phone='22332233')
        self.gei_organization = GeiOrganization.objects.create(ovv =self.ovv,  emission_ovv_date=datetime.date(2007, 1, 1), report_year=2019, base_year=2018)

        self.cantonal_gei_organization = GeiOrganization.objects.create(ovv =self.ovv,  emission_ovv_date=datetime.date(2007, 1, 1), report_year=2019, base_year=2018)

        self.organizational_gei_organization = GeiOrganization.objects.create(ovv =self.ovv,  emission_ovv_date=datetime.date(2007, 1, 1), report_year=2019, base_year=2018)

        self.cantonal_gei_organization.gei_activity_types.add(self.cantonal_gei_activity_type)
        self.organizational_gei_organization.gei_activity_types.add(self.organizational_gei_activity_type_1, self.organizational_gei_activity_type_2)

        self.ppcn_cantonal = PPCN.objects.create(user= self.superUser, organization=self.organization, geographic_level=self.cantonal_geographic_level, required_level=self.required_level, recognition_type=self.recognition_type, gei_organization=self.cantonal_gei_organization)

        self.ppcn_organizational = PPCN.objects.create(user= self.superUser, organization=self.organization, geographic_level=self.organizational_geographic_level, required_level=self.required_level, recognition_type=self.recognition_type, gei_organization=self.organizational_gei_organization)

    
    
    
    
    def test_get_ppcn_national(self):

        client.force_login(self.superUser)
        response = client.get(reverse('get_one_ppcn', args=[self.ppcn_organizational.id, 'en']))
        data = response.data
        organization_data = data.get('organization')
        gei_organization = data.get('gei_organization')

        self.assertEquals(data.get('id'), self.ppcn_organizational.id)
        self.assertEquals(data.get('user'), self.superUser.id)
        
        ## organization
        self.assertEquals(organization_data.get('id'), self.organization.id)
        self.assertEquals(organization_data.get('name'), self.organization.name)
        self.assertEquals(organization_data.get('representative_name'), self.organization.representative_name)
        self.assertEquals(organization_data.get('phone_organization'), self.organization.phone_organization)
        self.assertEquals(organization_data.get('postal_code'), self.organization.postal_code)
        self.assertEquals(organization_data.get('fax'), self.organization.fax)
        self.assertEquals(organization_data.get('address'), self.organization.address)
        self.assertEquals(organization_data.get('ciiu'), self.organization.ciiu)

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

        ## required_level
        self.assertEquals(data.get('required_level').get('id'), self.required_level.id)
        self.assertEquals(data.get('required_level').get('level_type'), self.required_level.level_type_en)

        ## recognition_type
        self.assertEquals(data.get('recognition_type').get('id'), self.recognition_type.id)
        self.assertEquals(data.get('recognition_type').get('recognition_type'), self.recognition_type.recognition_type_en)

        ## gei_organization
        self.assertEquals(gei_organization.get('id'), self.organizational_gei_organization.id)
        self.assertEquals(gei_organization.get('emission_ovv_date'), datetime.date(2007, 1, 1))
        self.assertEquals(gei_organization.get('report_year'), 2019)
        self.assertEquals(gei_organization.get('base_year'), 2018)

        ## gei_organization - ovv
        self.assertEquals(gei_organization.get('ovv').get('id'), self.organizational_gei_organization.ovv.id)
        self.assertEquals(gei_organization.get('ovv').get('name'), self.organizational_gei_organization.ovv.name)
        self.assertEquals(gei_organization.get('ovv').get('email'), self.organizational_gei_organization.ovv.email)
        
        ## gei_organization_ gei_activity_types
        gei_activity_1 = self.organizational_gei_organization.gei_activity_types.all()[0]
        self.assertEquals(gei_organization.get('gei_activity_types')[0].get('id'), gei_activity_1.id)
        self.assertEquals(gei_organization.get('gei_activity_types')[0].get('activity_type'), gei_activity_1.activity_type)

        ## gei_organization[0] - sector
        self.assertEquals(gei_organization.get('gei_activity_types')[0].get('sector').get('id'), gei_activity_1.sector.id)
        self.assertEquals(gei_organization.get('gei_activity_types')[0].get('sector').get('name'), gei_activity_1.sector.name_en)

        ## gei_organization[0] - subsector
        self.assertEquals(gei_organization.get('gei_activity_types')[0].get('sub_sector').get('id'), gei_activity_1.sub_sector.id)
        self.assertEquals(gei_organization.get('gei_activity_types')[0].get('sub_sector').get('name'), gei_activity_1.sub_sector.name_en)
        

        ## gei_organization_ gei_activity_types
        gei_activity_2 = self.organizational_gei_organization.gei_activity_types.all()[1]
        self.assertEquals(gei_organization.get('gei_activity_types')[1].get('id'), gei_activity_2.id)
        self.assertEquals(gei_organization.get('gei_activity_types')[1].get('activity_type'), gei_activity_2.activity_type)

        ## gei_organization[1] - sector
        self.assertEquals(gei_organization.get('gei_activity_types')[1].get('sector').get('id'), gei_activity_2.sector.id)
        self.assertEquals(gei_organization.get('gei_activity_types')[1].get('sector').get('name'), gei_activity_2.sector.name_en)

        ## gei_organization[1] - subsector
        self.assertEquals(gei_organization.get('gei_activity_types')[1].get('sub_sector').get('id'), gei_activity_2.sub_sector.id)
        self.assertEquals(gei_organization.get('gei_activity_types')[1].get('sub_sector').get('name'), gei_activity_2.sub_sector.name_en)


        
    def test_get_ppcn_cantonal(self):
        pass
    
