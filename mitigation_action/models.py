from __future__ import unicode_literals
from django.db.models import manager

from django.db.models.fields import BLANK_CHOICE_DASH, CharField, related
from django.db.models.query import QuerySet
from rest_framework import fields
from users.serializers import NewCustomUserSerializer
from django.conf import settings

import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from workflow.models import Comment, ReviewStatus
from general.storages import PrivateMediaStorage
from django_fsm import FSMField, transition
from general.services import EmailServices
from mitigation_action.email_services import MitigationActionEmailServices
from general.services import EmailServices
from general.permissions import PermissionsHelper
from general.helpers.validators import validate_year
from time import gmtime, strftime



User =  get_user_model()
permission = PermissionsHelper()
##Email services, default email -> sinamec@grupoincocr.com
ses_service = EmailServices()

CURRENCIES = (('CRC', _('Costa Rican colon')), ('USD', _('United States dollar')))
##
## Start Catalogs
##
def directory_path(instance, filename): 
    path = "mitigation_action/{0}/{1}/{2}/"

    return path.format(instance._meta.verbose_name, strftime("%Y%m%d", gmtime()), filename)


class CarbonDeposit(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    ##logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Carbon Deposit')
        verbose_name_plural = _('Carbon Deposits')


class Standard(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    ##logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Standar')
        verbose_name_plural = _('Standars')


class SustainableDevelopmentGoals(models.Model): 
    code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Sustainable Development Goal")
        verbose_name_plural = _("Sustainable Development Goals")


class GHGImpactSector(models.Model):

    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("GHG Impact Sector")
        verbose_name_plural = _("GHG Impact Sectors")


class ActionAreas(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(max_length=3, null=False, blank=False)
    
    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Action Area')
        verbose_name_plural = _('Action Areas')


class ActionGoals(models.Model):

    goal = models.TextField()
    code = models.CharField(max_length=3, null=False, blank=False)
    area = models.ForeignKey(ActionAreas, null=False, related_name='goal', on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Action Goal')
        verbose_name_plural = _('Action Goals')


class DescarbonizationAxis(models.Model):

    code = models.CharField(max_length=3, null=False, blank=False)
    description = models.TextField()

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Descarbonization Axis')
        verbose_name_plural = _('Descarbonization Axes')


class TransformationalVisions(models.Model):

    code = models.CharField(max_length=3, null=False, blank=False)
    description = models.TextField()
    axis = models.ForeignKey(DescarbonizationAxis, null=False, related_name='transformational_vision', on_delete=models.CASCADE)
    
    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Transformational Vision')
        verbose_name_plural = _('Transformational Visions')


class Topics(models.Model):

    code = models.CharField(max_length=3, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    
    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')


class SubTopics(models.Model):

    code = models.CharField(max_length=3, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    topic = models.ForeignKey(Topics, null=False, related_name='sub_topic', on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Sub Topic')
        verbose_name_plural = _('Sub Topics')


class Activity(models.Model):

    code = models.CharField(max_length=3, null=False, blank=False)
    description = models.TextField()
    sub_topic = models.ForeignKey(SubTopics, null=False, related_name='activity', on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')


class ImpactCategory(models.Model):

    code = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Impact Category')
        verbose_name_plural =  _('Impact Categories')


class InitiativeType(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)
    type = models.CharField(max_length=2, blank=False, null=False)
     
    ## Logs
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Initiative Type")
        verbose_name_plural = _("Initiative Types")

    def __unicode__(self):
        return smart_unicode(self.initiative_type_en)


class GeographicScale(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)
     
    ## Logs
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Geographic Scale")
        verbose_name_plural = _("Geographic Scales")

    def __unicode__(self):
        return smart_unicode(self.name)


class FinanceSourceType(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)
     
    ## Logs
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Finance Source Type")
        verbose_name_plural = _("Finance Source Types")

    def __unicode__(self):
        return smart_unicode(self.name)

class FinanceStatus(models.Model):
    
    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Finance Status")
        verbose_name_plural = _("Finance Statuses")

    def __unicode__(self):
        return smart_unicode(self.name)

class Status(models.Model):

    status = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")

    def __unicode__(self):
        return smart_unicode(self.status)


## section 5 new
class ThematicCategorizationType(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Thematic Categorization Type")
        verbose_name_plural = _("Thematic Categorization Types")

## section 5 new
class InformationSourceType(models.Model):
    name = models.CharField(max_length=500, null=True)
    code = models.CharField(max_length=500, null=True)
    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Information Source Type")
        verbose_name_plural = _("Information Source Types")

## section 5 new
class Classifier(models.Model):
    code = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Classifier")
        verbose_name_plural = _("Classifiers")



##
## Finish Catalogs
##

##
## Extra models
##

class Contact(models.Model):

    institution = models.CharField(max_length=500, null=True)
    full_name = models.CharField(max_length=100, blank=False, null=True)
    job_title = models.CharField(max_length=100, blank=False, null=True)
    email = models.EmailField(max_length=254, blank=False, null=True)
    phone = models.CharField(max_length=100, blank=False, null=True)

    user = models.ForeignKey(User, related_name='contact_registered', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __unicode__(self):
        return smart_unicode(self.full_name)



## section 5

class MonitoringReportingIndicator(models.Model):

    progress_in_monitoring = models.BooleanField(null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Monitoring and Reporting Indicators")
        verbose_name_plural = _("Monitoring and Reporting Indicators")


class MonitoringInformation(models.Model):
    
    ## TODO 
    ## This model is necessary, at the moment will be empty
    ## missing attributes that are not defined 
    code = models.CharField(max_length=255, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Monitoring Information")
        verbose_name_plural = _("Monitoring Information")

    
    def __str__(self):
        return smart_unicode(self.id)


class ImpactDocumentation(models.Model):
    ## TODO: Missing. catalogs emission sources and gases
    ## missing file for documentation of calculations estimate 
    estimate_reduction_co2 = models.TextField(null=True)
    period_potential_reduction =models.TextField(null=True)
    ##catalog
    carbon_deposit = models.ForeignKey(CarbonDeposit, null=True, related_name='impact_documentation', on_delete=models.CASCADE)
    base_line_definition = models.TextField(null=True)
    calculation_methodology = models.TextField(null=True)
    estimate_calculation_documentation = models.TextField(null=True)
    estimate_calculation_documentation_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    mitigation_action_in_inventory = models.BooleanField(null=True)


    ## Section 4.3
    ## TODO: Missing. catalogs standar to apply
    standard = models.ForeignKey(Standard, null=True, related_name='impact_documentation', on_delete=models.CASCADE)
    other_standard = models.TextField(null=True)
    carbon_international_commerce = models.BooleanField(null=True)
    methodologies_to_use = models.TextField(null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Monitoring Information")
        verbose_name_plural = _("Monitoring Information")

## missing Serializer
class Categorization(models.Model):
    
    action_goal = models.ManyToManyField(ActionGoals, related_name='categorization', blank=True)
    transformational_vision = models.ManyToManyField(TransformationalVisions, related_name='categorization', blank=True)
    sub_topics = models.ManyToManyField(SubTopics, related_name='categorization', blank=True)
    activities = models.ManyToManyField(Activity, related_name='categorization', blank=True)

    ## can be select more than one
    impact_categories = models.ManyToManyField(ImpactCategory, related_name='categorization', blank=True)
    is_part_to_another_mitigation_action = models.BooleanField(null=True)
    relation_description = models.CharField(max_length=255, null=True)


    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Categorization")
        verbose_name_plural = _("Categorization")


## section 5 new
class InformationSource(models.Model):
    responsible_institution = models.CharField(max_length=500, null=True)
    type = models.ForeignKey(InformationSourceType, null=True, related_name='information_source', on_delete=models.SET_NULL)
    other_type = models.CharField(max_length=500, null=True)
    statistical_operation = models.CharField(max_length=500, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Information Source")
        verbose_name_plural = _("Information Sources")


## section 5 new
class Indicator(models.Model):
    PERIODICITY = [
        ('YEARLY', 'Yearly'),
        ('BIANNUAL', 'Biannual'),
        ('QUARTERLY', 'Quartely')
    ]
    GEOGRAPHIC = [
        ('NATIONAL', 'National'),
        ('REGIONAL', 'Regional'),
        ('PROVINCIAL', 'Provincial'),
        ('CANTONAL', 'Cantonal'),
        ('OTHER', 'Other')
    ]

    ## TODO: Missing. catalogs for type 
    ## missing file for detail
    ## missing file for additional information

    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    unit = models.CharField(max_length=255, null=True)
    methodological_detail = models.TextField(null=True)
    ## need to endpoint to upload file
    methodological_detail_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    reporting_periodicity = models.CharField(max_length=50, choices=PERIODICITY, default='YEARLY', null=True)
    
    available_time_start_date = models.DateField(null=True)
    available_time_end_date = models.DateField(null=True)

    geographic_coverage = models.CharField(max_length=255, choices=GEOGRAPHIC, default='NATIONAL', null=True)
    other_geographic_coverage = models.CharField(max_length=255, blank=True, null=True)
    
    disaggregation = models.TextField(null=True)

    limitation = models.TextField(null=True)

    ## ensure sustainability
    additional_information = models.TextField(null=True)
    additional_information_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())

    comments = models.TextField(null=True)
    ## FK
    ## information source
    information_source = models.ForeignKey(InformationSource, null=True, related_name='indicator', on_delete=models.SET_NULL)
    
    ## thematic categorization
    type_of_data = models.ForeignKey(ThematicCategorizationType, null=True, related_name='indicator', on_delete=models.PROTECT)
    other_type_of_data = models.CharField(max_length=255, blank=True, null=True)
    classifier = models.ManyToManyField(Classifier, related_name='indicator', blank=True)
    other_classifier = models.CharField(max_length=255, blank=True, null=True)

    ## contact
    contact = models.ForeignKey(Contact, null=True, related_name='indicator', on_delete=models.SET_NULL)
    monitoring_information = models.ForeignKey(MonitoringInformation, related_name='indicator', null=True, on_delete=models.CASCADE)


    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Indicator")
        verbose_name_plural = _("Indicator")
    

    def __str__(self):

        return smart_unicode(self.name)

    def delete(self, *args, **kwargs):
        delete_field = ['contact', 'information_source']
        for field in delete_field:
            if hasattr(self, field):
                getattr(self, field).delete()

        super(Indicator, self).delete(*args, **kwargs)



## section 5 new
class IndicatorChangeLog(models.Model):

    indicator = models.ForeignKey(Indicator, related_name='indicator_change_log', on_delete=models.CASCADE)
    update_date = models.DateTimeField(auto_now=True)
    changes = models.TextField(null=True)
    changes_description = models.TextField(null=True)
    author = models.CharField(max_length=500, null=True)
    
    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MonitoringIndicator(models.Model):

    ## TODO: Missing.
    ## missing file for updated data
    initial_date_report_period = models.DateField(null=True)
    final_date_report_period = models.DateField(null=True)
    data_updated_date = models.DateField(null=True)
    updated_data = models.CharField(max_length=150, null=True)
    updated_data_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    progress_report = models.TextField(null=True)

    ## FK 
    indicator = models.ForeignKey(Indicator, related_name='monitoring_indicator', null=True, on_delete=models.CASCADE)
    monitoring_reporting_indicator = models.ForeignKey(MonitoringReportingIndicator, related_name='monitoring_indicator', null=True, on_delete=models.CASCADE)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Monitoring Indicator")
        verbose_name_plural = _("Monitoring Indicator")

    def __str__(self):
        return smart_unicode(self.status)


class QAQCReductionEstimateQuestion(models.Model):

    code = models.CharField(max_length=5, null=True)
    question = models.TextField(null=True)
    check = models.BooleanField(null=True)
    detail = models.TextField(null=True)
    
    ## FK
    impact_documentation = models.ForeignKey(ImpactDocumentation, related_name='question', null=True, on_delete=models.CASCADE)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Impact Documentation")
        verbose_name_plural = _("Impact Documentation")

    def __str__(self):
        return smart_unicode(self.status)


class Finance(models.Model):

    status = models.ForeignKey(FinanceStatus, related_name='finance', null=True, on_delete=models.CASCADE)
    administration = models.TextField(null=True)
    source = models.ManyToManyField(FinanceSourceType, related_name='finance', blank=True)
    source_description = models.CharField(max_length=255, null=True)
    reference_year =models.IntegerField(null=True, validators=[validate_year])
    budget = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    currency = models.CharField(choices=CURRENCIES, max_length=10, blank=False, null=True)
    mideplan_registered = models.BooleanField(null=True)
    mideplan_project = models.CharField(max_length=255, null=True) ## depend on mideplan registered
    executing_entity = models.CharField(max_length=255, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Finance")
        verbose_name_plural = _("Finance")

    def __unicode__(self):
        return smart_unicode(self.administration)


class GeographicLocation(models.Model):

    geographic_scale = models.ForeignKey(GeographicScale, related_name='geographic_location', null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=254, null=True)
    location_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Geographic Location")
        verbose_name_plural = _("Geographic Locations")

    def __unicode__(self):
        return smart_unicode(self.name)


class Initiative(models.Model):
    
    name = models.CharField(max_length=500, null=True)
    objective = models.TextField(null=True)
    description = models.TextField(null=True)
    description_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    initiative_type = models.ForeignKey(InitiativeType, related_name='initiative', null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Initiative")
        verbose_name_plural = _("Initiative")

    def __unicode__(self):
        return smart_unicode(self.name)


class InitiativeGoal(models.Model):

    goal = models.TextField(null=True)
    initiative = models.ForeignKey(Initiative, related_name='goal',on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Initiative Goal")
        verbose_name_plural = _("Initiative Goal")

    def __unicode__(self):
        return smart_unicode(self.goal)

class MitigationActionStatus(models.Model):

    status = models.ForeignKey(Status, related_name='mitigation_action_status', null=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    other_end_date = models.CharField(max_length=254, null=True)
    institution = models.CharField(max_length=254, null=True)
    other_institution = models.TextField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Mitigation Action Status")
        verbose_name_plural = _("Mitigation Action Status")

    def __unicode__(self):
        return smart_unicode(self.status)



##
## Finish extra model
##


## Greenhouse gases(GHG) - Gases de efectos invernadero (GEI)
class GHGInformation(models.Model): 
    
    ## TODO missing file to graphic description 
    impact_emission = models.TextField(null=True)
    graphic_description = models.TextField(null=True)
    graphic_description_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    impact_sector = models.ManyToManyField(GHGImpactSector, related_name='ghg_information', blank=True)
    goals = models.ManyToManyField(SustainableDevelopmentGoals, related_name='ghg_information', blank=True)

    ##logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("GHG Informaction")
        verbose_name_plural = _("GHG Informaction")



class MitigationAction(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fsm_state = FSMField(default='new', protected=True, max_length=100)
    # Foreign Key
    contact = models.ForeignKey(Contact, related_name='mitigation_action', blank=True, null=True, on_delete=models.CASCADE)
    initiative = models.ForeignKey(Initiative, related_name='mitigation_action', null=True, on_delete=models.CASCADE)
    status_information = models.ForeignKey(MitigationActionStatus, related_name='mitigation_action', null=True, on_delete=models.CASCADE)
    geographic_location = models.ForeignKey(GeographicLocation, related_name='mitigation_action', null=True, on_delete=models.CASCADE)
    categorization = models.ForeignKey(Categorization, related_name='mitigation_action', null=True, on_delete=models.CASCADE)
    finance = models.ForeignKey(Finance, related_name='mitigation_action', null=True, on_delete=models.CASCADE)
    ghg_information = models.ForeignKey(GHGInformation, related_name='mitigation_action', null=True, on_delete=models.CASCADE)
    
    ## section 4
    impact_documentation = models.ForeignKey(ImpactDocumentation, related_name='mitigation_action', null=True, on_delete=models.SET_NULL)
    
    ## section 5
    monitoring_information = models.ForeignKey(MonitoringInformation, related_name='mitigation_action', null=True, on_delete=models.SET_NULL)

    ## section 6

    monitoring_reporting_indicator = models.ForeignKey(MonitoringReportingIndicator, related_name='mitigation_action', null=True, on_delete=models.SET_NULL)
    
    # Timestamps and log 
    user = models.ForeignKey(User, related_name='mitigation_action', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Mitigation Action")
        verbose_name_plural = _("Mitigation Actions")
        ordering = ('created',)

    # FSM Annotated Methods (Transitions) and Ordinary Conditions
    # --- Transition ---
    # new -> submitted
    def can_submit(self):
        # Transition condition logic goes here
        # Verify current state
        # - new
        return self.fsm_state == 'new'

    @transition(field='fsm_state', source='new', target='submitted', conditions=[can_submit], on_error='failed', permission='')
    def submit(self):
        result = 'The mitigation action is transitioning from new to submitted'
        # Notify to DCC placeholder
        print(result)



    # --- Transition ---
    # submitted -> in_evaluation_by_DCC
    def can_evaluate_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted
        return self.fsm_state == 'submitted'
    
    @transition(field='fsm_state', source='submitted', target='in_evaluation_by_DCC', conditions=[can_evaluate_DCC], on_error='failed', permission='')
    def evaluate_DCC(self):
        print('The mitigation action is transitioning from submitted to in_evaluation_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # updating_by_request -> in_evaluation_by_DCC
    def can_update_evaluate_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - updating_by_request
        return self.fsm_state == 'updating_by_request'

    @transition(field='fsm_state', source='updating_by_request', target='in_evaluation_by_DCC', conditions=[can_update_evaluate_DCC], on_error='failed', permission='')
    def update_evaluate_DCC(self):
        print('The mitigation action is transitioning from updating_by_request to in_evaluation_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_by_DCC -> decision_step_DCC
    def can_submit_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_by_DCC
        return self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='decision_step_DCC', conditions=[can_submit_DCC], on_error='failed', permission='')
    def submit_DCC(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to decision_step_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_DCC -> changes_requested_by_DCC
    def can_request_changes_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_DCC
        # - in_evaluation_by_DCC
        return self.fsm_state == 'decision_step_DCC' or self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='decision_step_DCC', target='changes_requested_by_DCC', conditions=[can_request_changes_DCC], on_error='failed', permission='')
    def request_changes_DCC(self):
        print('The mitigation action is transitioning from decision_step_DCC to changes_requested_by_DCC')
        # Notify to DCC placeholder
        # self.notify_changes_requested_DCC()
        pass

    # --- Transition ---
    # decision_step_DCC -> rejected_by_DCC
    def can_reject_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_DCC
        # - in_evaluation_by_DCC
        return self.fsm_state == 'decision_step_DCC' or self.fsm_state == 'in_evaluation_by_DCC'

    @transition(field='fsm_state', source='decision_step_DCC', target='rejected_by_DCC', conditions=[can_reject_DCC], on_error='failed', permission='')
    def reject_DCC(self):
        print('The mitigation action is transitioning from decision_step_DCC to rejected_by_DCC')
        # Notify to DCC placeholder
        # self.notify_reject_DCC()
        pass

    # --- Transition ---
    # decision_step_DCC -> registering
    def can_register(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_DCC
        # - in_evaluation_by_DCC
        return self.fsm_state == 'decision_step_DCC' or self.fsm_state == 'in_evaluation_by_DCC'
    
    @transition(field='fsm_state', source='decision_step_DCC', target='registering', conditions=[can_register], on_error='failed', permission='')
    def register(self):
        print('The mitigation action is transitioning from decision_step_DCC to registering')
        # Notify to DCC placeholder
        # self.notify_registering_DCC()
        pass

    # --- Transition ---
    # in_evaluation_by_DCC -> changes_requested_by_DCC
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='changes_requested_by_DCC', conditions=[can_request_changes_DCC], on_error='failed', permission='')
    def evaluate_request_changes_DCC(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to changes_requested_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # changes_requested_by_DCC -> updating_by_request
    def can_update_by_request(self):
        # Transition condition logic goes here
        # Verify current state
        # - changes_requested_by_DCC
        return self.fsm_state == 'changes_requested_by_DCC'

    @transition(field='fsm_state', source='changes_requested_by_DCC', target='updating_by_request', conditions=[can_update_by_request], on_error='failed', permission='')
    def update_by_request(self):
        result = 'The mitigation action is transitioning from changes_requested_by_DCC to updating_by_request'
        
        print(result)
        
    # --- Transition ---
    # in_evaluation_by_DCC -> rejected_by_DCC
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='rejected_by_DCC', conditions=[can_reject_DCC], on_error='failed', permission='')
    def evaluate_reject_by_DCC(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to rejected_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # rejected_by_DCC -> end
    def can_end(self):
        # Transition condition logic goes here
        # Verify current state
        # - rejected_by_DCC
        return self.fsm_state == 'rejected_by_DCC'

    @transition(field='fsm_state', source='rejected_by_DCC', target='end', conditions=[can_end], on_error='failed', permission='')
    def end(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to rejected_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_by_DCC -> registering
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='registering', conditions=[can_register], on_error='failed', permission='')
    def evaluate_register(self):
        print('The mitigation action is transitioning from in_evaluation_by_DCC to registering')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # registering -> in_evaluation_INGEI_by_DCC_IMN
    def can_evaluate_INGEI(self):
        # Transition condition logic goes here
        # Verify current state
        # - registering
        return self.fsm_state == 'registering'

    @transition(field='fsm_state', source='registering', target='in_evaluation_INGEI_by_DCC_IMN', conditions=[can_evaluate_INGEI], on_error='failed', permission='')
    def evaluate_INGEI(self):
        print('The mitigation action is transitioning from registering to in_evaluation_INGEI_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_INGEI_by_DCC_IMN -> submit_INGEI_harmonization_required
    def can_submit_INGEI(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_INGEI_by_DCC_IMN
        return self.fsm_state == 'in_evaluation_INGEI_by_DCC_IMN'

    @transition(field='fsm_state', source='in_evaluation_INGEI_by_DCC_IMN', target='submit_INGEI_harmonization_required', conditions=[can_submit_INGEI], on_error='failed', permission='')
    def submit_INGEI(self):
        print('The mitigation action is transitioning from in_evaluation_INGEI_by_DCC_IMN to submit_INGEI_harmonization_required')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_harmonization_required -> INGEI_harmonization_required
    def can_require_INGEI_harmonization(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_harmonization_required
        return self.fsm_state == 'submit_INGEI_harmonization_required'

    @transition(field='fsm_state', source='submit_INGEI_harmonization_required', target='INGEI_harmonization_required', conditions=[can_require_INGEI_harmonization], on_error='failed', permission='')
    def require_INGEI_harmonization(self):
        print('The mitigation action is transitioning from submit_INGEI_harmonization_required to INGEI_harmonization_required')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_harmonization_required -> submitted_SINAMECC_conceptual_proposal_integration
    def can_submit_INGEI_SINAMECC_conceptual_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_harmonization_required
        return self.fsm_state == 'submit_INGEI_harmonization_required'

    @transition(field='fsm_state', source='submit_INGEI_harmonization_required', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_submit_INGEI_SINAMECC_conceptual_proposal], on_error='failed', permission='')
    def submit_INGEI_SINAMECC_conceptual_proposal(self):
        print('The mitigation action is transitioning from submit_INGEI_harmonization_required to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_INGEI_by_DCC_IMN -> INGEI_harmonization_required
    def can_evaluate_require_INGEI_harmonization(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_INGEI_by_DCC_IMN
        return self.fsm_state == 'in_evaluation_INGEI_by_DCC_IMN'

    @transition(field='fsm_state', source='in_evaluation_INGEI_by_DCC_IMN', target='INGEI_harmonization_required', conditions=[can_evaluate_require_INGEI_harmonization], on_error='failed', permission='')
    def evaluate_require_INGEI_harmonization(self):
        print('The mitigation action is transitioning from in_evaluation_INGEI_by_DCC_IMN to INGEI_harmonization_required')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_harmonization_required -> updating_INGEI_changes_proposal
    def can_update_INGEI_changes_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_harmonization_required
        return self.fsm_state == 'INGEI_harmonization_required'

    @transition(field='fsm_state', source='INGEI_harmonization_required', target='updating_INGEI_changes_proposal', conditions=[can_update_INGEI_changes_proposal], on_error='failed', permission='')
    def update_INGEI_changes_proposal(self):
        print('The mitigation action is transitioning from INGEI_harmonization_required to updating_INGEI_changes_proposal')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_harmonization_required -> submitted_SINAMECC_conceptual_proposal_integration
    def can_submit_SINAMECC_conceptual_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_harmonization_required
        return self.fsm_state == 'INGEI_harmonization_required'

    @transition(field='fsm_state', source='INGEI_harmonization_required', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_submit_SINAMECC_conceptual_proposal], on_error='failed', permission='')
    def submit_SINAMECC_conceptual_proposal(self):
        print('The mitigation action is transitioning from INGEI_harmonization_required to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # updating_INGEI_changes_proposal -> submitted_INGEI_changes_proposal_evaluation
    def can_submit_INGEI_changes_evaluation(self):
        # Transition condition logic goes here
        # Verify current state
        # - updating_INGEI_changes_proposal
        return self.fsm_state == 'updating_INGEI_changes_proposal'

    @transition(field='fsm_state', source='updating_INGEI_changes_proposal', target='submitted_INGEI_changes_proposal_evaluation', conditions=[can_submit_INGEI_changes_evaluation], on_error='failed', permission='')
    def submit_INGEI_changes_evaluation(self):
        print('The mitigation action is transitioning from updating_INGEI_changes_proposal to submitted_INGEI_changes_proposal_evaluation')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submitted_INGEI_changes_proposal_evaluation -> in_evaluation_INGEI_changes_proposal_by_DCC_IMN
    def can_evaluate_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted_INGEI_changes_proposal_evaluation
        return self.fsm_state == 'submitted_INGEI_changes_proposal_evaluation'

    @transition(field='fsm_state', source='submitted_INGEI_changes_proposal_evaluation', target='in_evaluation_INGEI_changes_proposal_by_DCC_IMN', conditions=[can_evaluate_DCC_IMN], on_error='failed', permission='')
    def evaluate_DCC_IMN(self):
        print('The mitigation action is transitioning from submitted_INGEI_changes_proposal_evaluation to in_evaluation_INGEI_changes_proposal_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_INGEI_changes_proposal_by_DCC_IMN -> submit_INGEI_changes_proposal_evaluation_result
    def can_submit_INGEI_changes_proposal_evaluation_result(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_INGEI_changes_proposal_by_DCC_IMN
        return self.fsm_state == 'in_evaluation_INGEI_changes_proposal_by_DCC_IMN'

    @transition(field='fsm_state', source='in_evaluation_INGEI_changes_proposal_by_DCC_IMN', target='submit_INGEI_changes_proposal_evaluation_result', conditions=[can_submit_INGEI_changes_proposal_evaluation_result], on_error='failed', permission='')
    def submit_INGEI_changes_proposal_evaluation_result(self):
        print('The mitigation action is transitioning from in_evaluation_INGEI_changes_proposal_by_DCC_IMN to submit_INGEI_changes_proposal_evaluation_result')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_changes_proposal_evaluation_result -> INGEI_changes_proposal_changes_requested_by_DCC_IMN
    def can_request_changes_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_changes_proposal_evaluation_result
        return self.fsm_state == 'submit_INGEI_changes_proposal_evaluation_result'

    @transition(field='fsm_state', source='submit_INGEI_changes_proposal_evaluation_result', target='INGEI_changes_proposal_changes_requested_by_DCC_IMN', conditions=[can_request_changes_DCC_IMN], on_error='failed', permission='')
    def request_changes_DCC_IMN(self):
        print('The mitigation action is transitioning from submit_INGEI_changes_proposal_evaluation_result to INGEI_changes_proposal_changes_requested_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_changes_proposal_evaluation_result -> INGEI_changes_proposal_rejected_by_DCC_IMN
    def can_reject_changes_proposal_by_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_changes_proposal_evaluation_result
        return self.fsm_state == 'submit_INGEI_changes_proposal_evaluation_result'

    @transition(field='fsm_state', source='submit_INGEI_changes_proposal_evaluation_result', target='INGEI_changes_proposal_rejected_by_DCC_IMN', conditions=[can_reject_changes_proposal_by_DCC_IMN], on_error='failed', permission='')
    def reject_changes_proposal_by_DCC_IMN(self):
        print('The mitigation action is transitioning from submit_INGEI_changes_proposal_evaluation_result to INGEI_changes_proposal_rejected_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submit_INGEI_changes_proposal_evaluation_result -> INGEI_changes_proposal_accepted_by_DCC_IMN
    def can_accept_changes_proposal_by_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - submit_INGEI_changes_proposal_evaluation_result
        return self.fsm_state == 'submit_INGEI_changes_proposal_evaluation_result'

    @transition(field='fsm_state', source='submit_INGEI_changes_proposal_evaluation_result', target='INGEI_changes_proposal_accepted_by_DCC_IMN', conditions=[can_accept_changes_proposal_by_DCC_IMN], on_error='failed', permission='')
    def accept_changes_proposal_by_DCC_IMN(self):
        print('The mitigation action is transitioning from submit_INGEI_changes_proposal_evaluation_result to INGEI_changes_proposal_accepted_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_changes_proposal_changes_requested_by_DCC_IMN -> updating_INGEI_changes_proposal_by_request_of_DCC_IMN
    def can_update_changes_proposal_by_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_changes_proposal_changes_requested_by_DCC_IMN
        return self.fsm_state == 'INGEI_changes_proposal_changes_requested_by_DCC_IMN'

    @transition(field='fsm_state', source='INGEI_changes_proposal_changes_requested_by_DCC_IMN', target='updating_INGEI_changes_proposal_by_request_of_DCC_IMN', conditions=[can_update_changes_proposal_by_DCC_IMN], on_error='failed', permission='')
    def update_changes_proposal_by_DCC_IMN(self):
        print('The mitigation action is transitioning from INGEI_changes_proposal_changes_requested_by_DCC_IMN to updating_INGEI_changes_proposal_by_request_of_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_changes_proposal_rejected_by_DCC_IMN -> submitted_SINAMECC_conceptual_proposal_integration
    def can_submit_SINAMECC_conceptual_proposal_integration(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_changes_proposal_rejected_by_DCC_IMN
        return self.fsm_state == 'INGEI_changes_proposal_rejected_by_DCC_IMN'

    @transition(field='fsm_state', source='INGEI_changes_proposal_rejected_by_DCC_IMN', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_submit_SINAMECC_conceptual_proposal_integration], on_error='failed', permission='')
    def submit_SINAMECC_conceptual_proposal_integration(self):
        print('The mitigation action is transitioning from INGEI_changes_proposal_rejected_by_DCC_IMN to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # INGEI_changes_proposal_accepted_by_DCC_IMN -> implementing_INGEI_changes
    def can_implement_INGEI_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - INGEI_changes_proposal_accepted_by_DCC_IMN
        return self.fsm_state == 'INGEI_changes_proposal_accepted_by_DCC_IMN'

    @transition(field='fsm_state', source='INGEI_changes_proposal_accepted_by_DCC_IMN', target='implementing_INGEI_changes', conditions=[can_implement_INGEI_changes], on_error='failed', permission='')
    def implement_INGEI_changes(self):
        print('The mitigation action is transitioning from INGEI_changes_proposal_accepted_by_DCC_IMN to implementing_INGEI_changes')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # updating_INGEI_changes_proposal_by_request_of_DCC_IMN -> in_evaluation_INGEI_changes_proposal_by_DCC_IMN
    def can_update_evaluate_DCC_IMN(self):
        # Transition condition logic goes here
        # Verify current state
        # - updating_INGEI_changes_proposal_by_request_of_DCC_IMN
        return self.fsm_state == 'updating_INGEI_changes_proposal_by_request_of_DCC_IMN'

    @transition(field='fsm_state', source='updating_INGEI_changes_proposal_by_request_of_DCC_IMN', target='in_evaluation_INGEI_changes_proposal_by_DCC_IMN', conditions=[can_update_evaluate_DCC_IMN], on_error='failed', permission='')
    def update_evaluate_DCC_IMN(self):
        print('The mitigation action is transitioning from updating_INGEI_changes_proposal_by_request_of_DCC_IMN to in_evaluation_INGEI_changes_proposal_by_DCC_IMN')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # implementing_INGEI_changes -> submitted_SINAMECC_conceptual_proposal_integration
    def can_implement_submit_SINAMECC_conceptual_proposal_integration(self):
        # Transition condition logic goes here
        # Verify current state
        # - implementing_INGEI_changes
        return self.fsm_state == 'implementing_INGEI_changes'

    @transition(field='fsm_state', source='implementing_INGEI_changes', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_implement_submit_SINAMECC_conceptual_proposal_integration], on_error='failed', permission='')
    def implement_submit_SINAMECC_conceptual_proposal_integration(self):
        print('The mitigation action is transitioning from implementing_INGEI_changes to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submitted_SINAMECC_conceptual_proposal_integration -> in_evaluation_conceptual_proposal_by_DCC
    def can_evaluate_conceptual_proposal_DCC(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted_SINAMECC_conceptual_proposal_integration
        return self.fsm_state == 'submitted_SINAMECC_conceptual_proposal_integration'

    @transition(field='fsm_state', source='submitted_SINAMECC_conceptual_proposal_integration', target='in_evaluation_conceptual_proposal_by_DCC', conditions=[can_evaluate_conceptual_proposal_DCC], on_error='failed', permission='')
    def evaluate_conceptual_proposal_DCC(self):
        print('The mitigation action is transitioning from submitted_SINAMECC_conceptual_proposal_integration to in_evaluation_conceptual_proposal_by_DCC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # conceptual_proposal_approved -> planning_integration_with_SINAMECC
    def can_plan_integration_SINAMECC(self):
        # Transition condition logic goes here
        # Verify current state
        # - conceptual_proposal_approved
        return self.fsm_state == 'conceptual_proposal_approved'

    @transition(field='fsm_state', source='conceptual_proposal_approved', target='planning_integration_with_SINAMECC', conditions=[can_plan_integration_SINAMECC], on_error='failed', permission='')
    def plan_integration_SINAMECC(self):
        print('The mitigation action is transitioning from conceptual_proposal_approved to planning_integration_with_SINAMECC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # changes_requested_to_conceptual_proposal -> submitted_conceptual_proposal_changes
    def can_submit_conceptual_proposal_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - changes_requested_to_conceptual_proposal
        return self.fsm_state == 'changes_requested_to_conceptual_proposal'

    @transition(field='fsm_state', source='changes_requested_to_conceptual_proposal', target='submitted_conceptual_proposal_changes', conditions=[can_submit_conceptual_proposal_changes], on_error='failed', permission='')
    def submit_conceptual_proposal_changes(self):
        print('The mitigation action is transitioning from changes_requested_to_conceptual_proposal to submitted_conceptual_proposal_changes')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submitted_conceptual_proposal_changes -> submitted_SINAMECC_conceptual_proposal_integration
    def can_submit_SINAMECC_conceptual_proposal_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted_conceptual_proposal_changes
        return self.fsm_state == 'submitted_conceptual_proposal_changes'

    @transition(field='fsm_state', source='submitted_conceptual_proposal_changes', target='submitted_SINAMECC_conceptual_proposal_integration', conditions=[can_submit_SINAMECC_conceptual_proposal_changes], on_error='failed', permission='')
    def submit_SINAMECC_conceptual_proposal_changes(self):
        print('The mitigation action is transitioning from submitted_conceptual_proposal_changes to submitted_SINAMECC_conceptual_proposal_integration')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # SINAMECC_integration_approved -> implementing_SINAMECC_changes
    def can_implement_SINAMECC_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - SINAMECC_integration_approved
        return self.fsm_state == 'SINAMECC_integration_approved'

    @transition(field='fsm_state', source='SINAMECC_integration_approved', target='implementing_SINAMECC_changes', conditions=[can_implement_SINAMECC_changes], on_error='failed', permission='')
    def implement_SINAMECC_changes(self):
        print('The mitigation action is transitioning from SINAMECC_integration_approved to implementing_SINAMECC_changes')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # SINAMECC_integration_changes_requested -> submitted_SINAMECC_integration_changes
    def can_submit_SINAMECC_integration_changes(self):
        # Transition condition logic goes here
        # Verify current state
        # - SINAMECC_integration_changes_requested
        return self.fsm_state == 'SINAMECC_integration_changes_requested'

    @transition(field='fsm_state', source='SINAMECC_integration_changes_requested', target='submitted_SINAMECC_integration_changes', conditions=[can_submit_SINAMECC_integration_changes], on_error='failed', permission='')
    def submit_SINAMECC_integration_changes(self):
        print('The mitigation action is transitioning from SINAMECC_integration_changes_requested to submitted_SINAMECC_integration_changes')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # submitted_SINAMECC_integration_changes -> planning_integration_with_SINAMECC
    def can_submit_plan_integration_SINAMECC(self):
        # Transition condition logic goes here
        # Verify current state
        # - submitted_SINAMECC_integration_changes
        return self.fsm_state == 'submitted_SINAMECC_integration_changes'

    @transition(field='fsm_state', source='submitted_SINAMECC_integration_changes', target='planning_integration_with_SINAMECC', conditions=[can_submit_plan_integration_SINAMECC], on_error='failed', permission='')
    def submit_plan_integration_SINAMECC(self):
        print('The mitigation action is transitioning from submitted_SINAMECC_integration_changes to planning_integration_with_SINAMECC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # implementing_SINAMECC_changes -> end
    def can_end_SINAMECC(self):
        # Transition condition logic goes here
        # Verify current state
        # - implementing_SINAMECC_changes
        return self.fsm_state == 'implementing_SINAMECC_changes'

    @transition(field='fsm_state', source='implementing_SINAMECC_changes', target='end', conditions=[can_end_SINAMECC], on_error='failed', permission='')
    def end_SINAMECC(self):
        print('The mitigation action is transitioning from implementing_SINAMECC_changes to end')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # in_evaluation_conceptual_proposal_by_DCC -> decision_step_DCC_proposal
    def can_decide_DCC_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - implementing_SINAMECC_changes
        return self.fsm_state == 'in_evaluation_conceptual_proposal_by_DCC'

    @transition(field='fsm_state', source='in_evaluation_conceptual_proposal_by_DCC', target='decision_step_DCC_proposal', conditions=[can_decide_DCC_proposal], on_error='failed', permission='')
    def decide_DCC_proposal(self):
        print('The mitigation action is transitioning from in_evaluation_conceptual_proposal_by_DCC to decision_step_DCC_proposal')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_DCC_proposal -> conceptual_proposal_approved
    def can_approve_conceptual_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_conceptual_proposal_by_DCC
        return self.fsm_state == 'decision_step_DCC_proposal'

    @transition(field='fsm_state', source='decision_step_DCC_proposal', target='conceptual_proposal_approved', conditions=[can_approve_conceptual_proposal], on_error='failed', permission='')
    def approve_conceptual_proposal(self):
        print('The mitigation action is transitioning from decision_step_DCC_proposal to conceptual_proposal_approved')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_DCC_proposal -> changes_requested_to_conceptual_proposal
    def can_request_changes_conceptual_proposal(self):
        # Transition condition logic goes here
        # Verify current state
        # - in_evaluation_conceptual_proposal_by_DCC
        return self.fsm_state == 'decision_step_DCC_proposal'

    @transition(field='fsm_state', source='decision_step_DCC_proposal', target='changes_requested_to_conceptual_proposal', conditions=[can_request_changes_conceptual_proposal], on_error='failed', permission='')
    def request_changes_conceptual_proposal(self):
        print('The mitigation action is transitioning from decision_step_DCC_proposal to changes_requested_to_conceptual_proposal')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # planning_integration_with_SINAMECC -> decision_step_SINAMEC
    def can_decide_SINAMECC(self):
        # Transition condition logic goes here
        # Verify current state
        # - implementing_SINAMECC_changes
        return self.fsm_state == 'planning_integration_with_SINAMECC'

    @transition(field='fsm_state', source='planning_integration_with_SINAMECC', target='decision_step_SINAMEC', conditions=[can_decide_SINAMECC], on_error='failed', permission='')
    def decide_SINAMECC(self):
        print('The mitigation action is transitioning from planning_integration_with_SINAMECC to decision_step_SINAMEC')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_SINAMEC -> SINAMECC_integration_approved
    def can_approve_SINAMECC_integration(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_SINAMEC
        return self.fsm_state == 'decision_step_SINAMEC'

    @transition(field='fsm_state', source='decision_step_SINAMEC', target='SINAMECC_integration_approved', conditions=[can_approve_SINAMECC_integration], on_error='failed', permission='')
    def approve_SINAMECC_integration(self):
        print('The mitigation action is transitioning from decision_step_SINAMEC to SINAMECC_integration_approved')
        # Additional logic goes here.
        pass

    # --- Transition ---
    # decision_step_SINAMEC -> SINAMECC_integration_changes_requested
    def can_request_changes_SINAMECC_integration(self):
        # Transition condition logic goes here
        # Verify current state
        # - decision_step_SINAMEC
        return self.fsm_state == 'decision_step_SINAMEC'

    @transition(field='fsm_state', source='decision_step_SINAMEC', target='SINAMECC_integration_changes_requested', conditions=[can_request_changes_SINAMECC_integration], on_error='failed', permission='')
    def request_changes_SINAMECC_integration(self):
        print('The mitigation action is transitioning from decision_step_SINAMEC to SINAMECC_integration_changes_requested')
        # Additional logic goes here.
        pass

    def __unicode__(self):
        return smart_unicode(self.name)

    

class ChangeLog(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=False)
    # Foreign Keys
    mitigation_action = models.ForeignKey(MitigationAction, related_name='change_log', on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=100, null=True)
    current_status = models.CharField(max_length=100)
    
    user = models.ForeignKey(User, related_name='change_log', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ChangeLog")
        verbose_name_plural = _("ChangeLogs")
        ordering = ('date',)

    def __unicode__(self):
        return smart_unicode(self.name)