# Generated by Django 3.2 on 2021-04-22 03:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import general.storages
import mitigation_action.workflow.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mitigation_action', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MAWorkflowStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('entry_name', models.CharField(max_length=100)),
                ('status', models.CharField(blank=True, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Workflow Step',
                'verbose_name_plural': 'Workflow Steps',
            },
        ),
        migrations.AlterField(
            model_name='mitigationaction',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mitigation_action', to='mitigation_action.contact'),
        ),
        migrations.CreateModel(
            name='MAWorkflowStepFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=general.storages.PrivateMediaStorage(), upload_to=mitigation_action.workflow.models.workflow_step_directory_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workflow_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_step_file', to='mitigation_action.maworkflowstep')),
            ],
            options={
                'verbose_name': 'Workflow Step File',
                'verbose_name_plural': 'Workflow Step Files',
            },
        ),
        migrations.AddField(
            model_name='maworkflowstep',
            name='mitigation_action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_step', to='mitigation_action.mitigationaction'),
        ),
        migrations.AddField(
            model_name='maworkflowstep',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('previous_status', models.CharField(max_length=100, null=True)),
                ('current_status', models.CharField(max_length=100)),
                ('mitigation_action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_log', to='mitigation_action.mitigationaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_log', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ChangeLog',
                'verbose_name_plural': 'ChangeLogs',
                'ordering': ('date',),
            },
        ),
    ]
