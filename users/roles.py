from rolepermissions.roles import AbstractUserRole
from ppcn.permissions.permissions import *
from mitigation_action.permissions.permissions import *
from mccr.permissions.permissions import  *
class Admin(AbstractUserRole):

    role = 'Administrator'
    app = 'all'
    type = 'admin'
    available_permissions = {
        **permission_ppcn,
        **permission_ppcn_reviewer,
        **permission_mitigation_action,
        **permission_mitigation_action_reviewer, 
        **permission_mccr, 
        **permission_mccr_reviewer
    }
    

class Reviewer(AbstractUserRole):
    
    role = 'Reviewer'
    app = ['ppcn', 'ma', 'mccr']
    type = 'reviewer'
    available_permissions = {
        **permission_ppcn_reviewer,
        **permission_mitigation_action_reviewer,
        **permission_mccr_reviewer,
    }


class InformationProvider(AbstractUserRole):

    role = 'Information Provider'
    app = ['ppcn', 'ma', 'mccr']
    type = 'provider'
    available_permissions = {
        **permission_ppcn,
        **permission_mitigation_action,
        **permission_mccr
    }

## PPCN Roles
class ReviewerPPCN(AbstractUserRole):

    role = 'Reviewer PPCN'
    app = 'ppcn'
    type = 'reviewer'
    available_permissions = {
        **permission_ppcn,
        **permission_ppcn_reviewer,
    }

class InformationProviderPPCN(AbstractUserRole):

    role = 'Information Provider PPCN'
    app = 'ppcn'
    available_permissions = {
        **permission_ppcn
    }


## Mitigation Action Roles
class ReviewerMitigationAction(AbstractUserRole):

    role = 'Reviewer Mitigation Action'
    app = 'ma'
    type = 'reviewer'
    available_permissions = {
        **permission_mitigation_action,
        **permission_mitigation_action_reviewer,
    }

class InformationProviderMitigationAction(AbstractUserRole):
    
    role = 'Information Provider Mitigation Action'
    app = 'ma'
    type = 'provider'
    available_permissions = {
        **permission_mitigation_action
    }

# MCCR Permissions 

class ReviewerMCCR(AbstractUserRole):

    role = 'Reviewer MCCR'
    app = 'mccr'
    type = 'reviewer'
    available_permissions = {
        **permission_mccr, 
        **permission_mccr_reviewer
    }

class InformationProviderMCCR(AbstractUserRole):
    role = 'Information Provider MCCR'
    app = 'mccr'
    type = 'provider'
    available_permissions = {
        **permission_mccr
    }