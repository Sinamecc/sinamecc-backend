from django.test import TestCase, Client
from django.utils import timezone
from rest_framework import status
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth.models import Group
from mitigation_action.services import MitigationActionService

import json
import uuid
import datetime 
from datetime import datetime
from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, FinanceSourceType, Finance, IngeiCompliance, GeographicScale, Location, Mitigation, ChangeLog
from mitigation_action.serializers import RegistrationTypeSerializer, ContactSerializer, StatusSerializer, ProgressIndicatorSerializer, FinanceSourceTypeSerializer, FinanceSerializer, IngeiComplianceSerializer, GeographicScaleSerializer, LocationSerializer, MitigationSerializer
from workflow.models import Comment, ReviewStatus

# initialize the APIClient app
client = Client()


class MitigationActionFormTest(TestCase):

    def setUp(self):
        user = User.objects.get_or_create(username='admin', is_superuser=True)[0]
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