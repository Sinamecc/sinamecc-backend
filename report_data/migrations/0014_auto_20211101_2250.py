# Generated by Django 3.2 on 2021-11-01 22:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import general.storages
import report_data.models


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0017_auto_20210831_0331'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report_data', '0013_reportfilemetadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('source', models.TextField(blank=True, null=True)),
                ('source_file', models.FileField(blank=True, null=True, storage=general.storages.PrivateMediaStorage(), upload_to=report_data.models.directory_path)),
                ('other_data_type', models.CharField(blank=True, max_length=255, null=True)),
                ('other_classifier', models.CharField(blank=True, max_length=255, null=True)),
                ('report_information', models.CharField(choices=[('statistics_or_variable', 'Statistics or Variable'), ('indicator', 'Indicator'), ('data_base', 'Data Base')], max_length=100)),
                ('have_line_base', models.BooleanField(default=False)),
                ('have_quality_element', models.BooleanField(default=False)),
                ('quality_element_description', models.TextField(blank=True, null=True)),
                ('transfer_data_with_sinamecc', models.BooleanField(default=False)),
                ('transfer_data_with_sinamecc_description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('classifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_data', to='mitigation_action.classifier')),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_data', to='mitigation_action.contact')),
                ('data_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_data', to='mitigation_action.thematiccategorizationtype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_data', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Report Data',
                'verbose_name_plural': 'Report Data',
                'ordering': ('created',),
            },
        ),
        migrations.AlterModelOptions(
            name='reportfile',
            options={'verbose_name': 'Report File', 'verbose_name_plural': 'Report Files'},
        ),
        migrations.AlterModelOptions(
            name='reportfilemetadata',
            options={'verbose_name': 'Report File Metadata', 'verbose_name_plural': 'Report FileMetadata'},
        ),
        migrations.AlterModelOptions(
            name='reportfileversion',
            options={'ordering': ('created',), 'verbose_name': 'Report File Version', 'verbose_name_plural': 'Report File Versions'},
        ),
        migrations.RemoveField(
            model_name='reportfile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='reportfile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reportfileversion',
            name='active',
        ),
        migrations.RemoveField(
            model_name='reportfileversion',
            name='user',
        ),
        migrations.AddField(
            model_name='reportfile',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='reportfileversion',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='reportfileversion',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='reportfileversion',
            name='file',
            field=models.FileField(blank=True, null=True, storage=general.storages.PrivateMediaStorage(), upload_to=report_data.models.directory_path),
        ),
        migrations.AlterField(
            model_name='reportfileversion',
            name='report_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_version', to='report_data.reportfile'),
        ),
        migrations.AlterField(
            model_name='reportfileversion',
            name='version',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='ReportDataChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changes', models.TextField(blank=True, null=True)),
                ('change_description', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_data_change_log', to=settings.AUTH_USER_MODEL)),
                ('report_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_data_change_log', to='report_data.reportdata', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Report Data Changelog',
                'verbose_name_plural': 'Report Data Changelogs',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=100, unique=True)),
                ('active', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('report_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='report_data.reportdata')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Report',
            },
        ),
        migrations.AddField(
            model_name='reportfile',
            name='report_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_file', to='report_data.report'),
        ),
    ]
