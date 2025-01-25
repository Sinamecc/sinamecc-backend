from django.db import migrations, models
from users.serializers import UserCreateSerializer
from rolepermissions.roles import assign_role
from core.auth.roles import Admin, Reviewer, InformationProvider
from django.contrib.auth import get_user_model


def add_create_user(apps, schema_editor):
    super_admin = {'username':'admin', 'first_name':'Administrador', 'last_name':'Sinamecc', 'email':'sinamec@grupoincocr.com', 'is_staff':True, 'is_active':True, 'is_provider':True, 'is_administrador_dcc':True, 'phone': '12345678'}
    dcc_general_user = {'username':'general_dcc', 'first_name':'DCC', 'last_name':'Sinamecc', 'email':'izcar@grupoincocr.com', 'is_staff':True, 'is_active':True, 'is_provider':False, 'is_administrador_dcc':True, 'phone': '12345678'}
    provider_general_user = {'username':'information_provider', 'first_name':'Provider', 'last_name':'Sinamecc', 'email':'carlos@grupoincocr.com', 'is_staff':True, 'is_active':True, 'is_provider':True, 'is_administrador_dcc':False, 'phone': '12345678'}

    user_list = [super_admin, dcc_general_user, provider_general_user]
    created_user = lambda x: UserCreateSerializer(data= {**x, 'password':'cambiame'})
    serialized_user_list =  list(map(created_user, user_list))
    saved_user_list = [user.save() if user.is_valid() else False for user in serialized_user_list ]
    user_list = [user.set_password('cambiame') if user else False for user in saved_user_list]
    user_saved_list = list()
    for user in saved_user_list:
        if user:
            if user.username == 'admin':
                user.is_superuser = True
            user_saved_list.append(user.save())
    
    UserModel = get_user_model()

    assign_role(UserModel.objects.get(username='admin'), Admin)
    assign_role(UserModel.objects.get(username='general_dcc'), Reviewer)
    assign_role(UserModel.objects.get(username='information_provider'), InformationProvider)

def remove_create_user(apps, schema_editor):
    UserModel = get_user_model()
    UserModel.objects.filter(username='admin').delete()
    UserModel.objects.filter(username='general_dcc').delete()
    UserModel.objects.filter(username='information_provider').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_auto_20190322_2126')
    ]
    operations = [
        migrations.RunPython(add_create_user, reverse_code=remove_create_user),
    ]

