from __future__ import unicode_literals
from ppcn.models import PPCN
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db import migrations

def createPermissions(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(PPCN)
    
    Permission.objects.create(
        codename='user_executive_secretary_permission_ppcn',
        name='user executive secretary permission PPCN',
        content_type=content_type,
    )

    Permission.objects.create(
        codename='user_dcc_permission_ppcn',
        name='user DCC permision PPCN',
        content_type=content_type,
    )

    Permission.objects.create(
        codename='user_ca_permission_ppcn',
        name='user CA permission PPCN',
        content_type=content_type,
    )

    Permission.objects.create(
        codename='can_provide_information_ppcn',
        name='Can provide information ppcn',
        content_type=content_type,
    )


class Migration(migrations.Migration):
    
    dependencies = [
        ('ppcn', '0016_auto_20190304_1628'),
    ]

    operations = [
        migrations.RunPython(createPermissions),
    ]