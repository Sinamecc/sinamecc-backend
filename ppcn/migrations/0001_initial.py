# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-20 14:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mitigation_action', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmissionFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'EmissionFactor',
                'verbose_name_plural': 'EmissionFactors',
            },
        ),
        migrations.CreateModel(
            name='InventoryMethodology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'InventoryMethodology',
                'verbose_name_plural': 'InventoryMethodologies',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_es', models.CharField(max_length=200)),
                ('level_en', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Level',
                'verbose_name_plural': 'Levels',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('representative_name', models.CharField(max_length=200)),
                ('postal_code', models.CharField(max_length=200)),
                ('fax', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('ciiu', models.CharField(max_length=200)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='mitigation_action.Contact')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='ppcn.Level')),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='PlusAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'PlusAction',
                'verbose_name_plural': 'PlusActions',
            },
        ),
        migrations.CreateModel(
            name='PotentialGlobalWarming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'PotentialGlobalWarming',
                'verbose_name_plural': 'PotentialGlobalWarmings',
            },
        ),
        migrations.CreateModel(
            name='QuantifiedGas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'QuantifiedGas',
                'verbose_name_plural': 'QuantifiedGases',
            },
        ),
        migrations.CreateModel(
            name='RequestPpcn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='request_ppcn/%Y%m%d/%H%M%S')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Organization', to='ppcn.Organization')),
            ],
            options={
                'verbose_name': 'RequestPpcn',
                'verbose_name_plural': 'RequestPpcns',
                'ordering': ('created',),
            },
        ),
    ]
