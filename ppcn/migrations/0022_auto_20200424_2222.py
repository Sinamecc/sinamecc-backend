# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-04-24 22:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0021_auto_20200421_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarbonOffset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offset_scheme', models.CharField(choices=[('CER', 'CER'), ('VER', 'VER'), ('UCC', 'Unidades de Compesnsacion de Carbono')], max_length=10)),
                ('project_location', models.CharField(max_length=200)),
                ('certificate_identification', models.CharField(max_length=200)),
                ('total_carbon_offset', models.CharField(max_length=100)),
                ('offset_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('offset_cost_currency', models.CharField(choices=[('CRC', 'Costa Rican colón'), ('USD', 'United States dollar')], max_length=10)),
                ('period', models.CharField(max_length=100)),
                ('total_offset_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_offset_cost_currency', models.CharField(choices=[('CRC', 'Costa Rican colón'), ('USD', 'United States dollar')], max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Carbon Offset',
                'verbose_name_plural': 'Carbon Offsets',
            },
        ),
        migrations.AddField(
            model_name='organizationclassification',
            name='created',
            field=models.DateTimeField(auto_now_add=True)
        ),
        migrations.AddField(
            model_name='organizationclassification',
            name='reduction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_classification', to='ppcn.Reduction'),
        ),
        migrations.AddField(
            model_name='organizationclassification',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='ppcn',
            name='organization_classification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ppcn', to='ppcn.OrganizationClassification'),
        ),
        migrations.AddField(
            model_name='reduction',
            name='created',
            field=models.DateTimeField(auto_now_add=True)
        ),
        migrations.AddField(
            model_name='reduction',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='organizationclassification',
            name='carbon_offset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_classification', to='ppcn.CarbonOffset'),
        ),
    ]