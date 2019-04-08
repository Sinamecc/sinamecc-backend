from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    is_provider = models.BooleanField(blank=False, null=False, default=False)
    is_administrador_dcc = models.BooleanField(blank=False, null=False, default=False)
    def __str__(self):
        return self.username

class CustomGroup(models.Model):
    
    group = models.OneToOneField(Group, related_name='custom_group')
    label = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("CustomGroup")
        verbose_name_plural = _("CustomGroups")

        