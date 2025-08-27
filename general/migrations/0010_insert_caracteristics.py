from general.migrations.default_data.data_migration_0002_01 import _category_ct
from django.db import migrations


def insert_data(apps, schema_editor):

    CategoryCT = apps.get_model("general", "CategoryCT")
    for _data in _category_ct:
        characteristic = _data.pop('characteristic', [])
        category_ct_record = CategoryCT(**_data)
        category_ct_record.save()

        for _characteristic in characteristic:
            Characteristic = apps.get_model("general", "Characteristic")
            characteristic_record = Characteristic(**_characteristic, category_ct=category_ct_record)
            characteristic_record.save()


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0009_categoryct_caracteristic'),
    ]

    operations = [
        migrations.RunPython(insert_data),
    ]
