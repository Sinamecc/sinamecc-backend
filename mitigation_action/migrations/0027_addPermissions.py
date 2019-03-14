from __future__ import unicode_literals
from mitigation_action.models import Mitigation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db import migrations

def createPermissions(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(Mitigation)

    Permission.objects.create(
        codename='can_provide_information_ma',
        name='Can Provide Information MA',
        content_type=content_type,
    )

    Permission.objects.create(
        codename='user_dcc_permission_ma',
        name='User DCC Permission MA',
        content_type=content_type,
    )

    Permission.objects.create(
        codename='user_executive_secretary_permission_ma',
        name='User Executive Secretary Permission MA',
        content_type=content_type,
    )


class Migration(migrations.Migration):
    
    dependencies = [
        ('mitigation_action', '0026_auto_20181204_1636'),
    ]

    operations = [
        migrations.RunPython(createPermissions),
    ]