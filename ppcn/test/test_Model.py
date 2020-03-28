from django.test import TestCase, Client
from ppcn.models import *
from ppcn.serializers import *
from mitigation_action.models import Contact
from users.models import CustomUser
from django.contrib.auth.models import Group
from ppcn.services import PpcnService
import datetime

# initialize the APIClient app
client = Client() ## create tests with it 
ses_service = EmailServices()

class PPCNModelTest(TestCase):


    def setUp(self):
        self.superUser = CustomUser.objects.get_or_create(username='admin', is_superuser=True)[0]
        self.user = CustomUser.objects.get_or_create(username='test_user')[0]
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
        self.gei_organization = GeiOrganization.objects.create(ovv =self.ovv,  emission_ovv_date=datetime.datetime(2007, 1, 1), report_year=2019, base_year=2018)

        self.cantonal_gei_organization = GeiOrganization.objects.create(ovv =self.ovv,  emission_ovv_date=datetime.datetime(2007, 1, 1), report_year=2019, base_year=2018)

        self.organizational_gei_organization = GeiOrganization.objects.create(ovv =self.ovv,  emission_ovv_date=datetime.datetime(2007, 1, 1), report_year=2019, base_year=2018)

        self.cantonal_gei_organization.gei_activity_types.add(self.cantonal_gei_activity_type)
        self.organizational_gei_organization.gei_activity_types.add(self.organizational_gei_activity_type_1, self.organizational_gei_activity_type_2)

        self.ppcn_cantonal = PPCN.objects.create(user= self.superUser, organization=self.organization, geographic_level=self.cantonal_geographic_level, required_level=self.required_level, recognition_type=self.recognition_type, gei_organization=self.cantonal_gei_organization)

        self.ppcn_organizational = PPCN.objects.create(user= self.superUser, organization=self.organization, geographic_level=self.organizational_geographic_level, required_level=self.required_level, recognition_type=self.recognition_type, gei_organization=self.organizational_gei_organization)

        
    def test_organization(self):

        field_name = self.organization.name
        field_repr_name = self.organization.representative_name
        field_phone_org = self.organization.phone_organization
        field_postal_code = self.organization.postal_code
        field_fax = self.organization.fax
        field_address = self.organization.address
        field_contact = self.organization.contact
        field_ciiu = self.organization.ciiu

        self.assertEquals(field_name, 'organization-name')
        self.assertEquals(field_repr_name, 'representative-name')
        self.assertEquals(field_phone_org, '88888888')
        self.assertEquals(field_postal_code, '40101')
        self.assertEquals(field_fax, '88778877')
        self.assertEquals(field_address, 'address-testing')
        self.assertEquals(field_contact, self.contact)
        self.assertEquals(field_ciiu, 'CIIU-CODE')
    
    def test_contact(self):

        field_full_name = self.contact.full_name
        field_job_title = self.contact.job_title
        field_email = self.contact.email
        field_phone = self.contact.phone

        self.assertEquals(field_full_name, 'Test_full_name')
        self.assertEquals(field_job_title, 'Secretary')
        self.assertEquals(field_email, 'test@gmail.com')
        self.assertEquals(field_phone, '77777777')

    def test_geographic_level(self):
        field_level_es_cantonal = self.cantonal_geographic_level.level_es
        field_level_en_cantonal = self.cantonal_geographic_level.level_en
        field_level_es_organizational = self.organizational_geographic_level.level_es
        field_level_en_organizational = self.organizational_geographic_level.level_en

        self.assertEquals(field_level_es_cantonal, 'Cantonal')
        self.assertEquals(field_level_en_cantonal, 'Cantonal')
        self.assertEquals(field_level_es_organizational, 'Organizational')
        self.assertEquals(field_level_en_organizational, 'Organizacional')

    
    def test_sector(self):

        field_cantonal_sector_en = self.cantonal_sector.name_en
        field_cantonal_sector_es = self.cantonal_sector.name_es
        field_cantonal_geo_level = self.cantonal_sector.geographicLevel
        field_organizational_sector_en = self.organizational_sector.name_en
        field_organizational_sector_es = self.organizational_sector.name_es
        field_organizational_geo_level = self.organizational_sector.geographicLevel

        self.assertEquals(field_cantonal_sector_en, 'cantonal_sector_en')
        self.assertEquals(field_cantonal_sector_es, 'cantonal_sector_es')
        self.assertEquals(field_cantonal_geo_level, self.cantonal_geographic_level)
        self.assertEquals(field_organizational_sector_en, 'organizational_sector_en')
        self.assertEquals(field_organizational_sector_es, 'organizational_sector_es')
        self.assertEquals(field_organizational_geo_level, self.organizational_geographic_level)

    def test_sub_sector(self):
        field_cantonal_sub_sector_en = self.cantonal_sub_sector.name_en
        field_cantonal_sub_sector_es = self.cantonal_sub_sector.name_es
        field_cantonal_sector = self.cantonal_sub_sector.sector
        field_organizational_sub_sector_en = self.organizational_sub_sector.name_en
        field_organizational_sub_sector_es = self.organizational_sub_sector.name_es
        field_organizational_sector = self.organizational_sub_sector.sector

        self.assertEquals(field_cantonal_sub_sector_en, 'cantonal_sub_sector_en')
        self.assertEquals(field_cantonal_sub_sector_es, 'cantonal_sub_sector_es')
        self.assertEquals(field_cantonal_sector, self.cantonal_sector)
        self.assertEquals(field_organizational_sub_sector_en, 'organizational_sub_sector_en')
        self.assertEquals(field_organizational_sub_sector_es, 'organizational_sub_sector_es')
        self.assertEquals(field_organizational_sector, self.organizational_sector)
    
    def test_required_level(self):

        field_required_level_es = self.required_level.level_type_es
        field_required_level_en = self.required_level.level_type_en

        self.assertEquals(field_required_level_es, 'required_level_es')
        self.assertEquals(field_required_level_en, 'required_level_en')

    def test_recognition_type(self):
        field_recognition_type_es = self.recognition_type.recognition_type_es
        field_recognition_type_en = self.recognition_type.recognition_type_en

        self.assertEquals(field_recognition_type_es, 'recognition_type_es')
        self.assertEquals(field_recognition_type_en, 'recognition_type_en')


    def test_gei_organization(self):
        field_ovv = self.organizational_gei_organization.ovv
        field_emission_ovv_date = self.organizational_gei_organization.emission_ovv_date
        field_base_year = self.organizational_gei_organization.base_year
        field_report_year = self.organizational_gei_organization.report_year

        self.assertEquals(field_ovv, self.ovv)
        self.assertEquals(field_emission_ovv_date, datetime.datetime(2007, 1, 1))
        self.assertEquals(field_base_year, 2018)
        self.assertEquals(field_report_year, 2019)
        gei_activity_test = [self.organizational_gei_activity_type_1 , self.organizational_gei_activity_type_2]
        count = 0
        for gei_activity in self.organizational_gei_organization.gei_activity_types.all():
            self.assertEquals(gei_activity, gei_activity_test[count])
            count += 1
        

    def test_ppcn_national(self):
        field_user = self.ppcn_organizational.user
        field_organization = self.ppcn_organizational.organization
        field_geographic_level = self.ppcn_organizational.geographic_level
        field_required_level = self.ppcn_organizational.required_level
        field_recognition_type = self.ppcn_organizational.recognition_type
        field_gei_organization = self.ppcn_organizational.gei_organization

        self.assertEquals(field_user, self.superUser)
        self.assertEquals(field_organization, self.organization)
        self.assertEquals(field_geographic_level, self.organizational_geographic_level)
        self.assertEquals(field_required_level, self.required_level)
        self.assertEquals(field_recognition_type, self.recognition_type)
        self.assertEquals(field_gei_organization, self.organizational_gei_organization)
        
        
    def test_ppcn_cantonal(self):
        field_user = self.ppcn_cantonal.user
        field_organization = self.ppcn_cantonal.organization
        field_geographic_level = self.ppcn_cantonal.geographic_level
        field_required_level = self.ppcn_cantonal.required_level
        field_recognition_type = self.ppcn_cantonal.recognition_type
        field_gei_organization = self.ppcn_cantonal.gei_organization

        self.assertEquals(field_user, self.superUser)
        self.assertEquals(field_organization, self.organization)
        self.assertEquals(field_geographic_level, self.cantonal_geographic_level)
        self.assertEquals(field_required_level, self.required_level)
        self.assertEquals(field_recognition_type, self.recognition_type)
        self.assertEquals(field_gei_organization, self.cantonal_gei_organization)

