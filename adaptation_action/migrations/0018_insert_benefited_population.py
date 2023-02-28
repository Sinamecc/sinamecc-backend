from django.db import migrations
from adaptation_action.migrations.default_data.data_migration_0001_03 import _benefited_population

def insert_benefited_population(apps, schema_editor):
    BenefitedPopulation = apps.get_model('adaptation_action', 'BenefitedPopulation')
    for _data in _benefited_population:
        benefited_population_record = BenefitedPopulation(**_data)
        benefited_population_record.save()

class Migration(migrations.Migration):
    
    dependencies = [
        ('adaptation_action', '0017_auto_20230228_2006'),
    ]

    operations = [
        migrations.RunPython(insert_benefited_population, reverse_code=migrations.RunPython.noop),
    ]