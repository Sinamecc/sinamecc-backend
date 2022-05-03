# Generated by Django 3.2 on 2022-05-03 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0017_auto_20210831_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiativetype',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mitigationaction',
            name='code',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
