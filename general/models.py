from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str as smart_unicode
from django.utils.translation import gettext_lazy as _
from general.storages import PrivateMediaStorage
User = get_user_model()
# Create your models here.
# base models for workflowStep 
class BaseWorkflowStep(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ##app = models.ForeignKey(models-app(PPCN, MA, MCCR), related_name='workflow_step', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    entry_name = models.CharField(max_length=100, blank=False, null=False)
    status = models.CharField(max_length=50, blank=True) # Accepted, Rejected, Commented
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Workflow Step")
        verbose_name_plural = _("Workflow Steps")
        abstract = True

    def __unicode__(self):
        return smart_unicode("{} - {}".format(self.name, self.entry_name))

class BaseWorkflowStepFile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Workflow Step File")
        verbose_name_plural = _("Workflow Step Files")
        abstract = True

    def __unicode__(self):
        return smart_unicode("{} - {}".format(self.workflow_step.name, self.file.name))

class Province(models.Model):

    name = models.CharField(max_length=25, null=True)
    code = models.CharField(max_length=3, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")

class Canton(models.Model):
    
    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=3, null=True)
    
    province = models.ForeignKey(Province, related_name="canton", null=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Canton")
        verbose_name_plural = _("Cantons")

class District(models.Model):
    
    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=3, null=True)
    
    canton = models.ForeignKey(Canton, related_name="district", null=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

class Address(models.Model):

    app_scale = models.TextField(null=True)
    description = models.CharField(max_length=3000, null=True)
    GIS = models.CharField(max_length=200, null=True)

    district = models.ManyToManyField(District, related_name="address", blank=True)
    canton = models.ManyToManyField(Canton, related_name="address", blank=True)
    province = models.ManyToManyField(Province, related_name="address", blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = ("Addresses")

##use in aa & ma
class Dimension(models.Model): #Section: 7

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=100, null=True) # 7.1.1.1

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Dimension")
        verbose_name_plural = _("Dimensions")


class CategoryGroup(models.Model):

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=100, null=True) # 7.1.1.2
    dimension = models.ForeignKey(Dimension, related_name='category_group', null=True, on_delete=models.CASCADE)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    class Meta:
        verbose_name = _("Category Group")
        verbose_name_plural = _("Category Groups")


class Category(models.Model):

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=200, null=True) # 7.1.1.3
    category_group = models.ForeignKey(CategoryGroup, related_name='category', null=True, on_delete=models.CASCADE)

    ## Logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

#use in section 8 aa & ma

class CategoryCT(models.Model):

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=200, null=True) 

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Category CT")
        verbose_name_plural = _("Categories CT")


class Characteristic(models.Model):

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=200, null=True)
    category_ct = models.ForeignKey(CategoryCT, related_name="characteristics", null=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Characteristic")
        verbose_name_plural = _("Characteristics")