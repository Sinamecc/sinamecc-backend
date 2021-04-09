from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from general.storages import PrivateMediaStorage
from time import gmtime, strftime

def profile_picture_path(instance, filename):
    dayly_date_segment = strftime("%Y%m%d", gmtime())
    hourly_date_segment = strftime("%H%M%S", gmtime())
    return "users/{0}/{1}/{2}/{3}".format(instance.user.username, dayly_date_segment, hourly_date_segment, filename)


# Create your models here.
class CustomUser(AbstractUser):
    is_provider = models.BooleanField(blank=False, null=False, default=False)
    is_administrador_dcc = models.BooleanField(blank=False, null=False, default=False)
    phone = models.CharField(max_length=50, blank=False, null=True)

    def __str__(self):
        return self.username


class ProfilePicture(models.Model):

    user = models.ForeignKey(CustomUser, related_name='profile_picture', on_delete=models.CASCADE)
    version = models.CharField(max_length=100, unique=True, blank=False, null=False)
    image = models.FileField(blank=False, null=False, upload_to=profile_picture_path, storage=PrivateMediaStorage())
    current = models.BooleanField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)