# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-19 04:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mccr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mccrregistry',
            name='status',
            field=models.CharField(default='new', max_length=50),
            preserve_default=False,
        ),
    ]