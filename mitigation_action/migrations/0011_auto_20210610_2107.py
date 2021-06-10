# Generated by Django 3.2 on 2021-06-10 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0010_auto_20210610_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringReportingIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_in_monitoring', models.BooleanField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Monitoring and Reporting Indicators',
                'verbose_name_plural': 'Monitoring and Reporting Indicators',
            },
        ),
        migrations.CreateModel(
            name='MonitoringIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_date_report_period', models.DateField(null=True)),
                ('final_date_report_period', models.DateField(null=True)),
                ('data_updated_date', models.DateField(null=True)),
                ('updated_data', models.CharField(max_length=150, null=True)),
                ('progress_report', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('indicator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monitoring_indicator', to='mitigation_action.indicator')),
                ('monitoring_reporting_indicator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monitoring_indicator', to='mitigation_action.monitoringreportingindicator')),
            ],
            options={
                'verbose_name': 'Monitoring Indicator',
                'verbose_name_plural': 'Monitoring Indicator',
            },
        ),
        migrations.AddField(
            model_name='mitigationaction',
            name='monitoring_reporting_indicator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mitigation_action', to='mitigation_action.monitoringreportingindicator'),
        ),
    ]
