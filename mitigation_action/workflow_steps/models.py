from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from general.storages import PrivateMediaStorage
from mitigation_action.models import Mitigation
from time import gmtime, strftime

User = get_user_model()


def workflow_step_directory_path(instance, filename):
    dayly_date_segment = strftime("%Y%m%d", gmtime())
    hourly_date_segment = strftime("%H%M%S", gmtime())
    return "mitigation_actions/workflow_steps/{0}/{1}/{2}/{3}".format(instance.workflow_step.name, dayly_date_segment,
                                                                      hourly_date_segment, filename)


class MAWorkflowStep(models.Model):
    user = models.ForeignKey(User, related_name='workflow_step')
    mitigation_action = models.ForeignKey(Mitigation, on_delete=models.CASCADE)
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


class MAWorkflowStepFile(models.Model):
    user = models.ForeignKey(User, related_name='harmonization_ingei_file')
    workflow_step = models.ForeignKey(MAWorkflowStep, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False, upload_to=workflow_step_directory_path,
                            storage=PrivateMediaStorage())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Workflow Step File")
        verbose_name_plural = _("Workflow Step Files")

    def __unicode__(self):
        return smart_unicode("{} - {}".format(self.workflow_step.name, self.file.name))