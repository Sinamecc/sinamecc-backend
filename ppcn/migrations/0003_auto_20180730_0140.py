# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-10 01:40
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0002_auto_20180730_2101'),
    ]
    operations = [
        migrations.AddField(
            model_name='subsector',
            name='sector',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sector', to='ppcn.Sector'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sector',
            name='geographicLevel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='geographicLevel', to='ppcn.GeographicLevel'),
        ),
        
    ]
