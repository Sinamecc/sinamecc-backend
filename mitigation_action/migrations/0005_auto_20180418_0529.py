# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-18 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0004_progressindicator_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mitigation',
            name='ingei_compliance',
        ),
        migrations.AddField(
            model_name='mitigation',
            name='ingei_compliances',
            field=models.ManyToManyField(to='mitigation_action.IngeiCompliance'),
        ),
    ]
