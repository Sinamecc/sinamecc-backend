from __future__ import unicode_literals
from django.db.models import manager

from django.db.models.fields import BLANK_CHOICE_DASH, CharField, related
from django.db.models.query import QuerySet
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




##
## Finish Catalogs
##

##
## Extra models
##

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



class Indicator(models.Model):
    PERIODICITY = [
        ('YEARLY', 'Yearly'),
        ('BIANNUAL', 'Biannual'),
        ('QUARTERLY', 'Quartely')
    ]
    ## TODO: Missing. catalogs for type 
    ## missing file for detail
    ## missing file for additional information

    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    type = models.CharField(max_length=255, null=True)
    unit = models.CharField(max_length=255, null=True)
    methodological_detail = models.TextField(null=True)
    ## detail file here
    reporting_periodicity = models.CharField(max_length=50, choices=PERIODICITY, default='YEARLY', null=True)
    
    data_generating_institution = models.CharField(max_length=255, null=True)
    reporting_institution = models.CharField(max_length=255, null=True)
    measurement_start_date = models.DateField(null=True)
    additional_information = models.TextField(null=True)
    ## aditional information file

    ## FK
    monitoring_information = models.ForeignKey(MonitoringInformation, related_name='indicator', null=True, on_delete=models.CASCADE)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Indicator")
        verbose_name_plural = _("Indicator")
    

    def __str__(self):

        return smart_unicode(self.name)


class MonitoringIndicator(models.Model):

    ## TODO: Missing.
    ## missing file for updated data
    ## missing url for updated data
    initial_date_report_period = models.DateField(null=True)
    final_date_report_period = models.DateField(null=True)
    data_updated_date = models.DateField(null=True)
    updated_data = models.CharField(max_length=150, null=True)
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
    source = models.ForeignKey(FinanceSourceType, related_name='finance', null=True, on_delete=models.CASCADE)
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

    ## comments
    review_count = models.IntegerField(null=True, blank=True, default=0)
    comments = models.ManyToManyField(Comment, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    ## email service
    email_service = MitigationActionEmailServices(EmailServices())

    class Meta:
        verbose_name = _("Mitigation Action")
        verbose_name_plural = _("Mitigation Actions")
        ordering = ('created',)

    # FSM Annotated Methods (Transitions) and Ordinary Conditions
    # --- Transition ---
    def can_submit(self):
        ## check all field are filled !!
        ## check current status is new
        return self.fsm_state in ['new','updating_by_request_DCC']
  
    def can_evaluate_by_DCC(self):
        ## check current status is submitted
        return self.fsm_state == 'submitted'

    ## rejected_by_DCC, requested_changes_by_DCC, accepted_by_DCC
    def can_rejected_by_DCC(self):
        ## check current status is submitted
        return self.fsm_state == 'in_evaluation_by_DCC'
    
    def can_request_changes_by_DCC(self):
        ## check current status is submitted
        return self.fsm_state == 'in_evaluation_by_DCC'
    
    def can_acception_by_DCC(self):
        ## check current status is submitted
        return self.fsm_state == 'in_evaluation_by_DCC'

    def can_update_by_DCC_request(self):
        ## check current status is submitted
        return self.fsm_state == 'requested_changes_by_DCC'

    @transition(field='fsm_state', source=['new', 'updating_by_request_DCC'], target='submitted', conditions=[can_submit], on_error='submitted')
    def submit(self):
        # new --> submitted        
        # send email to user that submitted the action
        print(f'The mitigation action is transitioning from <{self.fsm_state}> to <submitted>')
        email_function = {
            'new': self.email_service.notify_dcc_responsible_mitigation_action_submission,
            'updating_by_request_DCC': self.email_service.notify_dcc_responsible_mitigation_action_update,
        }

        email_status, email_data = email_function.get(self.fsm_state)(self)
        if email_status:
            print(email_data)
            return email_status, email_data
        else:
            ...
            ## maybe raise exception

    
    @transition(field='fsm_state', source='submitted', target='in_evaluation_by_DCC', conditions=[can_evaluate_by_DCC], on_error='submitted', permission='')
    def evaluate_by_DCC(self):
        # submitted --> in_evaluation_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <submitted> to <in_evaluation_by_DCC>')

        email_status, email_data = self.email_service.notify_contact_responsible_mitigation_action_evaluation_by_dcc(self)
        if email_status:
            print(email_data)
            return email_status, email_data
        else:
            ...
            ## maybe raise exception

    ##
    ## rejected_by_DCC, requested_changes_by_DCC, accepted_by_DCC
    ##
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='rejected_by_DCC', conditions=[can_rejected_by_DCC], on_error='in_evaluation_by_DCC', permission='')
    def evaluate_by_DCC_rejected(self):
        # in_evaluation_by_DCC --> rejected_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <in_evaluation_by_DCC> to <rejected_by_DCC>')
        email_status, email_data = self.email_service.notify_contact_responsible_mitigation_action_rejection(self)
        if email_status:
            print(email_data)
            return email_status, email_data
        else:
            ...
            ## maybe raise exception
    
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='requested_changes_by_DCC', conditions=[can_request_changes_by_DCC], on_error='in_evaluation_by_DCC', permission='')
    def evaluate_by_DCC_requested_changes(self):
        # in_evaluation_by_DCC --> requested_changes_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <in_evaluation_by_DCC> to <requested_changes_by_DCC>')
        ...
    
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='accepted_by_DCC', conditions=[can_acception_by_DCC], on_error='in_evaluation_by_DCC', permission='')
    def evaluate_by_DCC_accepted(self):
        # in_evaluation_by_DCC --> accepted_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <in_evaluation_by_DCC> to <accepted_by_DCC>')
        email_status, email_data = self.email_service.notify_contact_responsible_mitigation_action_approval(self)
        if email_status:
            print(email_data)
            return email_status, email_data
        else:
            ...
            ## maybe raise exception
    
    ## rejected by DCC to end
    @transition(field='fsm_state', source='rejected_by_DCC', target='end', conditions=[], on_error='rejected_by_DCC', permission='')
    def rejected_by_DCC_to_end(self):
        # rejected_by_DCC --> rejected_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <rejected_by_DCC> to <end>')
        ...
    
    @transition(field='fsm_state', source='requested_changes_by_DCC', target='updating_by_request_DCC', conditions=[can_update_by_DCC_request], on_error='requested_changes_by_DCC', permission='')
    def update_by_DCC_request(self):
        # requested_changes_by_DCC --> updating_by_request_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <requested_changes_by_DCC> to <updating_by_request_DCC>')
        ...
    
    ## accepted_by_DCC to	registered_by_DCC
    @transition(field='fsm_state', source='accepted_by_DCC', target='registered_by_DCC', conditions=[], on_error='accepted_by_DCC', permission='')
    def registered_by_DCC(self):
        # accepted_by_DCC --> registered_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <accepted_by_DCC> to <registered_by_DCC>')
        ...


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