# Generated by Django 3.2 on 2022-04-13 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adaptation_action', '0009_changelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionimpact',
            name='gender_equality',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='actionimpact',
            name='unwanted_action',
            field=models.TextField(null=True),
        ),
    ]
