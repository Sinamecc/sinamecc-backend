# Generated by Django 3.2 on 2021-04-29 04:59

from django.db import migrations, models
import django.db.models.deletion
import general.storages
import mitigation_action.models


class Migration(migrations.Migration):

    dependencies = [
        ('mitigation_action', '0005_insert_catalogs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Initiative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, null=True)),
                ('objective', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('description_file',models.FileField(null=True, storage=general.storages.PrivateMediaStorage(), upload_to=mitigation_action.models.directory_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('initiative_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initiative', to='mitigation_action.initiativetype')),
            ],
            options={
                'verbose_name': 'Initiative',
                'verbose_name_plural': 'Initiative',
            },
        ),
        migrations.AddField(
            model_name='contact',
            name='institution',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='job_title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='MitigationActionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('other_end_date', models.CharField(max_length=254, null=True)),
                ('institution', models.CharField(max_length=254, null=True)),
                ('other_institution', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mitigation_action_status', to='mitigation_action.status')),
            ],
            options={
                'verbose_name': 'Mitigation Action Status',
                'verbose_name_plural': 'Mitigation Action Status',
            },
        ),
        migrations.CreateModel(
            name='InitiativeGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('initiative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goal', to='mitigation_action.initiative')),
            ],
            options={
                'verbose_name': 'Initiative Goal',
                'verbose_name_plural': 'Initiative Goal',
            },
        ),
        migrations.CreateModel(
            name='GeographicLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=254, null=True)),
                ('location_file',models.FileField(null=True, storage=general.storages.PrivateMediaStorage(), upload_to=mitigation_action.models.directory_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('geographic_scale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='geographic_location', to='mitigation_action.geographicscale')),
            ],
            options={
                'verbose_name': 'Geographic Location', 
                'verbose_name_plural': 'Geographic Locations'
            },
        ),
        migrations.AddField(
            model_name='mitigationaction',
            name='geographic_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mitigation_action', to='mitigation_action.geographiclocation'),
        ),
        migrations.AddField(
            model_name='mitigationaction',
            name='initiative',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mitigation_action', to='mitigation_action.initiative'),
        ),
        migrations.AddField(
            model_name='mitigationaction',
            name='status_information',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mitigation_action', to='mitigation_action.mitigationactionstatus'),
        ),
    ]
