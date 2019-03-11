from django.contrib.auth.models import Group,Permission
class PermissionsHelper():

    ## Here permissions logic
    def __init__(self):
        pass

    def userProvideInformationPermission(self, instance, user):

        provide_information_permission_list = ['can_provide_information_ppcn']
        instance_permission_list = [permission_tuple[0] for permission_tuple in  instance._meta.permissions]

        return self.checkPermissions(instance_permission_list, user, provide_information_permission_list)

        
    def userCAPermission(self, instance, user):

        permission_list_CA = ['user_ca_permission_ppcn']
        instance_permission_list = [permission_tuple[0] for permission_tuple in  instance._meta.permissions]

        return self.checkPermissions(instance_permission_list, user, permission_list_CA)
       

    def userDCCPermission(self, instance, user):

        permission_list_dcc= ['user_dcc_permission_ppcn']
        instance_permission_list = [permission_tuple[0] for permission_tuple in  instance._meta.permissions]

        return self.checkPermissions(instance_permission_list, user, permission_list_dcc)
        
    
    def userExecutiveSecretaryPermission(self, instance, user):

        permission_list_dcc= ['user_executive_secretary_permission_ppcn']
        instance_permission_list = [permission_tuple[0] for permission_tuple in  instance._meta.permissions]

        return self.checkPermissions(instance_permission_list, user, permission_list_dcc)
        

    def checkPermissions(self, instance_permission_list, user, permission_list):

        ## the intersection can be only of one element
        permission = list(set(instance_permission_list).intersection(permission_list))[0]

        if permission and self.generalGroupPermissions(user, permission):
            print("debbuger: User has permission for this transition - Provide")
            return True
        
        print("debbuger: User has not permission for this transition - Provide")
        return False


    def generalGroupPermissions(self,user, transition_permission):
        
        for group in user.groups.all():
            permissions = group.permissions.all()

            for permission in permissions:
                if permission.codename == transition_permission:
                    return True
                    
        return False




