from rolepermissions.roles import AbstractUserRole

## permission for PPCN
permission_ppcn = {
    'create_ppcn': True, 
    'read_ppcn': True, 
    'edit_ppcn': True, 
    'delete_ppcn': True, 
}

permission_ppcn_reviewer = {
    'create_ppcn': True, 
    'read_all_ppcn': True, 
    'edit_ppcn': True, 
    'delete_ppcn': True, 
}

## permission for MA
permission_ma = {
    'create_mitigation_action': True, 
    'read_mitigation_action': True, 
    'edit_mitigation_action': True, 
    'delete_mitigation_action': True, 
}

permission_ma_reviewer = {
    'create_mitigation_action': True, 
    'read_all_mitigation_action': True, 
    'edit_mitigation_action': True, 
    'delete_mitigation_action': True, 
}


## permission for MCCR
permission_mccr = {
    'create_mccr': True,  
    'read_mccr': True, 
    'edit_mccr': True, 
    'delete_mccr': True, 
}

permission_mccr_reviewer = {
    'create_mccr': True,  
    'read_all_mccr': True, 
    'edit_mccr': True, 
    'delete_mccr': True, 
}



class Admin(AbstractUserRole):
    available_permissions = {
        **permission_ppcn,
        **permission_ppcn_reviewer,
        **permission_ma,
        **permission_ma_reviewer,
        **permission_mccr,
        **permission_mccr_reviewer,
    }

class Reviewer(AbstractUserRole):
    available_permissions = {
        **permission_ppcn_reviewer,
        **permission_ma_reviewer,
        **permission_mccr_reviewer,
    }

class InformationProvider(AbstractUserRole):
    available_permissions = {
        **permission_ppcn,
        **permission_ma,
        **permission_mccr,
    }
ROLEPERMISSIONS_REGISTER_ADMIN = True