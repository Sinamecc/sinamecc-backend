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



## Permission!!!!
@api_view(['GET'])
def get_post_put_patch_delete(request, mitigation_action_id=False): ## We need delete *args this parametes is temp at the moment to refactor MA
    
    if request.method == 'GET' and mitigation_action_id:
        result = view_helper.get_one(request, mitigation_action_id)
    
    elif request.method == 'GET' and not mitigation_action_id:
        result = view_helper.get_all(request)

    return result