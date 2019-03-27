from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class PermissionsHelper():
   
    ## Here permissions logic
    def __init__(self):
        self.request_type = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    ## End Points Permissions

    def userProviderPermission(self, request, instance_name , raise_exception=False):
        provider_information_permission = 'can_provide_information'
        if (request.method in self.request_type) and self.checkPermission(request.user, instance_name, provider_information_permission):
            return True

        if raise_exception:
            raise PermissionDenied

        return False
    
    def userDCCAdminPermission(self, request, instance_name , raise_exception=False):
        dcc_permission = 'user_dcc_permission'
        if (request.method in self.request_type) and self.checkPermission(request.user, instance_name, dcc_permission):
            return True

        if raise_exception:
            raise PermissionDenied

        return False
    
    
    def userPatchPermission(self, request, instance_name , raise_exception=False):

        provide_information_permission = 'can_provide_information'
        dcc_permission = 'user_dcc_permission'
        permissions_list = [provide_information_permission, dcc_permission]
        print(self.checkPermission(request.user, instance_name, permissions_list))

        if request.method == 'PATCH' and self.checkPermission(request.user, instance_name, permissions_list):
            return True

        if raise_exception:
            raise PermissionDenied

        return False

    ## Transition Permissions
    def userProvideInformationPermission(self, instance, user):

        provide_information_permission = 'can_provide_information'
        instance_name = ContentType.objects.get_for_model(instance).app_label
        return self.checkPermission(user, instance_name, provide_information_permission)
        
    def userCAPermission(self, instance, user):

        provide_ca_permission = 'user_ca_permission'
        instance_name = ContentType.objects.get_for_model(instance).app_label
        return self.checkPermission(user, instance_name, provide_ca_permission)
       

    def userDCCPermission(self, instance, user):

        dcc_permission = 'user_dcc_permission'
        instance_name = ContentType.objects.get_for_model(instance).app_label

        return self.checkPermission(user, instance_name, dcc_permission)
        
    
    def userExecutiveSecretaryPermission(self, instance, user):

        executive_secretary_permission = 'user_executive_secretary_permission'
        instance_name = ContentType.objects.get_for_model(instance).app_label

        return self.checkPermission(user, instance_name, executive_secretary_permission) 
        

    def checkPermission(self, user, instance, permission):
        if isinstance(permission, list):
            permission_list = []
            for p in permission:
                permission_list.append(user.has_perm( '%s.%s' % (instance, p)))
                return permission_list.count(True)

        return user.has_perm( '%s.%s' % (instance, permission))






