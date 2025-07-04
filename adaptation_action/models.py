from distutils.text_file import TextFile
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from general.models import Address
from django_fsm import FSMField, transition
from time import gmtime, strftime
from general.storages import PrivateMediaStorage
from adaptation_action.email_services import AdaptationActionEmailServices
from general.services import EmailServices
from django.db import transaction

from workflow.models import Comment
from .workflow.states import States as FSM_STATE
# Create your models here.
User =  get_user_model()

def directory_path(instance, filename): 
    path = "adaptation_action/{0}/{1}/{2}/"

    return path.format(instance._meta.verbose_name, strftime("%Y%m%d", gmtime()), filename)


class ReportOrganizationType(models.Model): 
    
    code = models.CharField(max_length=3, null=True)
    entity_type = models.CharField(max_length=100, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Report Organization Type")
        verbose_name_plural = _("Report Organization Types")

class Contact(models.Model):

    contact_name = models.TextField(null=True)      #1.1.5
    contact_position = models.TextField(null=True)  #1.1.6
    email = models.TextField(null=True)             #1.1.7
    phone = models.TextField(null=True)             #1.1.8
    address = models.TextField(null=True)
    institution = models.TextField(null=True)

    user = models.ForeignKey(User, related_name='contact_adaptation_action', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

class ReportOrganization(models.Model):

    responsible_entity = models.CharField(max_length=250, null=True)    #1.1.2
    legal_identification = models.CharField(max_length=50, null=True)   #1.1.3
    elaboration_date = models.DateField(null=True)                      #1.1.4
    entity_address = models.CharField(max_length=250, null=True)        #1.1.9
    
    report_organization_type = models.ForeignKey(ReportOrganizationType, related_name="report_organization", null=True, on_delete=models.CASCADE)   #1.1.1
    other_report_organization_type = models.TextField(null=True)
    contact = models.ForeignKey(Contact, related_name="report_organization", null=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Report Organization")
        verbose_name_plural = _("Report Organizations")

class AdaptationActionType(models.Model):

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=2, null=True)
    count = models.IntegerField(default=0)

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Adaptation Action Type")
        verbose_name_plural = _("Adaptation Action Types")

class ODS (models.Model):
    
    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=100, null=True)

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("ODS")
        verbose_name_plural = _("ODS")

class BenefitedPopulation(models.Model):

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=100, null=True)

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Benefited Population")
        verbose_name_plural = _("Benefited Populations")

class AdaptationActionInformation(models.Model):

    name = models.CharField(max_length=250, null=True)          #2.1.2
    objective = models.CharField(max_length=3000, null=True)    #2.1.3
    description = models.CharField(max_length=3000, null=True)  #2.1.4
    meta = models.CharField(max_length=3000, null=True)         #2.1.5
    expected_result = models.TextField(null=True)               #2.1.6
    potential_co_benefits = models.TextField(null=True)         #2.1.8

    adaptation_action_type = models.ForeignKey(AdaptationActionType, related_name="adaptation_action_information", null=True, on_delete=models.CASCADE) #2.1.1
    ods = models.ManyToManyField(ODS, related_name="adaptation_action_information", blank=True)                                                         #2.1.6
    benefited_population = models.ManyToManyField(BenefitedPopulation, related_name="adaptation_action_information", blank=True)                        #2.1.7

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Adaptation Action Information")
        verbose_name_plural = _("Adaptation Action Information")


class Topics(models.Model):

    code = models.CharField(max_length=3, null=True)
    description_es = models.TextField(null=True)
    description_en = models.TextField(null=True)
    
    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')


class SubTopics(models.Model):

    code = models.CharField(max_length=3, null=True)
    description_es = models.TextField(null=True)
    description_en = models.TextField(null=True)
    
    topic = models.ForeignKey(Topics, null=True, related_name="sub_topics", on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Sub Topic')
        verbose_name_plural = _('Sub Topics')


class AdaptationAxis(models.Model):

    code = models.CharField(max_length=3, null=True)
    description_es = models.TextField(null=True)
    description_en = models.TextField(null=True)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Adaptation Axis')
        verbose_name_plural = _('Adaptation Axis')


class AdaptationAxisGuideline(models.Model):

    code = models.CharField(max_length=3, null=True)
    description_es = models.TextField(null=True)
    description_en = models.TextField(null=True)

    adaptation_axis = models.ForeignKey(AdaptationAxis, null=True, related_name="adaptation_axis_guideline", on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Adaptation Axis Guideline')
        verbose_name_plural = _('Adaptation Axis Guidelines')


class NDCArea(models.Model):

    code = models.CharField(max_length=3, null=True)
    description_es = models.TextField(null=True)
    description_en = models.TextField(null=True)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('NDC Area')
        verbose_name_plural = _('NDC Areas')

class NDCContribution(models.Model):

    code = models.CharField(max_length=3, null=True)
    description_es = models.TextField(null=True)
    description_en = models.TextField(null=True)

    ndc_area = models.ForeignKey(NDCArea, null=True, related_name="ndc_contribution", on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('NDC Contribution')
        verbose_name_plural = _('NDC Contributions')    

class Activity(models.Model):

    code = models.CharField(max_length=3, null=True)
    description_es = models.TextField(null=True)
    description_en = models.TextField(null=True)
    
    sub_topic = models.ForeignKey(SubTopics, null=True, related_name="activity", on_delete=models.CASCADE)
    ndc_contribution = models.ManyToManyField(NDCContribution,related_name="activity", blank=True)
    adaptation_axis_guideline = models.ForeignKey(AdaptationAxisGuideline, null=True, related_name="activity", on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

class Instrument(models.Model):
    
    name = models.CharField(max_length=250, null=True, blank=True)  #2.4.1

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Instrument")
        verbose_name_plural = _("Instruments")


class TypeClimateThreat(models.Model):
    
    code = models.CharField(max_length=2, null=True)
    name = models.CharField(max_length=3000, null=True)

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Type Climate Threat")
        verbose_name_plural = _("Type Climate Threats")

class ClimateThreat(models.Model):

    type_climate_threat = models.ManyToManyField(TypeClimateThreat, related_name="climate_threat", blank=True)              #2.5.1
    other_type_climate_threat = models.TextField(null=True)                                                                 #2.5.1.1
    description_climate_threat = models.TextField(null=True)                                                                #2.5.2              
    file_description_climate_threat = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())  
    vulnerability_climate_threat = models.TextField(null=True)                                                              #2.5.3
    file_vulnerability_climate_threat = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    exposed_elements = models.TextField(null=True)                                                                          #2.5.4
    file_exposed_elements = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    description_losses = models.TextField(null=True)                                                                        #2.5.5
    file_description_losses = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    description_risks = models.TextField(null=True)                                                                         #2.5.6
    file_description_risks = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Type Climate Threat")
        verbose_name_plural = _("Type Climate Threats")

class Implementation(models.Model):
    
    start_date = models.DateField(null=True)                            #2.6.1
    end_date = models.DateField(null=True)                              #2.6.2
    responsible_entity = models.CharField(max_length=50, null=True, blank=True)     #2.6.4
    other_entity = models.CharField(max_length=250, null=True, blank=True)          #2.6.5
    action_code = models.TextField(null=True)                           #2.6.6

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Implementation")
        verbose_name_plural = _("Implementations")


class FinanceStatus(models.Model):

    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Finance Status")
        verbose_name_plural = _("Finance Status")

class FinanceSourceType(models.Model):

    name = models.CharField(max_length=100, blank=False, null=True)
    code = models.CharField(max_length=100, blank=False, null=True)
     
    ## Logs
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Finance Source Type")
        verbose_name_plural = _("Finance Source Types")

class FinanceInstrument(models.Model):

    name = models.CharField(max_length=100, blank=False, null=True)
    code = models.CharField(max_length=100, blank=False, null=True)
     
    ## Logs
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Finance Instrument")
        verbose_name_plural = _("Finance Instruments")

class Mideplan(models.Model):

    registry = models.CharField(max_length=2, null=True)
    name = models.CharField(max_length=300, null=True)      #3.2.1.1
    entity = models.CharField(max_length=200, null=True)    #3.2.2

    ## Logs
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Mideplan")
        verbose_name_plural = _("Mideplan")

class FinanceAdaptation(models.Model):

    administration = models.TextField(max_length=500, null=True)
    budget = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    currency = models.TextField(null=True)
    year = models.TextField(null=True)
    status = models.ForeignKey(FinanceStatus, related_name='finance_adaptation', null=True, on_delete=models.CASCADE)       #3.1.1
    source = models.ManyToManyField(FinanceSourceType, related_name='finance_adaptation', blank=True)                       #3.2.1
    finance_instrument = models.ManyToManyField(FinanceInstrument, related_name='finance_adaptation', blank=True)           #3.2.2
    instrument_name = models.TextField(null=True)
    mideplan = models.ForeignKey(Mideplan, related_name="finance_adaptation", null=True, on_delete=models.CASCADE)

    ## Logs
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Finance Adaptation")
        verbose_name_plural = _("Finance Adaptations")

class InformationSourceType(models.Model):
    name = models.CharField(max_length=500, null=True)
    code = models.CharField(max_length=500, null=True)
    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Information Source Type")
        verbose_name_plural = _("Information Source Types")


class InformationSource(models.Model):
    responsible_institution = models.CharField(max_length=500, null=True)
    type_information = models.ManyToManyField(InformationSourceType, related_name='information_source', blank=True)
    other_type = models.CharField(max_length=500, null=True)
    statistical_operation = models.CharField(max_length=500, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Information Source")
        verbose_name_plural = _("Information Sources")

class ThematicCategorizationType(models.Model):

    name = models.CharField(max_length=100, blank=False, null=True)
    code = models.CharField(max_length=100, blank=False, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Thematic Categorization Type")
        verbose_name_plural = _("Thematic Categorization Types")

class Classifier(models.Model):
    code = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Classifier")
        verbose_name_plural = _("Classifiers")

## Section: 4
class IndicatorAdaptation(models.Model):
    PERIODICITY = [
        ('YEARLY', 'Yearly'),
        ('BIANNUAL', 'Biannual'),
        ('QUARTERLY', 'Quartely'),
        ('OTHER', 'Other'),
    ]
    GEOGRAPHIC = [
        ('NATIONAL', 'National'),
        ('REGIONAL', 'Regional'),
        ('PROVINCIAL', 'Provincial'),
        ('CANTONAL', 'Cantonal'),
        ('OTHER', 'Other')
    ]
    #Section 4
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    unit = models.CharField(max_length=100, null=True)
    methodological_detail = models.TextField(null=True)
    adaptation_action = models.ForeignKey('AdaptationAction', null=True, related_name='indicator', on_delete=models.SET_NULL)
    methodological_detail_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    reporting_periodicity = models.CharField(max_length=50, choices=PERIODICITY, default='YEARLY', null=True)
    other_reporting_periodicity = models.TextField(null=True)
    
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
    indicator_base_line = models.TextField(null=True)
    file_base_line = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    
    ## FK
    ## information source
    information_source = models.ForeignKey(InformationSource, null=True, related_name='indicator_adaptation', on_delete=models.SET_NULL)
    
    ## thematic categorization
    type_of_data = models.ForeignKey(ThematicCategorizationType, null=True, related_name='indicator_adaptation', on_delete=models.PROTECT)
    other_type_of_data = models.CharField(max_length=255, blank=True, null=True)
    classifier = models.ManyToManyField(Classifier, related_name='indicator_adaptation', blank=True)
    other_classifier = models.CharField(max_length=255, blank=True, null=True)

    ## contact
    contact = models.ForeignKey(Contact, null=True, related_name='indicator_adaptation', on_delete=models.SET_NULL)


    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Indicator Adaptation")
        verbose_name_plural = _("Indicator Adaptation")
    

class ProgressLog(models.Model):

    action_status = models.CharField(max_length=25, null=True)
    progress_monitoring = models.CharField(max_length=5, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Progress Log")
        verbose_name_plural = _("Progress Logs")

class IndicatorSource(models.Model):

    code = models.CharField(max_length=255, null=True)
    name = models.TextField(null=True)
    
    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Indicator Source")
        verbose_name_plural = _("Indicator Source")

## Section: 5
class IndicatorMonitoring(models.Model):

    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    update_date = models.DateField(null=True)
    data_to_update = models.CharField(max_length=300, null=True)
    data_to_update_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())

    ## FK
    adaptation_action = models.ForeignKey('AdaptationAction', null=True, related_name='indicator_monitoring', on_delete=models.CASCADE)
    indicator_source = models.ManyToManyField(IndicatorSource, related_name='indicator_monitoring', blank=True)
    other_indicator_source = models.TextField(null=True)
    support_information = models.TextField(null=True)
    indicator = models.ForeignKey(IndicatorAdaptation, null=True, related_name='indicator_monitoring', on_delete=models.CASCADE)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Indicator Monitoring")
        verbose_name_plural = _("Indicator Monitoring")

class GeneralReport(models.Model):

    description = models.CharField(max_length=3000, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("General Report")
        verbose_name_plural = _("General Report")

class GeneralImpact(models.Model):

    code = models.CharField(max_length=2, null=True)
    name = models.CharField(max_length=255, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("General Impact")
        verbose_name_plural = _("General Impact")

class TemporalityImpact(models.Model):

    code = models.CharField(max_length=2, null=True)
    name = models.CharField(max_length=255, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Temporality Impact")
        verbose_name_plural = _("Temporality Impact")


class ActionImpact(models.Model):

    gender_equality = models.TextField(null=True)
    gender_equality_description = models.CharField(max_length=3000, null=True)
    unwanted_action = models.TextField(null=True)
    unwanted_action_description = models.CharField(max_length=3000, null=True)
    data_to_update_file_action_impact = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())

    ## FK
    general_impact = models.ForeignKey(GeneralImpact, null=True, related_name='action_impact', on_delete=models.CASCADE)
    temporality_impact = models.ManyToManyField(TemporalityImpact, related_name='action_impact', blank=True)
    ods = models.ManyToManyField(ODS, related_name='action_impact', blank=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Action Impact")
        verbose_name_plural = _("Action Impact")

class AdaptationAction(models.Model):
    
    #Section 1
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=255, null=True)
    fsm_state = models.CharField(max_length=50, default=FSM_STATE.NEW)
    report_organization = models.ForeignKey(ReportOrganization, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    #Section 2
    address = models.ForeignKey(Address, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    adaptation_action_information = models.ForeignKey(AdaptationActionInformation, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    activity = models.ManyToManyField(Activity, related_name="adaptation_action", blank=True)
    instrument = models.ForeignKey(Instrument, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    climate_threat = models.ForeignKey(ClimateThreat, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    implementation = models.ForeignKey(Implementation, related_name="adaptation_action", null=True, on_delete=models.CASCADE)

    #Section 3
    finance = models.ForeignKey(FinanceAdaptation, related_name="adaptation_action", null=True, on_delete=models.CASCADE)

    #Section 5
    progress_log = models.ForeignKey(ProgressLog, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    general_report = models.ForeignKey(GeneralReport, related_name="adaptation_action", null=True, on_delete=models.CASCADE)

    #Section 6
    action_impact = models.ForeignKey(ActionImpact, related_name="adaptation_action", null=True, on_delete=models.CASCADE)

    comments = models.ManyToManyField(Comment, blank=True)
    review_count = models.IntegerField(null=True, blank=True, default=0)
    user = models.ForeignKey(User, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Adaptation Action")
        verbose_name_plural = _("Adaptation Actions")
    

    def create_code(self):
        ##
        ## format code: AA{initiative_type}-{0000}
        ##
        if not (self.adaptation_action_information is None or self.adaptation_action_information.adaptation_action_type is None):
            with transaction.atomic():
                adaptation_action_type = AdaptationActionType.objects.select_for_update().get(pk=self.adaptation_action_information.adaptation_action_type.id)
                self.code = f'AA{adaptation_action_type.type}-{adaptation_action_type.count:0>4}'
                self.adaptation_action_information.adaptation_action_type.count += 1
                self.save()
                self.adaptation_action_information.adaptation_action_type.save()
    
    
class ChangeLog(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=False)
    # Foreign Keys
    adaptation_action = models.ForeignKey(AdaptationAction, related_name='change_log', on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=100, null=True)
    current_status = models.CharField(max_length=100)
    
    user = models.ForeignKey(User, related_name='adaptation_action_change_log', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ChangeLog")
        verbose_name_plural = _("ChangeLogs")
        ordering = ('date',)
