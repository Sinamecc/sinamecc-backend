# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-05-25 22:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0022_auto_20200511_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='GasRemoval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removal_cost', models.DecimalField(decimal_places=2, max_digits=20)),
                ('removal_cost_currency', models.CharField(choices=[('CRC', 'Costa Rican colón'), ('USD', 'United States dollar')], max_length=10)),
                ('total', models.DecimalField(decimal_places=5, max_digits=20)),
                ('removal_descriptions', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Gas Removal',
                'verbose_name_plural': 'Gas Remals',
            },
        ),
        migrations.CreateModel(
            name='RemovalProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_es', models.CharField(max_length=100, null=True)),
                ('name_en', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Removal Project',
                'verbose_name_plural': 'Removal Projects',
            },
        ),
        migrations.AddField(
            model_name='ppcn',
            name='gas_removal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ppcn', to='ppcn.GasRemoval'),
        ),
    ]
