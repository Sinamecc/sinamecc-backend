# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-25 20:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import general.storages
import mccr.workflow_steps.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mccr', '0007_auto_20180803_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCCRWorkflowStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('entry_name', models.CharField(max_length=100)),
                ('status', models.CharField(blank=True, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('mccr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_step', to='mccr.MCCRRegistry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Workflow Step',
                'verbose_name_plural': 'Workflow Steps',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MCCRWorkflowStepFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(storage=general.storages.PrivateMediaStorage(), upload_to=mccr.workflow_steps.models.workflow_step_directory_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workflow_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_step_file', to='mccr.MCCRWorkflowStep')),
            ],
            options={
                'verbose_name': 'Workflow Step File',
                'verbose_name_plural': 'Workflow Step Files',
                'abstract': False,
            },
        ),
    ]
