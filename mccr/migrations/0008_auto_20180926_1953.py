# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-26 19:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mccr', '0007_auto_20180803_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('previous_status', models.CharField(max_length=100, null=True)),
                ('current_status', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'ChangeLog',
                'verbose_name_plural': 'ChangeLogs',
                'ordering': ('date',),
            },
        ),
        migrations.AddField(
            model_name='mccrregistry',
            name='fsm_state',
            field=django_fsm.FSMField(default='new', max_length=50, protected=True),
        ),
        migrations.AddField(
            model_name='changelog',
            name='ppcn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_log', to='mccr.MCCRRegistry'),
        ),
        migrations.AddField(
            model_name='changelog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_log_mccr', to=settings.AUTH_USER_MODEL),
        ),
    ]
