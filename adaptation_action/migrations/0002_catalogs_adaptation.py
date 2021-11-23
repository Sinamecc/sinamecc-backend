from django.db import migrations
from adaptation_action.migrations.default_data.data_migration_0001_02 import _province
from adaptation_action.migrations.default_data.data_migration_0001_03 import _report_organization_type, _type_climated_threat, _adaptation_action_type

def insert_province_data(apps, schema_editor):

    # Models
    Province = apps.get_model('general', 'Province')
    Canton = apps.get_model('general', 'Canton')
    District = apps.get_model('general', 'District')

    for _data in _province:
        _canton = _data.pop('canton')
        province_record = Province(**_data)
        province_record.save()

        for canton in _canton:
            _district = canton.pop('district')
            canton_record = Canton(province=province_record, **canton)
            canton_record.save()

            for district in _district:
                district_record = District(canton=canton_record, **district)
                district_record.save()


def insert_report_organization_type_data(apps, schema_editor):
    ReportOrganizationType = apps.get_model('adaptation_action', 'ReportOrganizationType')
    for _data in _report_organization_type:
        report_organization_type_record = ReportOrganizationType(**_data)
        report_organization_type_record.save()

def insert_type_climated_threat_data(apps, schema_editor):
    TypeClimatedThreat = apps.get_model('adaptation_action', 'TypeClimatedThreat')
    for _data in _type_climated_threat:
        type_climated_threat_record = TypeClimatedThreat(**_data)
        type_climated_threat_record.save()

def insert_adaptation_action_type_data(apps, schema_editor):
    AdaptationActionType = apps.get_model('adaptation_action', 'AdaptationActionType')
    for _data in _adaptation_action_type:
        adaptation_action_type_record = AdaptationActionType(**_data)
        adaptation_action_type_record.save()

class Migration(migrations.Migration):

    dependencies = [
        ('adaptation_action', '0001_initial'),
        ('general', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(insert_province_data, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_report_organization_type_data, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_type_climated_threat_data, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_adaptation_action_type_data, reverse_code=migrations.RunPython.noop),
    ]
