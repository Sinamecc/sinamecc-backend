# Generated by Django 3.2 on 2021-04-22 03:45

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0002_auto_20210422_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='mitigationaction',
            name='fsm_state',
            field=django_fsm.FSMField(default='new', max_length=100, protected=True),
        ),
    ]
