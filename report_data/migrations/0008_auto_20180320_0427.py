# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-20 04:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report_data', '0007_auto_20180320_0346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportfile',
            name='versions',
        ),
        migrations.AddField(
            model_name='reportfileversion',
            name='report_file',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report_data.ReportFile'),
            preserve_default=False,
        ),
    ]
