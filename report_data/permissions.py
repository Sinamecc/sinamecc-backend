from rolepermissions.permissions import register_object_checker
from users.roles import Reviewer, ReviewerReportData, Admin

@register_object_checker()
def access_report_data_register(role, user, report_data_register):

    if user.report_data.filter(pk=report_data_register.id).first() is not None:
        return True
    
    if ReviewerReportData == role or Reviewer == role  or Admin == role:
        return True

    return False
