# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-04 03:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mccr', '0002_mccrregistry_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCCRUserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'MCCRUserType',
                'verbose_name_plural': 'MCCRUserTypes',
            },
        ),
        migrations.AlterModelOptions(
            name='mccrfile',
            options={'verbose_name': 'MCCRFile', 'verbose_name_plural': 'MCCRFiles'},
        ),
        migrations.AlterModelOptions(
            name='mccrregistry',
            options={'verbose_name': 'MCCRRegistry', 'verbose_name_plural': 'MCCRRegistries'},
        ),
        migrations.AlterField(
            model_name='mccrregistry',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mccr', to='mccr.MCCRUserType'),
        ),
    ]
