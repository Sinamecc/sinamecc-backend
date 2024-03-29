# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-08-05 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0026_auto_20200602_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationclassification',
            name='carbon_offset',
        ),
        migrations.RemoveField(
            model_name='organizationclassification',
            name='reduction',
        ),
        migrations.RemoveField(
            model_name='ppcn',
            name='gas_removal',
        ),
        migrations.AddField(
            model_name='carbonoffset',
            name='organization_classification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carbon_offset', to='ppcn.OrganizationClassification'),
        ),
        migrations.AddField(
            model_name='gasremoval',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='gasremoval',
            name='ppcn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gas_removal', to='ppcn.PPCN'),
        ),
        migrations.AddField(
            model_name='gasremoval',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='reduction',
            name='organization_classification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reduction', to='ppcn.OrganizationClassification'),
        ),
        migrations.AlterField(
            model_name='geiactivitytype',
            name='gei_organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gei_activity_type', to='ppcn.GeiOrganization'),
        ),
    ]
