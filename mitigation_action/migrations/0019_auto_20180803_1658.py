# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-03 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import general.storages


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0018_auto_20180726_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harmonizationingeifile',
            name='file',
            field=models.FileField(storage=general.storages.PrivateMediaStorage(), upload_to='mitigation_actions/harmonization_ingei/%Y%m%d/%H%M%S'),
        ),
    ]