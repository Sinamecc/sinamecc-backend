from __future__ import unicode_literals
from typing import Tuple
from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from mitigation_action.models import Contact, ThematicCategorizationType, Classifier
from general.storages import PrivateMediaStorage
from general.utils import unique_field_value_generator
from time import gmtime, strftime
import string

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

    user = models.ForeignKey(User, related_name='report_data', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    source_file = models.FileField(upload_to=directory_path, storage=PrivateMediaStorage(), blank=True, null=True)
    data_type = models.ForeignKey(ThematicCategorizationType, related_name='report_data', null=True, on_delete=models.CASCADE)
    other_data_type = models.CharField(max_length=255, blank=True, null=True)
    classifier = models.ForeignKey(Classifier, related_name='report_data', null=True, on_delete=models.CASCADE)
    other_classifier = models.CharField(max_length=255, blank=True, null=True)
    report_information = models.CharField(max_length=100, choices=REPORT_TYPE_CHOICES, blank=False, null=False)
    
    have_line_base = models.BooleanField(default=False)
    line_base_type = models.CharField(max_length=100,choices=REPORT_DATA_TYPE_CHOICES, blank=True, null=True)
    line_base_report = models.TextField(blank=True, null=True) ## can be used for the line base report or url 
    
    have_quality_element = models.BooleanField(default=False)
    quality_element_description = models.TextField(blank=True, null=True)
    transfer_data_with_sinamecc = models.BooleanField(default=False)
    transfer_data_with_sinamecc_description = models.TextField(blank=True, null=True)
    
    report_data_type = models.CharField(max_length=100, choices=REPORT_DATA_TYPE_CHOICES, blank=True, null=True)
    individual_report_data = models.TextField(blank=True, null=True) ## can be used for the individual report or url
    
    contact = models.ForeignKey(Contact, related_name='report_data', null=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Report Data")
        verbose_name_plural = _("Report Data")
        ordering = ('created',)

    def __unicode__(self):
        return smart_unicode(self.name)


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


class ReportFileMetadata(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    value = models.CharField(max_length=100, blank=False, null=False)
    report_file = models.ForeignKey(ReportFile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Report File Metadata")
        verbose_name_plural = _("Report FileMetadata")


class ReportDataChangeLog(models.Model):

    report_data = models.ForeignKey(ReportData, related_name='report_data_change_log', null=True, blank=True, on_delete=models.CASCADE)
    changes = models.TextField(null=True, blank=True)
    change_description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, related_name='report_data_change_log', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Report Data Changelog")
        verbose_name_plural = _("Report Data Changelogs")
