# Generated by Django 3.2 on 2022-04-20 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0004_auto_20201028_1950'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportdata',
            name='comments',
            field=models.ManyToManyField(blank=True, to='workflow.Comment'),
        ),
        migrations.AddField(
            model_name='reportdata',
            name='review_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('previous_status', models.CharField(max_length=100, null=True)),
                ('current_status', models.CharField(max_length=100)),
                ('report_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_log', to='report_data.reportdata')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_data_fsm_change_log', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ChangeLog',
                'verbose_name_plural': 'ChangeLogs',
                'ordering': ('date',),
            },
        ),
    ]
