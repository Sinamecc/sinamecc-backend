# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-04-21 19:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0020_auto_20200421_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission_quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buildings_number', models.IntegerField()),
                ('data_inventory_quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recognition_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_classification', to='ppcn.RecognitionType')),
                ('required_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_classification', to='ppcn.RequiredLevel')),
            ],
            options={
                'verbose_name': 'Organnization Classification',
                'verbose_name_plural': 'Organnization Classification',
            },
        ),
        migrations.CreateModel(
            name='Reduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=200)),
                ('activity', models.CharField(max_length=200)),
                ('detail_reduction', models.TextField()),
                ('emission', models.CharField(max_length=10)),
                ('total_emission', models.CharField(max_length=10)),
                ('investment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('investment_currency', models.CharField(choices=[('CRC', 'Costa Rican colón'), ('USD', 'United States dollar')], max_length=10)),
                ('total_investment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_investment_currency', models.CharField(choices=[('CRC', 'Costa Rican colón'), ('USD', 'United States dollar')], max_length=10)),
            ],
            options={
                'verbose_name': 'Reduction',
                'verbose_name_plural': 'Reductions',
            },
        ),
        migrations.AlterModelOptions(
            name='ciiucode',
            options={'verbose_name': 'CIIU Code', 'verbose_name_plural': 'CIIU Codes'},
        ),
        migrations.RemoveField(
            model_name='ppcn',
            name='recognition_type',
        ),
        migrations.RemoveField(
            model_name='ppcn',
            name='required_level',
        ),
    ]
