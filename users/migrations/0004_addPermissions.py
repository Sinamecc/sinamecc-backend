from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mitigation_action.models import Mitigation
from django.db import migrations, models

def add_Permissions(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(Mitigation)

    mitigation_action_provider_group = Group.objects.get(name ='mitigation_action_provider')
    mitigation_action_information_provider_permission = Permission.objects.get(codename='can_provide_information',content_type=content_type)
    mitigation_action_provider_group.permissions.add(mitigation_action_information_provider_permission)

    dcc_mitigation_action_responsible_group = Group.objects.get(name ='dcc_mitigation_action_responsible')
    DCC_functionary_MA_permission = Permission.objects.get(codename='user_dcc_permission',content_type=content_type)
    dcc_mitigation_action_responsible_group.permissions.add(DCC_functionary_MA_permission)

    dcc_executive_secretary_group = Group.objects.get(name ='dcc_executive_secretary')
    executive_secretary_of_the_DCC_permission = Permission.objects.get(codename='user_executive_secretary_permission',content_type=content_type)
    dcc_executive_secretary_group.permissions.add(executive_secretary_of_the_DCC_permission)


class Migration(migrations.Migration):
    dependencies = [

        ('mitigation_action', '0027_addPermissions'),
        ('users', '0003_addPermissions')
    ]
    operations = [
        migrations.RunPython(add_Permissions),
    ]