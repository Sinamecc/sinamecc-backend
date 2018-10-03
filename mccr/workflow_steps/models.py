from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from general.storages import PrivateMediaStorage
from mccr.models import  MCCRRegistry
from general.models import BaseWorkflowStep, BaseWorkflowStepFile
from time import gmtime, strftime

User = get_user_model()


def workflow_step_directory_path(instance, filename):
    dayly_date_segment = strftime("%Y%m%d", gmtime())
    hourly_date_segment = strftime("%H%M%S", gmtime())
    return "mccr/workflow_steps/{0}/{1}/{2}/{3}".format(instance.workflow_step.name, dayly_date_segment,
                                                                      hourly_date_segment, filename)

class MCCRWorkflowStep(BaseWorkflowStep):

    mccr = models.ForeignKey(MCCRRegistry, related_name='workflow_step', on_delete=models.CASCADE)
    
    
class MCCRWorkflowStepFile(BaseWorkflowStepFile):
    workflow_step = models.ForeignKey(MCCRWorkflowStep,related_name='workflow_step_file', on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False, upload_to=workflow_step_directory_path,
                            storage=PrivateMediaStorage())
