# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-05-07 16:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppcn', '0019_auto_20190718_2141'),
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
        migrations.CreateModel(
            name='CIIUCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciiu_code', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'CIIU Code',
                'verbose_name_plural': 'CIIU Codes',
            },
        ),
        migrations.CreateModel(
            name='OrganizationClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission_quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buildings_number', models.IntegerField()),
                ('data_inventory_quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('carbon_offset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_classification', to='ppcn.CarbonOffset')),
                ('recognition_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_classification', to='ppcn.RecognitionType')),
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
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Reduction',
                'verbose_name_plural': 'Reductions',
            },
        ),
        migrations.RemoveField(
            model_name='organization',
            name='ciiu',
        ),
        migrations.RemoveField(
            model_name='ppcn',
            name='recognition_type',
        ),
        migrations.RemoveField(
            model_name='ppcn',
            name='required_level',
        ),
        migrations.AddField(
            model_name='organization',
            name='created',
            field=models.DateTimeField(auto_now_add=True)
        ),
        migrations.AddField(
            model_name='organization',
            name='legal_identification',
            field=models.CharField(max_length=12)
        ),
        migrations.AddField(
            model_name='organization',
            name='representative_legal_identification',
            field=models.CharField(max_length=12),
        ),
        migrations.AddField(
            model_name='organization',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='ppcn',
            name='confidential',
            field=models.CharField(choices=[('confidential', 'Confidential'), ('no_confidential', 'No Confidential'), ('partially_confidential', 'Partially Confidential')], default='confidential', max_length=50),
        ),
        migrations.AddField(
            model_name='ppcn',
            name='confidential_fields',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='organizationclassification',
            name='reduction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_classification', to='ppcn.Reduction'),
        ),
        migrations.AddField(
            model_name='organizationclassification',
            name='required_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_classification', to='ppcn.RequiredLevel'),
        ),
        migrations.AddField(
            model_name='ciiucode',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ciiu_code', to='ppcn.Organization'),
        ),
        migrations.AddField(
            model_name='ppcn',
            name='organization_classification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ppcn', to='ppcn.OrganizationClassification'),
        ),
    ]
