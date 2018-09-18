from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from general.storages import PrivateMediaStorage
from ppcn.models import PPCN
from time import gmtime, strftime

User = get_user_model()


def workflow_step_directory_path(instance, filename):
    dayly_date_segment = strftime("%Y%m%d", gmtime())
    hourly_date_segment = strftime("%H%M%S", gmtime())
    return "ppcn/workflow_steps/{0}/{1}/{2}/{3}".format(instance.workflow_step.name, dayly_date_segment, hourly_date_segment, filename)


class PPCNWorkflowStep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ppcn = models.ForeignKey(PPCN, related_name='workflow_step', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    entry_name = models.CharField(max_length=100, blank=False, null=False)
    status = models.CharField(max_length=50, blank=True) # Accepted, Rejected, Commented
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Workflow Step")
        verbose_name_plural = _("Workflow Steps")

    def __unicode__(self):
        return smart_unicode("{} - {}".format(self.name, self.entry_name))


class PPCNWorkflowStepFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workflow_step = models.ForeignKey(PPCNWorkflowStep,related_name='files', on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False, upload_to=workflow_step_directory_path, storage=PrivateMediaStorage())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Workflow Step File")
        verbose_name_plural = _("Workflow Step Files")

    def __unicode__(self):
        return smart_unicode("{} - {}".format(self.workflow_step.name, self.file.name))