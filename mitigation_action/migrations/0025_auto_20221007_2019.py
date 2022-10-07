# Generated by Django 3.2 on 2022-10-07 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0024_auto_20220920_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informationsource',
            name='type',
        ),
        migrations.AddField(
            model_name='informationsource',
            name='type',
            field=models.ManyToManyField(null=True, blank=True, related_name='information_source', to='mitigation_action.InformationSourceType'),
        ),
    ]
