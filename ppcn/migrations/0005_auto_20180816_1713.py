# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-16 17:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0004_auto_20180801_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ppcnfile',
            name='ppcn_form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='ppcn.PPCN'),
        ),
    ]