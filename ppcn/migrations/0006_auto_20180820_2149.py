# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-20 21:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0005_auto_20180816_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ppcn',
            name='base_year',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ppcn',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ppcn.Sector'),
        ),
    ]
