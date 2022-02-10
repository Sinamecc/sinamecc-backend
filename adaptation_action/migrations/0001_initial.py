# Generated by Django 3.2 on 2021-11-23 17:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mitigation_action', '0017_auto_20210831_0331'),
        ('general', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, null=True)),
                ('description', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='AdaptationActionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Adaptation Action Type',
                'verbose_name_plural': 'Adaptation Action Types',
            },
        ),
        migrations.CreateModel(
            name='AdaptationAxis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Adaptation Axis',
                'verbose_name_plural': 'Adaptation Axis',
            },
        ),
        migrations.CreateModel(
            name='Implementation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('duration', models.CharField(max_length=20, null=True)),
                ('responsible_entity', models.CharField(max_length=50, null=True)),
                ('other_entity', models.CharField(max_length=250, null=True)),
                ('action_code', models.CharField(max_length=3, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Implementation',
                'verbose_name_plural': 'Implementations',
            },
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
                ('description', models.CharField(max_length=3000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Instrument',
                'verbose_name_plural': 'Instruments',
            },
        ),
        migrations.CreateModel(
            name='NDCArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=2500)),
                ('other', models.CharField(max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'NDC Area',
                'verbose_name_plural': 'NDC Areas',
            },
        ),
        migrations.CreateModel(
            name='ODS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'ODS',
                'verbose_name_plural': 'ODS',
            },
        ),
        migrations.CreateModel(
            name='ReportOrganizationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, null=True)),
                ('entity_type', models.CharField(max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Report Organization Type',
                'verbose_name_plural': 'Report Organization Types',
            },
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.CreateModel(
            name='TypeClimateThreat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, null=True)),
                ('name', models.CharField(max_length=3000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Type Climate Threat',
                'verbose_name_plural': 'Type Climate Threats',
            },
        ),
        migrations.CreateModel(
            name='SubTopics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_topics', to='adaptation_action.topics')),
            ],
            options={
                'verbose_name': 'Sub Topic',
                'verbose_name_plural': 'Sub Topics',
            },
        ),
        migrations.CreateModel(
            name='ReportOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsible_entity', models.CharField(max_length=200, null=True)),
                ('legal_identification', models.CharField(max_length=50, null=True)),
                ('elaboration_date', models.DateField(null=True)),
                ('entity_address', models.CharField(max_length=250, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_organization', to='mitigation_action.contact')),
                ('report_organization_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_organization', to='adaptation_action.reportorganizationtype')),
            ],
            options={
                'verbose_name': 'Report Organization',
                'verbose_name_plural': 'Report Organizations',
            },
        ),
        migrations.CreateModel(
            name='NDCContribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=2500)),
                ('other', models.CharField(max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('ndc_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ndc_contribution', to='adaptation_action.ndcarea')),
            ],
            options={
                'verbose_name': 'NDC Contribution',
                'verbose_name_plural': 'NDC Contributions',
            },
        ),
        migrations.CreateModel(
            name='ClimateThreat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type_climate_threat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='climate_threat', to='adaptation_action.typeclimatethreat')),
            ],
            options={
                'verbose_name': 'Type Climate Threat',
                'verbose_name_plural': 'Type Climate Threats',
            },
        ),
        migrations.CreateModel(
            name='AdaptationAxisGuideline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('adaptation_axis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adaptation_axis_guideline', to='adaptation_action.adaptationaxis')),
            ],
            options={
                'verbose_name': 'Adaptation Axis Guideline',
                'verbose_name_plural': 'Adaptation Axis Guidelines',
            },
        ),
        migrations.CreateModel(
            name='AdaptationActionInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
                ('objective', models.CharField(max_length=3000, null=True)),
                ('description', models.CharField(max_length=3000, null=True)),
                ('meta', models.CharField(max_length=3000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('adaptation_action_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adaptation_action_information', to='adaptation_action.adaptationactiontype')),
                ('ods', models.ManyToManyField(blank=True, related_name='adaptation_action_information', to='adaptation_action.ODS')),
            ],
            options={
                'verbose_name': 'Adaptation Action Information',
                'verbose_name_plural': 'Adaptation Action Information',
            },
        ),
        migrations.CreateModel(
            name='AdaptationAction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adaptation_action', to='adaptation_action.activity')),
                ('adaptation_action_information', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adaptation_action', to='adaptation_action.adaptationactioninformation')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adaptation_action', to='general.address')),
                ('climate_threat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adaptation_action', to='adaptation_action.climatethreat')),
                ('implementation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adaptation_action', to='adaptation_action.implementation')),
                ('instrument', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adaptation_action', to='adaptation_action.instrument')),
                ('report_organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adaptation_action', to='adaptation_action.reportorganization')),
            ],
            options={
                'verbose_name': 'Adaptation Action',
                'verbose_name_plural': 'Adaptation Actions',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='adaptation_axis_guideline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='adaptation_action.adaptationaxisguideline', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='ndc_contribution',
            field=models.ManyToManyField(blank=True, related_name='activity', to='adaptation_action.NDCContribution', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='sub_topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='adaptation_action.subtopics'),
        ),
    ]
