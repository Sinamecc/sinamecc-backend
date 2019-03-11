from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ppcn.models import PPCN
from django.db import migrations, models


def add_Permissions(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(PPCN)
    executive_secretary_group = Group.objects.get(name ='dcc_executive_secretary')
    executive_secretary_permission, created = Permission.objects.get_or_create(codename='user_executive_secretary_permission',content_type=content_type)
    executive_secretary_group.permissions.add(executive_secretary_permission)

    user_DCC_permission_ppcn_group = Group.objects.get(name ='dcc_ppcn_responsible')
    user_DCC_permission, created = Permission.objects.get_or_create(codename='user_dcc_permission_ppcn',content_type=content_type)
    user_DCC_permission_ppcn_group.permissions.add(user_DCC_permission)

    user_CA_permission_ppcn_group = Group.objects.get(name ='dcc_ppcn_responsible')
    user_CA_permission, created = Permission.objects.get_or_create(codename='user_ca_permission_ppcn',content_type=content_type)
    user_CA_permission_ppcn_group.permissions.add(user_CA_permission)

    can_provide_information_ppcn_group = Group.objects.get(name ='ppcn_responsible')
    can_provide_information_permission, created = Permission.objects.get_or_create(codename='can_provide_information_ppcn',content_type=content_type)
    can_provide_information_ppcn_group.permissions.add(can_provide_information_permission)


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_customgroup')
    ]
    operations = [
        migrations.RunPython(add_Permissions),
    ]

    