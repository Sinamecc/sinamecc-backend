from django.db import models
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
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