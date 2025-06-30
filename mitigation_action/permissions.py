from rolepermissions.permissions import register_object_checker

from core.auth.roles import Admin, Reviewer, ReviewerMitigationAction


@register_object_checker()
def access_mitigation_action_register(role, user, mitigation_action_register):

    if user.mitigation_action.filter(pk=mitigation_action_register.id).first() is not None:
        return True
    
    if ReviewerMitigationAction == role or Reviewer == role  or Admin == role:
        return True

    return False
