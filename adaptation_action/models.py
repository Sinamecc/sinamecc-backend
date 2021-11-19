import uuid
from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import flatten_choices_dict
from mitigation_action.models import Contact, Finance, Indicator, MonitoringIndicator
from general.models import Address

# Create your models here.

class ReportOrganizationType(models.Model): 
    #Generar data por defecto!
    code = models.CharField(max_length=3, null=True)
    entity_type = models.CharField(max_length=100, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Report Organization Type")
        verbose_name_plural = _("Report Organization Types")

class ReportOrganization(models.Model):

    responsible_entity = models.CharField(max_length=200, null=True)
    legal_identification = models.CharField(max_length=50, null=True)
    elaboration_date = models.DateField(null=True)
    entity_address = models.CharField(max_length=250, null=True)
    
    report_organization_type = models.ForeignKey(ReportOrganizationType, related_name="report_organization", null=True, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, related_name="report_organization", null=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Report Organization")
        verbose_name_plural = _("Report Organizations")

class AdaptationActionType(models.Model):

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=100, null=True)

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

class AdaptationActionInformation(models.Model):

    name = models.CharField(max_length=250, null=True)
    objective = models.CharField(max_length=3000, null=True)
    description = models.CharField(max_length=3000, null=True)
    meta = models.CharField(max_length=3000, null=True)

    adaptation_action_type = models.ForeignKey(AdaptationActionType, related_name="adaptation_action_information", null=True, on_delete=models.CASCADE)
    ods = models.ManyToManyField(ODS, related_name="adaptation_action_information", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Adaptation Action Information")
        verbose_name_plural = _("Adaptation Action Information")


class Topics(models.Model):

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=255, null=True)
    
    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')


class SubTopics(models.Model):

    code = models.CharField(max_length=3, null=False)
    name = models.CharField(max_length=255, null=False)
    
    topic = models.ForeignKey(Topics, null=False, related_name="sub_topics", on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Sub Topic')
        verbose_name_plural = _('Sub Topics')


class AdaptationAxis(models.Model):

    code = models.CharField(max_length=3, null=False)
    description = models.CharField(max_length=500, null=False)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Adaptation Axis')
        verbose_name_plural = _('Adaptation Axis')


class AdaptationAxisGuideline(models.Model):

    code = models.CharField(max_length=3, null=False)
    name = models.CharField(max_length=500, null=False)

    adaptation_axis = models.ForeignKey(AdaptationAxis, null=False, related_name="adaptation_axis_guideline", on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Adaptation Axis Guideline')
        verbose_name_plural = _('Adaptation Axis Guidelines')


class AdaptationGuideline(models.Model):

    code = models.CharField(max_length=3, null=False)
    name = models.CharField(max_length=500, null=False)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Adaptation Guideline')
        verbose_name_plural = _('Adaptation Guidelines')

class AdaptationGuidelineMeta(models.Model):

    code = models.CharField(max_length=3, null=False)
    meta = models.CharField(max_length=500, null=False)

    adaptation_guideline = models.ForeignKey(AdaptationGuideline, null=False, related_name="adaptation_guideline_meta", on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Adaptation Guideline Meta')
        verbose_name_plural = _('Adaptation Guideline Meta')

class NDCArea(models.Model):

    code = models.CharField(max_length=3, null=False)
    description = models.CharField(max_length=500, null=False)
    other = models.CharField(max_length=500, null=True)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('NDC Area')
        verbose_name_plural = _('NDC Areas')

class NDCContribution(models.Model):

    code = models.CharField(max_length=3, null=False)
    description = models.CharField(max_length=500, null=False)
    other = models.CharField(max_length=500, null=True)

    ndc_area = models.ForeignKey(NDCArea, null=False, related_name="ndc_contribution", on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('NDC Contribution')
        verbose_name_plural = _('NDC Contributions')    

class Activity(models.Model):

    code = models.CharField(max_length=3, null=True)
    description = models.CharField(max_length=250, null=True)
    
    sub_topic = models.ForeignKey(SubTopics, null=False, related_name="activity", on_delete=models.CASCADE)
    adaptation_guideline_meta = models.ForeignKey(AdaptationGuidelineMeta, null=False, related_name="activity", on_delete=models.CASCADE)
    ndc_contribution = models.ManyToManyField(NDCContribution, null=False, related_name="activity", blank=True)
    adaptation_axis_guideline = models.ForeignKey(AdaptationAxisGuideline, null=False, related_name="activity", on_delete=models.CASCADE)

    ## logs
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

class Instrument(models.Model):
    
    name = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=3000, null=True)

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Instrument")
        verbose_name_plural = _("Instruments")


class TypeClimatedThreat(models.Model):
    #Generar data por defecto
    code = models.CharField(max_length=2, null=True)
    name = models.CharField(max_length=3000, null=True)

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Type Climated Threat")
        verbose_name_plural = _("Type Climated Threats")

class ClimateThreat(models.Model):

    #archivo 
    type_climated_threat = models.ForeignKey(TypeClimatedThreat, related_name="climate_threat", null=True, on_delete=models.CASCADE)

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Type Climated Threat")
        verbose_name_plural = _("Type Climated Threats")

class Implementation(models.Model):
    
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    duration = models.CharField(max_length=20, null=True)
    responsible_entity = models.CharField(max_length=50, null=True)
    other_entity = models.CharField(max_length=250, null=True)
    action_code = models.CharField(max_length=3, null=True)

    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Implementation")
        verbose_name_plural = _("Implementations")

class AdaptationAction(models.Model):
    #Section 1
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    report_organization = models.ForeignKey(ReportOrganization, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    #Section 2
    address = models.ForeignKey(Address, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    adaptation_action_information = models.ForeignKey(AdaptationActionInformation, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    climate_threat = models.ForeignKey(ClimateThreat, related_name="adaptation_action", null=True, on_delete=models.CASCADE)
    implementation = models.ForeignKey(Implementation, related_name="adaptation_action", null=True, on_delete=models.CASCADE)


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Adaptation Action")
        verbose_name_plural = _("Adaptation Actions")


