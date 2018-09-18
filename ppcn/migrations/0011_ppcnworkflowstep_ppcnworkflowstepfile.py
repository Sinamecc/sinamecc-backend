# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-07 22:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import general.storages
import ppcn.workflow_steps.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ppcn', '0010_auto_20180831_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='PPCNWorkflowStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('entry_name', models.CharField(max_length=100)),
                ('status', models.CharField(blank=True, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('ppcn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_step', to='ppcn.PPCN')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Workflow Step',
                'verbose_name_plural': 'Workflow Steps',
            },
        ),
        migrations.CreateModel(
            name='PPCNWorkflowStepFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=general.storages.PrivateMediaStorage(), upload_to=ppcn.workflow_steps.models.workflow_step_directory_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workflow_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='ppcn.PPCNWorkflowStep')),
            ],
            options={
                'verbose_name': 'Workflow Step File',
                'verbose_name_plural': 'Workflow Step Files',
            },
        ),
    ]
