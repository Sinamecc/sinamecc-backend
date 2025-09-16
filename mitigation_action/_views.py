from rest_framework import status
from rest_framework.decorators import api_view
from rolepermissions.decorators import has_permission_decorator

from general.helpers.views import ViewHelper
from mitigation_action._services import MitigationActionService

service = MitigationActionService()
view_helper = ViewHelper(service)


@api_view(['PUT'])
def send_to_review(request, mitigation_action_id):
    """
    Send mitigation action to review
    """
    if request.method == 'PUT':
        result = view_helper.execute_by_name('sent_to_review', request, mitigation_action_id)
        
    return result


## Permission!!!!
@api_view(['GET'])
def get_catalog_data(request, parent=None, parent_id=None, child=None, **kwargs): ## We need delete *args this parametes is temp at the moment to refactor MA
    if request.method == 'GET' and not parent:
        result = view_helper.execute_by_name("get_catalog_data", request)

    elif request.method == 'GET' and all([parent, parent_id, child]):
        result = view_helper.execute_by_name("get_child_data_from_parent_id_catalogs", request, parent, parent_id, child)

    return result


## Permission!!!!
@api_view(['GET'])
def get_indicator_from_mitigation_action(request, mitigation_action_id=False):

    if request.method == 'GET':
        result = view_helper.execute_by_name("get_indicator_from_mitigation_action", request, mitigation_action_id)
    return result


## Permission!!!!
@api_view(['DELETE'])
def delete_indicator_from_mitigation_action(request, mitigation_action_id=None, indicator_id=None):

    if request.method == 'DELETE':
        result = view_helper.execute_by_name("delete_indicator_from_mitigation_action", request, mitigation_action_id, indicator_id)
    return result


## Permission!!!!
@api_view(['GET'])
def get_change_log_from_mitigation_action(request, mitigation_action_id=None):

    if request.method == 'GET':
        result = view_helper.execute_by_name("get_change_log_from_mitigation_action", request, mitigation_action_id)
    return result


## Permission!!!!
@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def get_post_put_patch_delete(request, mitigation_action_id=False): ## We need delete *args this parametes is temp at the moment to refactor MA
    
    if request.method == 'GET' and mitigation_action_id:
        result = view_helper.get_one(request, mitigation_action_id)
    
    elif request.method == 'GET' and not mitigation_action_id:
        result = view_helper.get_all(request)
    
    elif request.method == 'POST' and not mitigation_action_id:
        result = view_helper.post(request)

    elif request.method == 'PUT' and mitigation_action_id:
        result = view_helper.put(request, mitigation_action_id)
    
    elif request.method == 'PATCH' and mitigation_action_id:
        result = view_helper.patch(request, mitigation_action_id)

    return result


## Permission!!!!
@api_view(['PUT'])
def upload_file_from_mitigation_action(request, mitigation_action_id, model_type):
    if request.method == 'PUT':
        result = view_helper.execute_by_name("upload_file_from_mitigation_action", request, mitigation_action_id, model_type)
    return result


## Permission!!!!
@api_view(['GET'])
def get_comments(request, mitigation_action_id, fsm_state=False, review_number=False):
    if request.method == 'GET' and not (fsm_state or review_number):
        result = view_helper.execute_by_name('get_current_comments', request, mitigation_action_id)

    elif request.method == 'GET' and (fsm_state or review_number):
        result = view_helper.execute_by_name('get_comments_by_fsm_state_or_review_number', request, mitigation_action_id, fsm_state, review_number)

    return result


@api_view(['GET', 'PUT', 'POST'])
def get_put_indicator(request, mitigation_action_id=False):
    if request.method == 'GET' and mitigation_action_id:
        result = view_helper.execute_by_name('_get_indicator', request, mitigation_action_id)

    elif request.method == 'PUT':
        result = view_helper.execute_by_name('_create_update_indicator', request, mitigation_action_id)

    elif request.method == 'POST':
        result = view_helper.execute_by_name('_create_indicator', request)

    return result


@api_view(['GET'])
def get_indicator(request, mitigation_action_id):
    result = view_helper.execute_by_name('_get_all_indicator', request, mitigation_action_id)
    return result