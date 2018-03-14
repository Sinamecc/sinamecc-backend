from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _

class ReportFile(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    file = models.FileField(blank=False, null=False, upload_to='report_data/%Y/%m/%d/%H/%M/%S')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    version = models.ManyToManyField(ReportFileVersion)

    class Meta:
        verbose_name = _("ReportFile")
        verbose_name_plural = _("ReportFiles")
        ordering = ('created',)

    def __unicode__(self):
        return smart_unicode(self.name)

class ReportFileVersion(models.Model):
    version: models.CharField(max_length=100, unique=True, blank=False, null=False)

    class Meta:
        verbose_name = _("ReportFileVersion")
        verbose_name_plural = _("ReportFileVersions")
    
    def __unicode__(self):
        return smart_unicode(self.version)


