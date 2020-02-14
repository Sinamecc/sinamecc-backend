from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    is_provider = models.BooleanField(blank=False, null=False, default=False)
    is_administrador_dcc = models.BooleanField(blank=False, null=False, default=False)
    phone = models.CharField(max_length=50, blank=False, null=True)

    def __str__(self):
        return self.username
