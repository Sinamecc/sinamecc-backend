# Generated by Django 3.2 on 2022-11-21 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0025_auto_20221012_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoringindicator',
            name='progress_report_period',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='monitoringindicator',
            name='source_type',
            field=models.TextField(null=True),
        ),
    ]
