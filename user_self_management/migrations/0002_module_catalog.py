from django.db import migrations
from user_self_management.migrations.default_data.data_migration_0001_01 import _modules

def insert_module_data(apps, schema_editor):
    
    Module = apps.get_model('user_self_management', 'Module')
    for _data in _modules:
        module_record = Module(**_data)
        module_record.save()
    
class Migration(migrations.Migration):
    
        dependencies = [
            ('user_self_management', '0001_initial'),
        ]
    
        operations = [
            migrations.RunPython(insert_module_data, reverse_code=migrations.RunPython.noop),
        ]