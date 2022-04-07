# Generated by Django 3.2 on 2022-04-05 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adaptation_action', '0007_catalogs_adaptation'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicatoradaptation',
            name='other_reporting_periodicity',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='reportorganization',
            name='other_report_organization_type',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='implementation',
            name='action_code',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='indicatoradaptation',
            name='reporting_periodicity',
            field=models.CharField(choices=[('YEARLY', 'Yearly'), ('BIANNUAL', 'Biannual'), ('QUARTERLY', 'Quartely'), ('OTHER', 'Other')], default='YEARLY', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='indicatoradaptation',
            name='unit',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='reportorganization',
            name='responsible_entity',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
