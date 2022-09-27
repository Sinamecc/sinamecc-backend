from rolepermissions.permissions import register_object_checker
from users.roles import Reviewer, ReviewerAdaptationAction, Admin

@register_object_checker()
def access_adaptation_action_register(role, user, adaptation_action_register):

    if user.adaptation_action.filter(pk=adaptation_action_register.id).first() is not None:
        return True
    
    if ReviewerAdaptationAction == role or Reviewer == role  or Admin == role:
        return True

    return False
