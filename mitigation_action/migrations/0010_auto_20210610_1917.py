# Generated by Django 3.2 on 2021-06-10 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0009_auto_20210528_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Monitoring Information',
                'verbose_name_plural': 'Monitoring Information',
            },
        ),
        migrations.AlterModelOptions(
            name='impactdocumentation',
            options={'verbose_name': 'Monitoring Information', 'verbose_name_plural': 'Monitoring Information'},
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('unit', models.CharField(max_length=255, null=True)),
                ('methodological_detail', models.TextField(null=True)),
                ('reporting_periodicity', models.CharField(choices=[('YEARLY', 'Yearly'), ('BIANNUAL', 'Biannual'), ('QUARTERLY', 'Quartely')], default='YEARLY', max_length=50, null=True)),
                ('data_generating_institution', models.CharField(max_length=255, null=True)),
                ('reporting_institution', models.CharField(max_length=255, null=True)),
                ('measurement_start_date', models.DateField(null=True)),
                ('additional_information', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('monitoring_information', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='indicator', to='mitigation_action.monitoringinformation')),
            ],
            options={
                'verbose_name': 'Indicator',
                'verbose_name_plural': 'Indicator',
            },
        ),
        migrations.AddField(
            model_name='mitigationaction',
            name='monitoring_information',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mitigation_action', to='mitigation_action.monitoringinformation'),
        ),
    ]
