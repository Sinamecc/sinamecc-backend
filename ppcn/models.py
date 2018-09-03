from __future__ import unicode_literals
from mitigation_action.models import Contact
from django.conf import settings
import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from general.storages import PrivateMediaStorage
User = get_user_model()

class InventoryMethodology(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("InventoryMethodology")
        verbose_name_plural = _("InventoryMethodologies")
    
    def __unicode__(self):
        return smart_unicode(self.type)

class PotentialGlobalWarming(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("PotentialGlobalWarming")
        verbose_name_plural = _("PotentialGlobalWarmings")
    
    def __unicode__(self):
        return smart_unicode(self.type)

class EmissionFactor(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("EmissionFactor")
        verbose_name_plural = _("EmissionFactors")
    
    def __unicode__(self):
        return smart_unicode(self.type)

class GeographicLevel(models.Model):
    level_es = models.CharField(max_length=200, blank=False, null=False)
    level_en = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("GeographicLevel")
        verbose_name_plural = _("GeographicLevels")
    
    def __unicode__(self):
        return smart_unicode(self.level)

class RequiredLevel(models.Model):
    level_type_es = models.CharField(max_length=200, blank=False, null=False)
    level_type_en = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("RequiredLevel")
        verbose_name_plural = _("RequiredLevels")

    def __unicode__(self):
        return smart_unicode(self.level)

class RecognitionType(models.Model):
    recognition_type_es = models.CharField(max_length=200, blank=False, null=False)
    recognition_type_en = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("RecognitionType")
        verbose_name_plural = _("RecognitionTypes")

    def __unicode__(self):
        return smart_unicode(self.recognition_type)


class QuantifiedGas(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("QuantifiedGas")
        verbose_name_plural = _("QuantifiedGases")
    
    def __unicode__(self):
        return smart_unicode(self.type)

class PlusAction(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("PlusAction")
        verbose_name_plural = _("PlusActions")
    
    def __unicode__(self):
        return smart_unicode(self.type)

class Organization(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    representative_name = models.CharField(max_length=200, blank=False, null=False)
    phone_organization = models.CharField(max_length=200, blank=False, null=True)
    postal_code = models.CharField(max_length=200, blank=True, null=True)
    fax = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=False, null=False)
    contact = models.ForeignKey(Contact, related_name='organization', on_delete=models.CASCADE)
    ciiu = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __unicode__(self):
        return smart_unicode(self.name)

class Sector(models.Model):
    name_es = models.CharField(max_length=200, blank=False, null=False)
    name_en = models.CharField(max_length=200, blank=False, null=False)
    geographicLevel = models.ForeignKey(GeographicLevel, blank = False, null = False)

    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")

    def __unicode__(self):
        return smart_unicode(self.name)

class SubSector(models.Model):
    name_es = models.CharField(max_length=200, blank=False, null=False)
    name_en = models.CharField(max_length=200, blank=False, null=False)
    sector = models.ForeignKey(Sector, related_name='sector')
    class Meta:
        verbose_name = _("SubSector")
        verbose_name_plural = _("SubSectors")

    def __unicode__(self):
        return smart_unicode(self.name)


class GeiOrganization(models.Model):

    activity_type = models.CharField(max_length=200, blank=False, null=False)
    ovv = models.CharField(max_length=200, blank=False, null=False)
    emision_OVV = models.DateField(null=False)
    report_date = models.DateField(null=False)
    base_year = models.DateField(null=False)

    class Meta:
        verbose_name = _("GeiOrganization")
        verbose_name_plural = _("GeiOrganization")

    def __unicode__(self):
        return smart_unicode(self.activity_type)



class PPCN(models.Model):
    
    organization = models.ForeignKey(Organization, related_name='organization', on_delete=models.CASCADE)
    geographicLevel = models.ForeignKey(GeographicLevel, related_name='geographicLevel')
    requiredLevel = models.ForeignKey(RequiredLevel, related_name='requiredLevel')
    sector = models.ForeignKey(Sector, null = False, blank = False)
    subsector = models.ForeignKey(SubSector, related_name='subsector')
    recognitionType = models.ForeignKey(RecognitionType, related_name='recognization')
    base_year = models.DateField(null = False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('PPCN')
        verbose_name_plural = _('PPCNs')
    
    def __unicode__(self):
        return smart_unicode(self.type)


class PPCNFile(models.Model):

    user = models.ForeignKey(User, related_name='ppcn_file')
    file = models.FileField(blank = False, null = False, upload_to='ppcn/files/%Y%m%d/%H%M%S',storage=PrivateMediaStorage())
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    ppcn_form = models.ForeignKey(PPCN, related_name = "files", blank = False, null= False, on_delete=models.CASCADE)

    class meta:
        verbose_name = _('ppcn_file')
        verbose_name_plural = _('ppcn_files')

    def __unicode__(self):
        return smart_unicode(self.name)
