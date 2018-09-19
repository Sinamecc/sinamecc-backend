# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-19 15:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0021_auto_20180819_0423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maworkflowstep',
            name='mitigation_action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_step', to='mitigation_action.Mitigation'),
        ),
        migrations.AlterField(
            model_name='maworkflowstep',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='maworkflowstepfile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='maworkflowstepfile',
            name='workflow_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_step_file', to='mitigation_action.MAWorkflowStep'),
        ),
    ]
