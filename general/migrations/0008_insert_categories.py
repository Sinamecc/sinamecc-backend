from general.migrations.default_data.data_migration_0001_01 import _dimension
from django.db import migrations


def insert_data(apps, schema_editor):
    
    Dimension = apps.get_model('general', 'Dimension')
    for _data in _dimension:
        category_group = _data.pop('groups', [])
        dimension_record = Dimension(**_data)
        dimension_record.save()
        
        for group in category_group:
            category = group.pop('categories', [])
            category_group_record = apps.get_model('general', 'CategoryGroup')(dimension=dimension_record, **group)
            category_group_record.save()

            for _category in category:
                category_record = apps.get_model('general', 'Category')(category_group=category_group_record, **_category)
                category_record.save()


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0007_categorygroup_dimension_category_and_more'),
    ]

    operations = [
        migrations.RunPython(insert_data, reverse_code=migrations.RunPython.noop),
    ]
