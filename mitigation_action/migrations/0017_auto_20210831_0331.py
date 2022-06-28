# Generated by Django 3.2 on 2021-08-31 03:31

from django.db import migrations, models
import django.db.models.deletion
import general.storages
import mitigation_action.models

from mitigation_action.migrations.default_data.data_migration_0017 import _classifier, _information_source_type, _thematic_categorization_type

def insert_form_data(apps, schema_editor):

    # Models
    Classifier = apps.get_model('mitigation_action', 'Classifier')
    InformationSourceType = apps.get_model('mitigation_action', 'InformationSourceType')
    ThematicCategorizationType = apps.get_model('mitigation_action', 'ThematicCategorizationType')

    model_and_data = {

        Classifier: _classifier,
        InformationSourceType: _information_source_type,
        ThematicCategorizationType: _thematic_categorization_type
    }

    for _model, _data in model_and_data.items():
        for _record in _data:
            record = _model(**_record)
            record.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0016_auto_20210729_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Classifier',
                'verbose_name_plural': 'Classifiers',
            },
        ),
        migrations.CreateModel(
            name='InformationSourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, null=True)),
                ('code', models.CharField(max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Information Source Type',
                'verbose_name_plural': 'Information Source Types',
            },
        ),
        migrations.CreateModel(
            name='ThematicCategorizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Thematic Categorization Type',
                'verbose_name_plural': 'Thematic Categorization Types',
            },
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='data_generating_institution',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='measurement_start_date',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='reporting_institution',
        ),
        migrations.AddField(
            model_name='indicator',
            name='additional_information_file',
            field=models.FileField(null=True, storage=general.storages.PrivateMediaStorage(), upload_to=mitigation_action.models.directory_path),
        ),
        migrations.AddField(
            model_name='indicator',
            name='available_time_end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='available_time_start_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='comments',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='indicator', to='mitigation_action.contact'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='disaggregation',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='geographic_coverage',
            field=models.CharField(choices=[('NATIONAL', 'National'), ('REGIONAL', 'Regional'), ('PROVINCIAL', 'Provincial'), ('CANTONAL', 'Cantonal'), ('OTHER', 'Other')], default='NATIONAL', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='limitation',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='methodological_detail_file',
            field=models.FileField(null=True, storage=general.storages.PrivateMediaStorage(), upload_to=mitigation_action.models.directory_path),
        ),
        migrations.AddField(
            model_name='indicator',
            name='other_classifier',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='other_geographic_coverage',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='other_type_of_data',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='monitoringindicator',
            name='updated_data_file',
            field=models.FileField(null=True, storage=general.storages.PrivateMediaStorage(), upload_to=mitigation_action.models.directory_path),
        ),
        migrations.CreateModel(
            name='InformationSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsible_institution', models.CharField(max_length=500, null=True)),
                ('other_type', models.CharField(max_length=500, blank=True, null=True)),
                ('statistical_operation', models.CharField(max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='information_source', to='mitigation_action.informationsourcetype')),
            ],
            options={
                'verbose_name': 'Information Source',
                'verbose_name_plural': 'Information Sources',
            },
        ),
        migrations.CreateModel(
            name='IndicatorChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('changes', models.TextField(null=True)),
                ('changes_description', models.TextField(null=True)),
                ('author', models.CharField(max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicator_change_log', to='mitigation_action.indicator')),
            ],
        ),
        migrations.AddField(
            model_name='indicator',
            name='classifier',
            field=models.ManyToManyField(blank=True, related_name='indicator', to='mitigation_action.Classifier'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='information_source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='indicator', to='mitigation_action.informationsource'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='type_of_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='indicator', to='mitigation_action.thematiccategorizationtype'),
        ),
        migrations.RunPython(insert_form_data),
    ]
