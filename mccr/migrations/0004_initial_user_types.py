# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-04 03:54
from __future__ import unicode_literals

from django.db import migrations

def inser_form_data(apps, schema_editor):
    MCCRUserType = apps.get_model('mccr', 'MCCRUserType')

    # Data
    user_type_data = [
        'Registrator',
        'Reviewer'
    ]

    MCCRUserType.objects.all().delete()

    for utd in user_type_data:
        mut = MCCRUserType(name=utd)
        mut.save()

class Migration(migrations.Migration):

    dependencies = [
        ('mccr', '0003_auto_20180504_0350'),
    ]

    operations = [
        migrations.RunPython(inser_form_data)
    ]