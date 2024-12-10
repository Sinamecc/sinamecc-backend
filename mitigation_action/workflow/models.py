from django.db import models
from django.utils.encoding import smart_str as smart_unicode
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from general.storages import PrivateMediaStorage
from mitigation_action.models import MitigationAction
from time import gmtime, strftime

User = get_user_model()


def workflow_step_directory_path(instance, filename):
    dayly_date_segment = strftime("%Y%m%d", gmtime())
    hourly_date_segment = strftime("%H%M%S", gmtime())
    return "mitigation_actions/workflow_steps/{0}/{1}/{2}/{3}".format(instance.workflow_step.name, dayly_date_segment,
                                                                      hourly_date_segment, filename)


class MAWorkflowStep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mitigation_action = models.ForeignKey(MitigationAction, related_name='workflow_step', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    entry_name = models.CharField(max_length=100, blank=False, null=False)
    status = models.CharField(max_length=50, blank=True) # Accepted, Rejected, Commented
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Workflow Step")
        verbose_name_plural = _("Workflow Steps")

        


class MAWorkflowStepFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workflow_step = models.ForeignKey(MAWorkflowStep,related_name='workflow_step_file', on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False, upload_to=workflow_step_directory_path,
                            storage=PrivateMediaStorage())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Workflow Step File")
        verbose_name_plural = _("Workflow Step Files")

