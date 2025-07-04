from __future__ import unicode_literals

import uuid
from time import gmtime, strftime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils.encoding import smart_str as smart_unicode
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

from general.helpers.validators import validate_year
from general.permissions import PermissionsHelper
from general.services import EmailServices
from general.storages import PrivateMediaStorage
from mitigation_action.services.emails import (
    EmailServices as MitigationActionEmailServices,
)
from workflow.models import Comment, ReviewStatus

from .constants import MitigationActionFilesType
from .workflow.states import States as FSM_STATE

User =  get_user_model()
permission = PermissionsHelper()

CURRENCIES = (('CRC', _('Costa Rican colon')), ('USD', _('United States dollar')),  ('EUR', 'Euro'))
##
## Start Catalogs
##
def directory_path(instance, filename): 
    path = "mitigation_action/{0}/{1}/{2}/"

    return path.format(instance._meta.verbose_name, strftime("%Y%m%d", gmtime()), filename)

"""
Refactor of some models to optimize the database structure and avoid redundancy.
The first step is consolidating the file fields, basically, save all file into one model with metadata
and then link it to the models that need it or with the main model (MitigationAction).
"""

def _directory_file_path(instance: "GenericFileStorage", filename: str) -> str:

    path = 'mitigation_action/{type}/{object_id}/files/{filename}'

    return path.format(
        object_id=instance.object_id,
        type=instance.type,
        filename=str(uuid.uuid4())
    )

class GenericFileStorage(models.Model):
    """
    A model to store files with generic relation to any model.
    This model allows to store files with metadata and link them to any model using GenericForeignKey.
    How to use:
    1. mitigation_action.generic_files

    """
    file = models.FileField(upload_to=_directory_file_path)
    type = models.CharField(max_length=50, choices=MitigationActionFilesType.choices())
    metadata = models.JSONField(blank=True, null=True)

    ## Get All files from records and sub records
    mitigation_action = models.ForeignKey(
        'MitigationAction',
        related_name='generic_files',
        on_delete=models.CASCADE,
    )

    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Generic File Storage')
        verbose_name_plural = _('Generic File Storage')
        

class Sector(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name_es = models.TextField()
    name_en = models.TextField()

    ##logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')
    
    def __repr__(self) -> str:
        return '{}: {}'.format(self.code, self.name_es)
    
    def __str__(self):
        return self.code + ":" +self.name_es + '::' + self.name_en
    


class SectorIPCC2006(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name_es = models.TextField()
    name_en = models.TextField()
    sector = models.ForeignKey(Sector, related_name='sector_ipcc_2006', on_delete=models.CASCADE)
    
    ##logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Sector IPCC2006')
        verbose_name_plural = _('Sectors IPCC2006')
        
    def __str__(self):
        return self.code + ":" +self.name_es + '::' + self.name_en + ':::' + self.sector.name_es


class CategoryIPCC2006(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name_es = models.TextField()
    name_en = models.TextField()
    sector_ipcc_2006 = models.ForeignKey(SectorIPCC2006, related_name='category_ipcc_2006', on_delete=models.CASCADE)
    ##logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Category IPCC2006')
        verbose_name_plural = _('Categories IPCC2006')
        
        
    def __str__(self):
        return self.code + ":" +self.name_es + '::' + self.name_en + ':::' + self.sector_ipcc_2006.name_es


class SubCategoryIPCC2006(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name_es = models.TextField()
    name_en = models.TextField()
    category_ipcc_2006 = models.ForeignKey(CategoryIPCC2006, related_name='sub_sector_ipcc2006', on_delete=models.CASCADE)
    
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Subcategory IPCC2006')
        verbose_name_plural = _('Subcategories IPCC2006')
        
    def __str__(self):
        return self.code + ":" +self.name_es + '::' + self.name_en + ':::' + self.category_ipcc_2006.name_es

class CarbonDeposit(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name_es = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)

    ##logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Carbon Deposit')
        verbose_name_plural = _('Carbon Deposits')


class Standard(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name_es = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)

    ##logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Standar')
        verbose_name_plural = _('Standars')


class SustainableDevelopmentGoals(models.Model): 
    code = models.CharField(max_length=255, blank=True, null=True)
    description_es = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Sustainable Development Goal")
        verbose_name_plural = _("Sustainable Development Goals")


class GHGImpactSector(models.Model):

    code = models.CharField(max_length=255, blank=True, null=True)
    name_es = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("GHG Impact Sector")
        verbose_name_plural = _("GHG Impact Sectors")


class ActionAreas(models.Model):
    name_es = models.CharField(max_length=255, null=False, blank=False)
    name_en = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(max_length=3, null=False, blank=False)
    
    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Action Area')
        verbose_name_plural = _('Action Areas')


class ActionGoals(models.Model):

    goal_es = models.TextField()
    goal_en = models.TextField()
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
    description_es = models.TextField()
    description_en = models.TextField()

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Descarbonization Axis')
        verbose_name_plural = _('Descarbonization Axes')


class TransformationalVisions(models.Model):

    code = models.CharField(max_length=3, null=False, blank=False)
    description_es = models.TextField()
    description_en = models.TextField()
    axis = models.ForeignKey(DescarbonizationAxis, null=False, related_name='transformational_vision', on_delete=models.CASCADE)
    
    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Transformational Vision')
        verbose_name_plural = _('Transformational Visions')


class Topics(models.Model):

    code = models.CharField(max_length=3, null=False, blank=False)
    name_es = models.CharField(max_length=255, null=False, blank=False)
    name_en = models.CharField(max_length=255, null=False, blank=False)
    
    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')


class SubTopics(models.Model):

    code = models.CharField(max_length=3, null=False, blank=False)
    name_es = models.CharField(max_length=255, null=False, blank=False)
    name_en = models.CharField(max_length=255, null=False, blank=False)
    topic = models.ForeignKey(Topics, null=False, related_name='sub_topic', on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Sub Topic')
        verbose_name_plural = _('Sub Topics')


class Activity(models.Model):

    code = models.CharField(max_length=3, null=False, blank=False)
    description_es = models.TextField()
    description_en = models.TextField()
    sub_topic = models.ForeignKey(SubTopics, null=False, related_name='activity', on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')


class ImpactCategory(models.Model):

    code = models.CharField(max_length=255, null=False, blank=False)
    name_es = models.CharField(max_length=255, null=False, blank=False)
    name_en = models.CharField(max_length=255, null=False, blank=False)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Impact Category')
        verbose_name_plural =  _('Impact Categories')


class InitiativeType(models.Model):

    name_es = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)
    type = models.CharField(max_length=2, blank=False, null=False)
    count = models.IntegerField(default=0)
     
    ## Logs
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Initiative Type")
        verbose_name_plural = _("Initiative Types")

    def __unicode__(self):
        return smart_unicode(self.initiative_type_en)


class GeographicScale(models.Model):

    name_es = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=False, null=False)
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

    name_es = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=False, null=False)
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
    
    name_es = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=False, null=False)
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

    status_es = models.CharField(max_length=100, blank=False, null=False)
    status_en = models.CharField(max_length=100, blank=False, null=False)
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

    name_es = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Thematic Categorization Type")
        verbose_name_plural = _("Thematic Categorization Types")

## section 5 new
class InformationSourceType(models.Model):
    name_es = models.CharField(max_length=500, null=True)
    name_en = models.CharField(max_length=500, null=True)
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
    name_es = models.CharField(max_length=255, null=True)
    name_en = models.CharField(max_length=255, null=True)

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
    carbon_deposit = models.ManyToManyField(CarbonDeposit, blank=True, related_name='impact_documentation')
    gases = models.TextField(null=True) # separate by commas CO2, CH4, N2O
    base_line_definition = models.TextField(null=True)
    calculation_methodology = models.TextField(null=True)
    estimate_calculation_documentation = models.TextField(null=True)
    #estimate_calculation_documentation_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    mitigation_action_in_inventory = models.CharField(max_length=50, null=True)

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
    
    impact_category = models.ForeignKey(ImpactCategory, related_name='categorization', blank=True, null=True, on_delete=models.PROTECT)
    is_part_to_another_mitigation_action = models.BooleanField(null=True)
    relation_description = models.TextField(max_length=255, blank=True, null=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Categorization")
        verbose_name_plural = _("Categorization")


## multiselection of the same model
## section 1
class TopicsSelection(models.Model):
    topic = models.ForeignKey(Topics, null=True, related_name='topics_selection', on_delete=models.CASCADE)
    sub_topic = models.ManyToManyField(SubTopics, related_name='topics_selection')
    categorization = models.ForeignKey(Categorization, null=True, related_name='topics_selection', on_delete=models.CASCADE)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

class ActionAreasSelection(models.Model):
    area = models.ForeignKey(ActionAreas, null=False, related_name='action_area_selection', on_delete=models.CASCADE)
    categorization = models.ForeignKey(Categorization, null=False, related_name='action_area_selection', on_delete=models.CASCADE)
    goals = models.ManyToManyField(ActionGoals, related_name='action_area_selection', blank=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

class DescarbonizationAxisSelection(models.Model):
    descarbonization_axis = models.ForeignKey(DescarbonizationAxis, related_name='descarbonization_axis_selection', on_delete=models.CASCADE)
    categorization = models.ForeignKey(Categorization, related_name='descarbonization_axis_selection', blank=True, on_delete=models.CASCADE)
    transformational_vision = models.ManyToManyField(TransformationalVisions, related_name='descarbonization_axis_selection', blank=True)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



## section #4 selection of sector
class SectorSelection(models.Model):
    sector = models.ForeignKey(Sector, related_name='sector_selection', on_delete=models.CASCADE)
    sector_ipcc_2006 = models.ForeignKey(SectorIPCC2006, related_name='sector_selection', on_delete=models.CASCADE)
    category_ipcc_2006 = models.ForeignKey(CategoryIPCC2006, related_name='sector_selection', on_delete=models.CASCADE)
    sub_category_ipcc_2006 = models.ManyToManyField(SubCategoryIPCC2006, related_name='sector_selection')
    impact_documentation = models.ForeignKey(ImpactDocumentation, related_name='sector_selection', on_delete=models.CASCADE)
    
    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


## section 5 new
class InformationSource(models.Model):
    responsible_institution = models.CharField(max_length=500, null=True)
    type = models.ManyToManyField(InformationSourceType, blank=True, related_name='information_source')
    other_type = models.CharField(max_length=500, blank=True, null=True)
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
        ('QUARTERLY', 'Quartely'),
        ('OTHER', 'Other')
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
    #methodological_detail_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    reporting_periodicity = models.TextField(max_length=50, choices=PERIODICITY, default='YEARLY', null=True)
    
    available_time_start_date = models.DateField(null=True)
    available_time_end_date = models.DateField(null=True)

    ghg_indicator_goal = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    ghg_indicator_base = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    geographic_coverage = models.CharField(max_length=255, choices=GEOGRAPHIC, default='NATIONAL', null=True)
    other_geographic_coverage = models.CharField(max_length=255, blank=True, null=True)
    
    disaggregation = models.TextField(null=True)

    classifier = models.ManyToManyField(Classifier, related_name='indicator', blank=True)
    other_classifier = models.CharField(max_length=255, blank=True, null=True)
    
    limitation = models.TextField(null=True)
    ensure_sustainability = models.TextField(null=True)
    ## need to endpoint to upload file
    #ensure_sustainability_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    
    comments = models.TextField(null=True)
    ## FK
    ## information source
    information_source = models.ForeignKey(InformationSource, null=True, related_name='indicator', on_delete=models.SET_NULL)
    
    ## thematic categorization
    type_of_data = models.ForeignKey(ThematicCategorizationType, null=True, related_name='indicator', on_delete=models.PROTECT)
    other_type_of_data = models.CharField(max_length=255, blank=True, null=True)

    ## contact
    contact = models.ForeignKey(Contact, null=True, related_name='indicator', on_delete=models.SET_NULL)
    monitoring_information = models.ForeignKey(MonitoringInformation, related_name='indicator', null=True, on_delete=models.CASCADE)
    files = GenericRelation(GenericFileStorage, related_query_name='indicator_files')

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
    report_type = models.TextField(null=True)
    updated_data = models.CharField(max_length=150, null=True)
    #updated_data_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    report_line_text = models.TextField(null=True)
    #report_line_text_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    web_service_conection = models.TextField(null=True)
    #web_service_conection_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
    
    progress_report_period = models.DateField(null=True)
    progress_report_period_until = models.DateField(null=True)
    progress_report = models.TextField(null=True)

    ## FK 
    indicator = models.ForeignKey(Indicator, related_name='monitoring_indicator', null=True, on_delete=models.CASCADE)
    monitoring_reporting_indicator = models.ForeignKey(MonitoringReportingIndicator, related_name='monitoring_indicator', null=True, on_delete=models.CASCADE)

    files = GenericRelation(GenericFileStorage, related_query_name='monitoring_indicator_files')
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
    is_checked = models.BooleanField(null=True)
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
    administration = models.TextField(null=True) ## !! review this
    source = models.ManyToManyField(FinanceSourceType, related_name='finance', blank=True)
    
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


class FinanceInformation(models.Model):

    source_description = models.CharField(max_length=255, null=True)
    budget = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    currency = models.TextField(null=True)
    reference_year =models.DateField(null=True)
    finance = models.ForeignKey(Finance, related_name='finance_information', null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Finance Information")
        verbose_name_plural = _("Finance Information")


class GeographicLocation(models.Model):

    geographic_scale = models.ForeignKey(GeographicScale, related_name='geographic_location', null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=254, null=True)
    #location_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
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
    #description_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
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
    #graphic_description_file = models.FileField(null=True, upload_to=directory_path, storage=PrivateMediaStorage())
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
    code = models.CharField(max_length=255, null=True, unique=True)
    fsm_state = models.CharField(max_length=50, default=FSM_STATE.NEW)
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


    ## Save files 
    files = GenericRelation('mitigation_action.GenericFileStorage', content_type_field='content_type', object_id_field='object_id')
    ## comments
    review_count = models.IntegerField(null=True, blank=True, default=0)
    comments = models.ManyToManyField(Comment, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Mitigation Action")
        verbose_name_plural = _("Mitigation Actions")
        ordering = ('created',)

    
    def create_code(self):
        ##
        ## format code: AM{initiative_type}-{0000}
        ##
        if not (self.initiative is None or self.initiative.initiative_type is None):
            with transaction.atomic():
                initiative_type = InitiativeType.objects.select_for_update().get(pk=self.initiative.initiative_type.id)
                self.code = f'AM{initiative_type.type}-{initiative_type.count:0>4}'
                self.initiative.initiative_type.count += 1
                
                self.save()
                self.initiative.initiative_type.save()
            
    
    
    

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
