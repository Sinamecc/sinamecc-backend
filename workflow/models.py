from __future__ import unicode_literals
from django.conf import settings

import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User =  get_user_model()


STATUS = (('resolved', _('Resolved')), ('pending', _('Pending'), )) 

class Comment(models.Model):

    form_section = models.CharField(max_length=3000, blank=False, null=True)
    comment = models.TextField(max_length=2048, blank=False, null=False)
    status = models.CharField(choices=STATUS, default='pending', max_length=10, blank=False, null=False)
    review_number = models.IntegerField()
    fsm_state = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __unicode__(self):
        return smart_unicode(self.name)

class ReviewStatus(models.Model):
    status = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("ReviewStatus")
        verbose_name_plural = _("ReviewStatuses")

    def __unicode__(self):
        return smart_unicode(self.name)
