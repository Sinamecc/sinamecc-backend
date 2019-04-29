from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mccr.models import MCCRRegistry
from mitigation_action.models import Mitigation
from ppcn.models import PPCN
from django.db import migrations, models
from users.serializers import NewCustomUserSerializer
from django.contrib.auth import get_user_model

group_sinamecc = { 
        u'general_administrator': 'General Administrator', u'registry_operator': 'Registry Operator',
        u'mitigation_action_provider': 'Mitigation Action Provider', u'ppcn_provider': 'PPCN Provider', 
        u'mccr_provider': 'MCCR Provider',  
        u'pgai': 'PGAI', u'validation_organization':'Validation Organization', 
        u'government_representative':'Government Representative', u'data_analyst': 'Data Analyst',
        u'non_governmental_data_provider':'Non-governmental Data Provider', u'inventory_compiler':'Inventory Compiler',

        u'dcc_ppcn_responsible':'DCC PPCN Responsible', u'dcc_mitigation_action_responsible':'DCC Mitigation Action Responsible', 
        u'dcc_mccr_responsible': 'DCC MCCR Responsible', 
        u'dcc_executive_secretary':'DCC Executive Secretary', u'dcc_executive_committee': 'DCC Executive Committe', 
        u'dcc_general': 'General Group DCC'
   } 
def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    CustomGroup = apps.get_model('users', 'CustomGroup')
    ## delete existing groups
    Group.objects.filter(name__in=[codename for codename in group_sinamecc.keys()]).delete()
    Group.objects.filter(name__in=['mitigation_action_responsible', 'ppcn_responsible', 'general_user']).delete()
    Group.objects.filter(name__in=[group_sinamecc[codename] for codename in group_sinamecc.keys()]).delete()
    CustomGroup.objects.filter(label__in=['Mitigation Action Responsible', 'PPCN Responsible', 'General User']).delete()

    #creatig groups
    group_saved = Group.objects.bulk_create([ Group(name=codename) for codename in group_sinamecc.keys()])
    CustomGroup.objects.bulk_create([ CustomGroup(label=group_sinamecc[group.name], group_id=group.id) for group in group_saved])



def add_permissions(apps, schema_editor):
    
    content_type_mccr = ContentType.objects.get_for_model(MCCRRegistry)
    content_type_ma = ContentType.objects.get_for_model(Mitigation)
    content_type_ppcn = ContentType.objects.get_for_model(PPCN)
    group_permission_mccr = [
        {'group':'dcc_mccr_responsible', 'perm':'user_dcc_permission'} , 
        {'group':'mccr_provider', 'perm':'can_provide_information'}, 
        {'group':'dcc_executive_committee', 'perm':'user_executive_committee_permissions'},
        {'group':'dcc_executive_secretary', 'perm' :'user_executive_secretary_permission'}
    ]
    group_permission_ma = [
        {'group':'mitigation_action_provider', 'perm':'can_provide_information'},
        {'group':'dcc_mitigation_action_responsible', 'perm':'user_dcc_permission'},
        {'group':'dcc_executive_secretary', 'perm':'user_executive_secretary_permission'},
    ]
    group_permission_ppcn = [
        {'group':'dcc_ppcn_responsible', 'perm':'user_dcc_permission'},
        {'group':'dcc_ppcn_responsible', 'perm':'user_ca_permission'},
        {'group':'ppcn_provider', 'perm':'can_provide_information'},
        {'group':'dcc_executive_secretary', 'perm':'user_executive_secretary_permission'}

    ]
    group_permission_list = [(group_permission_mccr, content_type_mccr), (group_permission_ma, content_type_ma), (group_permission_ppcn, content_type_ppcn)]

    for group_perm, content_type in group_permission_list:

        get_perm_groups = lambda x: (Group.objects.get(name = x['group']), Permission.objects.get(codename=x['perm'],content_type=content_type))
        create_relationship = lambda y: (y[0].permissions.add(y[1]))

        perm_group = list(map(get_perm_groups, group_perm))
        list(map(create_relationship, perm_group))
    

def add_create_user(apps, schema_editor):
    super_admin = {'username':'admin_sinamecc', 'first_name':'Administrador', 'last_name':'Sinamecc', 'email':'sinamec@grupoincocr.com', 'is_staff':True, 'is_active':True, 'is_provider':True, 'is_administrador_dcc':True}
    dcc_general_user = {'username':'dcc_general', 'first_name':'DCC', 'last_name':'Sinamecc', 'email':'izcar@grupoincocr.com', 'is_staff':True, 'is_active':True, 'is_provider':False, 'is_administrador_dcc':True}
    provider_general_user = {'username':'provider_general', 'first_name':'Provider', 'last_name':'Sinamecc', 'email':'carlos@grupoincocr.com', 'is_staff':True, 'is_active':True, 'is_provider':True, 'is_administrador_dcc':False}

    user_list = [super_admin, dcc_general_user, provider_general_user]
    created_user = lambda x: NewCustomUserSerializer(data = x)
    serialized_user_list =  list(map(created_user, user_list))
    saved_user_list = [user.save() if user.is_valid() else False for user in serialized_user_list ]
    user_list = [user.set_password('cambiame2019!') if user else False for user in saved_user_list]

    for user in saved_user_list:
        if user:
            if user.username == 'admin_sinamecc':
                user.is_superuser = True
            user.save()

def add_user_to_group(apps, schema_editor):
    UserModel = get_user_model()
    general_user = ['admin_sinamecc', 'dcc_general', 'provider_general']
    provider_groups = ['ppcn_provider', 'mitigation_action_provider', 'mccr_provider']
    general_user_list = [UserModel.objects.filter(username=username).get() for  username in general_user]
    for group in group_sinamecc.keys(): 
        group_db = Group.objects.get(name = group)
        general_user_list[0].groups.add(group_db)
        if group in provider_groups:
            general_user_list[2].groups.add(group_db)
        else: general_user_list[1].groups.add(group_db)








class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_auto_20190322_2126')
    ]
    operations = [
        migrations.RunPython(create_groups),
        migrations.RunPython(add_permissions),
        migrations.RunPython(add_create_user),
        migrations.RunPython(add_user_to_group)
    ]

