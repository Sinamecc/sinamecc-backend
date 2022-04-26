# Generated by Django 3.2 on 2021-12-22 02:42

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('adaptation_action', '0005_auto_20211215_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='adaptationaction',
            name='fsm_state',
            field=django_fsm.FSMField(default='new', max_length=100, protected=True),
        ),
        migrations.AddField(
            model_name='adaptationaction',
            name='review_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]