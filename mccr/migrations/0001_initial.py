# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-19 03:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mitigation_action', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCCRFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='mccr/%Y%m%d')),
            ],
        ),
        migrations.CreateModel(
            name='MCCRRegistry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_type', models.CharField(max_length=100)),
                ('mitigation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mccr', to='mitigation_action.MitigationAction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mccr', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mccrfile',
            name='mccr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mccr.MCCRRegistry'),
        ),
        migrations.AddField(
            model_name='mccrfile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
