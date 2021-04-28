from rest_framework.decorators import api_view
from rest_framework import status
from general.helpers.views import ViewHelper
from mitigation_action.services import MitigationActionService
from rolepermissions.decorators import has_permission_decorator

service = MitigationActionService()
view_helper = ViewHelper(service)


## Permission!!!!
@api_view(['GET'])
def get_catalog_data(request, **kwargs): ## We need delete *args this parametes is temp at the moment to refactor MA
    if request.method == 'GET':
        result = view_helper.execute_by_name("get_catalog_data", request)
    return result