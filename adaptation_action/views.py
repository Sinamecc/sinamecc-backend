from rest_framework.decorators import api_view
from rest_framework import status
from general.helpers.views import ViewHelper
from adaptation_action.services import AdaptationActionServices
from rolepermissions.decorators import has_permission_decorator


service = AdaptationActionServices()
view_helper = ViewHelper(service)


# Create your views here.


## Permission!!!!
@api_view(['GET', 'POST', 'PUT'])
def get_post_put_patch_delete(request, adaptation_action_id=False): ## We need delete *args this parametes is temp at the moment to refactor AA
    
    if request.method == 'GET' and adaptation_action_id:
        result = view_helper.get_one(request, adaptation_action_id)
    
    elif request.method == 'GET' and not adaptation_action_id:
        result = view_helper.get_all(request)
    
    elif request.method == 'POST' and not adaptation_action_id:
        result = view_helper.post(request)

    elif request.method == 'PUT' and adaptation_action_id:
        result = view_helper.put(request, adaptation_action_id)

    return result
