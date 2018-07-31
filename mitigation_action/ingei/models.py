from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from mitigation_action.models import Mitigation
from general.storages import PrivateMediaStorage
User = get_user_model()

class HarmonizationIngei(models.Model):
    user = models.ForeignKey(User, related_name='harmonization_ingei')
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("HarmonizationIngei")
        verbose_name_plural = _("HarmonizationIngeis")

    def __unicode__(self):
        return smart_unicode(self.name)

class HarmonizationIngeiFile(models.Model):
    user = models.ForeignKey(User, related_name='harmonization_ingei_file')
    mitigation_action = models.ForeignKey(Mitigation, on_delete=models.CASCADE)
    harmonization_ingei = models.ForeignKey(HarmonizationIngei, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False, upload_to='mitigation_actions/harmonization_ingei/%Y%m%d/%H%M%S',storage=PrivateMediaStorage())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("HarmonizationIngeiFile")
        verbose_name_plural = _("HarmonizationIngeiFiles")
        ordering = ('created',)

    def __unicode__(self):
        return smart_unicode(self.name)