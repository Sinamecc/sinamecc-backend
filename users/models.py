from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):

    def __str__(self):
        return self.username

class CustomGroup(models.Model):
    
    group = models.OneToOneField(Group)
    label = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = _("CustomGroup")
        verbose_name_plural = _("CustomGroups")
