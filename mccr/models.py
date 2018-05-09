from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from mitigation_action.models import Mitigation
import uuid

User =  get_user_model()

class MCCRUserType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("MCCRUserType")
        verbose_name_plural = _("MCCRUserTypes")

    def __unicode__(self):
        return smart_unicode(self.name)

# TODO: fix upload_to to include MCCR UUID
class MCCRRegistry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50, blank=False, null=False)
    user = models.ForeignKey(User, related_name='mccr')
    mitigation = models.ForeignKey(Mitigation, related_name='mccr')
    user_type = models.ForeignKey(MCCRUserType, related_name='mccr')

    class Meta:
        verbose_name = _("MCCRRegistry")
        verbose_name_plural = _("MCCRRegistries")

    def __unicode__(self):
        return smart_unicode(self.id)

class MCCRFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(blank=False, null=False, upload_to='mccr/%Y%m%d')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mccr = models.ForeignKey(MCCRRegistry, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("MCCRFile")
        verbose_name_plural = _("MCCRFiles")

    def __unicode__(self):
        return smart_unicode(self.type)
