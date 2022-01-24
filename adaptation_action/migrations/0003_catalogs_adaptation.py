from django.db import migrations
from adaptation_action.migrations.default_data.data_migration_0001_02 import _province
from adaptation_action.migrations.default_data.data_migration_0001_03 import _report_organization_type, _type_climated_threat, _adaptation_action_type, \
    _ODS_data, _finance_source, _instrument_detail, _source_type, _thematic_data, _classifier_sinamecc
from adaptation_action.models import FinanceInstrument

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

def insert_ODS_data(apps, schema_editor):
    ODS = apps.get_model('adaptation_action', 'ODS')
    for _data in _ODS_data:
        ods_record = ODS(**_data)
        ods_record.save()

def insert_finance_source(apps, schema_editor):
    FinanceSourceType = apps.get_model('adaptation_action', 'FinanceSourceType')
    for _data in _finance_source:
        finance_source_record = FinanceSourceType(**_data)
        finance_source_record.save()

def insert_instrument_detail(apps, schema_editor):
    FinanceInstrument = apps.get_model('adaptation_action', 'FinanceInstrument')
    for _data in _instrument_detail:
        instrument_detail_record = FinanceInstrument(**_data)
        instrument_detail_record.save()

def insert_source_type(apps, schema_editor):
    FinanceSourceType = apps.get_model('adaptation_action', 'FinanceSourceType')
    for _data in _finance_source:
        source_type_record = FinanceSourceType(**_data)
        source_type_record.save()

def insert_information_source_type(apps, schema_editor):
    InformationSourceType = apps.get_model('adaptation_action', 'InformationSourceType')
    for _data in _source_type:
        information_source_type_record = InformationSourceType(**_data)
        information_source_type_record.save()

def insert_thematic_data(apps, schema_editor):
    ThematicCategorizationType = apps.get_model('adaptation_action', 'ThematicCategorizationType')
    for _data in _thematic_data:
        thematic_data_record = ThematicCategorizationType(**_data)
        thematic_data_record.save()

def insert_classifier_sinamecc(apps, schema_editor):
    Classifier = apps.get_model('adaptation_action', 'Classifier')
    for _data in _classifier_sinamecc:
        classifier_sinamecc_record = Classifier(**_data)
        classifier_sinamecc_record.save()


class Migration(migrations.Migration):

    dependencies = [
        ('adaptation_action', '0002_auto_20211102_1437'),
    ]

    operations = [
        migrations.RunPython(insert_province_data, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_report_organization_type_data, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_type_climated_threat_data, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_adaptation_action_type_data, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_ODS_data, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_finance_source, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_instrument_detail, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_source_type, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_information_source_type, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_thematic_data, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(insert_classifier_sinamecc, reverse_code=migrations.RunPython.noop),
    ]
