# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-21 16:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0006_auto_20180820_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sector',
            name='geographicLevel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ppcn.GeographicLevel'),
        ),
    ]
