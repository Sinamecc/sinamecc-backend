from rolepermissions.roles import AbstractUserRole
from ppcn.permissions.permissions import *
from mitigation_action.permissions.permissions import *
from mccr.permissions.permissions import  *
from users.permissions.permissions import *  
from adaptation_action.permissions.permissions import *
from report_data.permissions.permissions import *

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
        **permission_mccr_reviewer,
        **permission_users,
        **permission_adaptation_action,
        **permission_adaptation_action_reviewer,
        **permission_report_data,
        **permission_report_data_reviewer,
    }
    

class Reviewer(AbstractUserRole):
    
    role = 'Reviewer'
    app = ['ppcn', 'ma', 'mccr', 'aa', 'rd']
    type = 'reviewer'
    available_permissions = {
        **permission_ppcn_reviewer,
        **permission_mitigation_action_reviewer,
        **permission_mccr_reviewer,
        **permission_adaptation_action_reviewer,
        **permission_report_data_reviewer,
    }


class InformationProvider(AbstractUserRole):

    role = 'Information Provider'
    app = ['ppcn', 'ma', 'mccr', 'aa', 'rd']
    type = 'provider'
    available_permissions = {
        **permission_ppcn,
        **permission_mitigation_action,
        **permission_mccr,
        **permission_adaptation_action,
        **permission_report_data,
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
    type = 'provider'
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

## Adaptation Action Roles
class ReviewerAdaptationAction(AbstractUserRole):

    role = 'Reviewer Adaptation Action'
    app = 'aa'
    type = 'reviewer'
    available_permissions = {
        **permission_adaptation_action,
        **permission_adaptation_action_reviewer,
    }

class InformationProviderAdaptationAction(AbstractUserRole):

    role = 'Information Provider Adaptation Action'
    app = 'aa'
    type = 'provider'
    available_permissions = {
        **permission_adaptation_action
    }

## Report Data Roles
class ReviewerReportData(AbstractUserRole):

    role = 'Reviewer Report Data'
    app = 'rd'
    type = 'reviewer'
    available_permissions = {
        **permission_report_data,
        **permission_report_data_reviewer,
    }

class InformationProviderReportData(AbstractUserRole):
    
    role = 'Information Provider Report Data'
    app = 'rd'
    type = 'provider'
    available_permissions = {
        **permission_report_data
    }