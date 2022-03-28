from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from mitigation_action.models import Contact, ThematicCategorizationType, Classifier, InformationSourceType
from general.storages import PrivateMediaStorage
from general.utils import unique_field_value_generator
from time import gmtime, strftime
import string
from django_fsm import FSMField, transition

import report_data

User =  get_user_model()


def directory_path(instance, filename): 
    path = "report_data/{0}/{1}/{2}/"

    return path.format(instance._meta.verbose_name, strftime("%Y%m%d", gmtime()), filename)


class ReportData(models.Model):
    ## report information choices
    REPORT_TYPE_CHOICES = (
        ('statistics_or_variable', _('Statistics or Variable')),
        ('indicator', _('Indicator')),
        ('data_base', _('Data Base')),
    )
    REPORT_DATA_TYPE_CHOICES = (
        ('upload_files', _('Upload Files')),
        ('individual_report', _('Individual Report')),
        ('url', _('url')),
    )

    PERIODICITY = (
        ('yearly', 'Yearly'),
        ('biannual', 'Biannual'),
        ('quartely', 'Quartely'),
        ('other', 'Other'),
    )
    
    GEOGRAPHIC = (
        ('NATIONAL', 'National'),
        ('REGIONAL', 'Regional'),
        ('PROVINCIAL', 'Provincial'),
        ('CANTONAL', 'Cantonal'),
        ('OTHER', 'Other')
    )
    fsm_state = FSMField(default='new', protected=True, max_length=100)
    user = models.ForeignKey(User, related_name='report_data', on_delete=models.CASCADE)
    
    # sec 2
    ###
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    calculation_methodology = models.CharField(max_length=1000, blank=True, null=True)
    measurement_frequency = models.CharField(max_length=100, choices=PERIODICITY, blank=True, null=True)
    measurement_frequency_other = models.CharField(max_length=255, blank=True, null=True)
    ## available time field
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    geographic_coverage = models.CharField(max_length=255, choices=GEOGRAPHIC, null=True)
    geographic_coverage_other = models.CharField(max_length=255, blank=True, null=True)
    disaggregation = models.TextField(null=True)
    limitation = models.TextField(null=True)
    additional_information = models.TextField(null=True)
    sustainable = models.TextField(null=True)
    ## information source 
    responsible_institution = models.CharField(max_length=500, blank=True, null=True)
    information_source = models.ForeignKey(InformationSourceType, related_name='report_data', on_delete=models.DO_NOTHING, null=True)
    statistical_operation = models.TextField(null=True)
    contact = models.ForeignKey(Contact, related_name='report_data', null=True, on_delete=models.CASCADE)
    contact_annotation = models.TextField(null=True)
    
    ## Categorization of report data
    data_type = models.ForeignKey(ThematicCategorizationType, related_name='report_data', null=True, on_delete=models.DO_NOTHING)
    other_data_type = models.CharField(max_length=255, blank=True, null=True)
    classifier = models.ManyToManyField(Classifier, related_name='report_data')
    other_classifier = models.CharField(max_length=255, blank=True, null=True)
    ###
    # sec 1.2 
    report_information = models.CharField(max_length=100, choices=REPORT_TYPE_CHOICES, blank=False, null=False)
    have_base_line = models.BooleanField(default=False)
    base_line_type = models.CharField(max_length=100,choices=REPORT_DATA_TYPE_CHOICES, blank=True, null=True)
    base_line_report = models.TextField(blank=True, null=True) ## can be used for the line base report or url 
    have_quality_element = models.BooleanField(default=False)
    quality_element_description = models.TextField(blank=True, null=True)
    transfer_data_with_sinamecc = models.BooleanField(default=False)
    transfer_data_with_sinamecc_description = models.TextField(blank=True, null=True)
    #attr report_data -> File in the report_data Report File model
    report_data_type = models.CharField(max_length=100, choices=REPORT_DATA_TYPE_CHOICES, blank=True, null=True)
    individual_report_data = models.TextField(blank=True, null=True) ## can be used for the individual report or url
    
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Report Data")
        verbose_name_plural = _("Report Data")
        ordering = ('created',)

    def __unicode__(self):
        return smart_unicode(self.name)

    
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
        print(f'The report data is transitioning from <{self.fsm_state}> to <submitted>')
        ...
        ## maybe raise exception

    
    @transition(field='fsm_state', source='submitted', target='in_evaluation_by_DCC', conditions=[can_evaluate_by_DCC], on_error='submitted', permission='')
    def evaluate_by_DCC(self):
        # submitted --> in_evaluation_by_DCC
        # send email to user that submitted the action
        print('The report data is transitioning from <submitted> to <in_evaluation_by_DCC>')
        ...
        ## maybe raise exception

    ##
    ## rejected_by_DCC, requested_changes_by_DCC, accepted_by_DCC
    ##
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='rejected_by_DCC', conditions=[can_rejected_by_DCC], on_error='in_evaluation_by_DCC', permission='')
    def evaluate_by_DCC_rejected(self):
        # in_evaluation_by_DCC --> rejected_by_DCC
        # send email to user that submitted the action
        print('The report data is transitioning from <in_evaluation_by_DCC> to <rejected_by_DCC>')
        ...
        ## maybe raise exception
    
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='requested_changes_by_DCC', conditions=[can_request_changes_by_DCC], on_error='in_evaluation_by_DCC', permission='')
    def evaluate_by_DCC_requested_changes(self):
        # in_evaluation_by_DCC --> requested_changes_by_DCC
        # send email to user that submitted the action
        print('The report data is transitioning from <in_evaluation_by_DCC> to <requested_changes_by_DCC>')
        ...
    
    @transition(field='fsm_state', source='in_evaluation_by_DCC', target='accepted_by_DCC', conditions=[can_acception_by_DCC], on_error='in_evaluation_by_DCC', permission='')
    def evaluate_by_DCC_accepted(self):
        # in_evaluation_by_DCC --> accepted_by_DCC
        # send email to user that submitted the action
        print('The report data is transitioning from <in_evaluation_by_DCC> to <accepted_by_DCC>')
        ...
            ## maybe raise exception
    
    ## rejected by DCC to end
    @transition(field='fsm_state', source='rejected_by_DCC', target='end', conditions=[], on_error='rejected_by_DCC', permission='')
    def rejected_by_DCC_to_end(self):
        # rejected_by_DCC --> rejected_by_DCC
        # send email to user that submitted the action
        print('The report data is transitioning from <rejected_by_DCC> to <end>')
        ...
    
    @transition(field='fsm_state', source='requested_changes_by_DCC', target='updating_by_request_DCC', conditions=[can_update_by_DCC_request], on_error='requested_changes_by_DCC', permission='')
    def update_by_DCC_request(self):
        # requested_changes_by_DCC --> updating_by_request_DCC
        # send email to user that submitted the action
        print('The report data is transitioning from <requested_changes_by_DCC> to <updating_by_request_DCC>')
        ...
    
    ## accepted_by_DCC to	registered_by_DCC
    @transition(field='fsm_state', source='accepted_by_DCC', target='registered_by_DCC', conditions=[], on_error='accepted_by_DCC', permission='')
    def registered_by_DCC(self):
        # accepted_by_DCC --> registered_by_DCC
        # send email to user that submitted the action
        print('The report data is transitioning from <accepted_by_DCC> to <registered_by_DCC>')
        ...


class Report(models.Model):
    user = models.ForeignKey(User, related_name='report', on_delete=models.CASCADE)
    report_data = models.ForeignKey(ReportData, related_name='report', on_delete=models.CASCADE)
    version = models.CharField(max_length=100, unique=True, blank=False, null=False)
    active = models.BooleanField(blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Report")
    
    def __unicode__(self):
        return smart_unicode(self.version)


class ReportFile(models.Model):

    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)
    file = models.FileField(upload_to=directory_path, storage=PrivateMediaStorage(), blank=True, null=True)
    report_data = models.ForeignKey(ReportData, related_name='report_file', on_delete=models.CASCADE, null=True)
    report_type = models.CharField(max_length=100, null=True) ## base_line_indicator | report_data
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Report File")
        verbose_name_plural = _("Report Files")

    def _create_slug(self):
        symbols = string.ascii_letters + '-'
        return unique_field_value_generator(self, 20, 'slug', symbols)


    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = self._create_slug()
        
        super(ReportFile, self).save(*args, **kwargs)

class ReportDataChangeLog(models.Model):

    report_data = models.ForeignKey(ReportData, related_name='report_data_change_log', null=True, blank=True, on_delete=models.CASCADE)
    changes = models.TextField(null=True, blank=True)
    change_description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, related_name='report_data_change_log', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Report Data Changelog")
        verbose_name_plural = _("Report Data Changelogs")

