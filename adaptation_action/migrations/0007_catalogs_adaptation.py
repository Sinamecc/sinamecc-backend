from django.db import migrations
from adaptation_action.migrations.default_data.data_migration_0001_03 import _source_type, _general_impact, _temporality_impact

def insert_indicator_source(apps, schema_editor):
    IndicatorSource = apps.get_model('adaptation_action', 'IndicatorSource')
    for _data in _source_type:
        indicator_source_record = IndicatorSource(**_data)
        indicator_source_record.save()

def insert_general_impact(apps, schema_editor):
    GeneralImpact = apps.get_model('adaptation_action', 'GeneralImpact')
    for _data in _general_impact:
        general_impact_record = GeneralImpact(**_data)
        general_impact_record.save()

def insert_temporality_impact(apps, schema_editor):
    TemporalityImpact = apps.get_model('adaptation_action', 'TemporalityImpact')
    for _data in _temporality_impact:
        temporality_impact_record = TemporalityImpact(**_data)
        temporality_impact_record.save()

class Migration(migrations.Migration):
    
    dependencies = [
        ('adaptation_action', '0006_auto_20211222_0242'),
    ]

    operations = [
        migrations.RunPython(insert_indicator_source, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_general_impact, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_temporality_impact, reverse_code=migrations.RunPython.noop),
    ]