# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-03-18 21:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0027_addPermissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mitigation',
            options={'ordering': ('created',), 'permissions': (('can_provide_information', 'Can Provide Information MA'), ('user_dcc_permission', 'User DCC Permission MA'), ('user_executive_secretary_permission', 'User Executive Secretary Permission MA')), 'verbose_name': 'MitigationAccess', 'verbose_name_plural': 'MitigationAccesses'},
        ),
    ]
