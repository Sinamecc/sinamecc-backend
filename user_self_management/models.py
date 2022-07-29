from venv import create
from django.db import models
import uuid

class Module(models.Model):

    name = models.TextField(null=True)
    supplier_reviewer = models.TextField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'

# Create your models here.
class User(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.TextField(null=True)
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    institution = models.TextField(null=True)
    role = models.TextField(null=True)
    position = models.TextField(null=True)
    module = models.ManyToManyField(Module, blank=True)


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'