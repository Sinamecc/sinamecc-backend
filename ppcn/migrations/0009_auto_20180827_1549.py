# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-27 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0008_auto_20180822_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emissionfactor',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='geographiclevel',
            name='level_en',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='geographiclevel',
            name='level_es',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='inventorymethodology',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='organization',
            name='fax',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='organization',
            name='postal_code',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='organization',
            name='representative_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='plusaction',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='potentialglobalwarming',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='quantifiedgas',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
