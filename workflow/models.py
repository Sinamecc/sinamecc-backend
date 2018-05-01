from __future__ import unicode_literals
from django.conf import settings

import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User =  get_user_model()

class Comment(models.Model):
    comment = models.CharField(max_length=500, blank=False, null=False)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

class ReviewStatus(models.Model):
    status = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("ReviewStatus")
        verbose_name_plural = _("ReviewStatuses")
