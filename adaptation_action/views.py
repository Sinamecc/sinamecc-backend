from rest_framework.decorators import api_view
from rest_framework import status
from general.helpers.views import ViewHelper
from adaptation_action.services import AdaptationActionServices
from rolepermissions.decorators import has_permission_decorator


service = AdaptationActionServices()
view_helper = ViewHelper(service)


@has_permission_decorator('read_adaptation_action')
def get_one_adaptation_action(request, pk):
    if request.method == 'GET':
        result = view_helper.get_one(request, pk)
    return result

@has_permission_decorator('read_adaptation_action')
def get_adaptation_action(request):
    if request.method == 'GET':
        result = view_helper.get_all(request)
    return result

@has_permission_decorator('create_adaptation_action')
def post_adaptation_action(request):
    if request.method == 'POST':
        result = view_helper.post(request)
    return result

@has_permission_decorator('edit_adaptation_action')
def put_adaptation_action(request, pk):
    if request.method == 'PUT':
        result = view_helper.put(request, pk)
    return result

@has_permission_decorator('edit_adaptation_action')
def patch_adaptation_action(request, pk):
    if request.method == 'PATCH':
        result = view_helper.patch(request, pk)
    return result

@has_permission_decorator('delete_adaptation_action')
def delete_adaptation_action(request, adaptation_action_id):
    if request.method == 'DELETE':
        result = view_helper.delete(adaptation_action_id)
    return result

## Permission!!!!
@api_view(['PUT'])
def upload_file_from_adaptation_action(request, adaptation_action_id, model_type):
    if request.method == 'PUT':
        result = view_helper.execute_by_name("upload_file_from_adaptation_action", request, adaptation_action_id, model_type)
    return result

@api_view(['GET'])
def get_file_to_adaptation_action(request, model_id, file_name):
    if request.method == 'GET':
        result = view_helper.call_download_file_method('download_file', request, model_id, file_name)

        return result


@api_view(['PUT'])
@has_permission_decorator('edit_adaptation_action')
def put_indicator_file_adaptation_action(request, adaptation_action_id, file_id):
    if request.method == 'PUT':
        result = view_helper.execute_by_name('upload_indicator_file_by_id', request, adaptation_action_id, file_id)

        return result


@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_indicator_file_adaptation_action(request, adaptation_action_id, file_id, file_field):
    if request.method == 'GET':
        result = view_helper.call_download_file_method('download_indicator_file_by_id', request ,adaptation_action_id, file_id, file_field)

        return result


@has_permission_decorator('edit_adaptation_action')
def _put_monitoring_indicator_file_adaptation_action(request, adaptation_action_id, file_id):
    
    if request.method == 'PUT':
        result = view_helper.execute_by_name('upload_monitoring_file_by_id', request, adaptation_action_id, file_id)

        return result


@has_permission_decorator('read_adaptation_action')
def _get_monitoring_indicator_file_adaptation_action(request, adaptation_action_id, file_id):
    
    if request.method == 'GET':
        result = view_helper.call_download_file_method('download_monitoring_indicator_file_by_id', request, adaptation_action_id, file_id)

        return result

@api_view(['GET', 'PUT'])
def get_put_monitoring_indicator_file_adaptation_action(request, adaptation_action_id, file_id):
        
        if request.method == 'PUT':
            result = _put_monitoring_indicator_file_adaptation_action(request, adaptation_action_id, file_id)
        elif request.method == 'GET':
            result = _get_monitoring_indicator_file_adaptation_action(request, adaptation_action_id, file_id)
        
        return result

## Permission!!!!
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def get_post_put_patch_delete(request, adaptation_action_id=False): ## We need delete *args this parametes is temp at the moment to refactor AA
    
    if request.method == 'GET' and adaptation_action_id:
        result = get_one_adaptation_action(request, adaptation_action_id)
    
    elif request.method == 'GET' and not adaptation_action_id:
        result = get_adaptation_action(request)
    
    elif request.method == 'POST' and not adaptation_action_id:
        result = post_adaptation_action(request)

    elif request.method == 'PUT' and adaptation_action_id:
        result = put_adaptation_action(request, adaptation_action_id)
        
    elif request.method == 'PATCH' and adaptation_action_id:
        result = patch_adaptation_action(request, adaptation_action_id)

    elif request.method == 'DELETE' and adaptation_action_id:
        result = delete_adaptation_action(request, adaptation_action_id)

    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_type_climate_threat(request, adaptation_action_id=False): ## We need delete *args this parametes is temp at the moment to refactor AA
    
    if request.method == 'GET' and adaptation_action_id:
        result = view_helper.get_one(request, adaptation_action_id)
    
    elif request.method == 'GET' and not adaptation_action_id:
        result = view_helper.execute_by_name("_get_all_type_climate_threat", request)

    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_benefited_population(request, benefited_population_id=False):
    if request.method == 'GET' and benefited_population_id:
        result = view_helper.execute_by_name("_get_benefited_population_by_id", request)
    
    elif request.method == 'GET' and not benefited_population_id:
        result = view_helper.execute_by_name("_get_all_benefited_population", request)

    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_ods(request, ods_id=False): ## We need delete *args this parametes is temp at the moment to refactor AA
    
    if request.method == 'GET' and ods_id:
        result = view_helper.get_one(request, ods_id)
    
    elif request.method == 'GET' and not ods_id:
        result = view_helper.execute_by_name("_get_all_ods", request)

    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_instrument_detail(request, instrument_id=False):
    if request.method == 'GET' and instrument_id:
        result = view_helper.get_one(request, instrument_id)
    
    elif request.method == 'GET' and not instrument_id:
        result = view_helper.execute_by_name("_get_all_instrument_detail", request)

    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_topics(request, topic_id=False):

    if request.method == 'GET' and not topic_id:
        result = view_helper.execute_by_name("_get_all_topic", request)
    
    elif request.method == 'GET' and topic_id:
        result = view_helper.execute_by_name("_get_topic_by_id", request, topic_id)
    
    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_subtopics(request, subtopic_id=False):

    if request.method == 'GET' and not subtopic_id:
        result = view_helper.execute_by_name("_get_all_subtopic", request)
    
    elif request.method == 'GET' and subtopic_id:
        result = view_helper.execute_by_name("_get_subtopic_by_id", request, subtopic_id)
    
    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_activities(request, activity_id=False):

    if request.method == 'GET' and not activity_id:
        result = view_helper.execute_by_name("_get_all_activity", request)
    
    elif request.method == 'GET' and activity_id:
        result = view_helper.execute_by_name("_get_activity_by_id", request, activity_id)
    
    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_information_source_type(request, information_source_type_id=False):

    if request.method == 'GET' and not information_source_type_id:
        result = view_helper.execute_by_name("_get_all_information_source_type", request)
    
    elif request.method == 'GET' and information_source_type_id:
        result = view_helper.execute_by_name("_get_information_source_type_by_id", request, information_source_type_id)
    
    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_general_impact(request, general_impact_id=False):

    if request.method == 'GET' and not general_impact_id:
        result = view_helper.execute_by_name("_get_all_general_impact", request)
    
    elif request.method == 'GET' and general_impact_id:
        result = view_helper.execute_by_name("_get_general_impact_by_id", request, general_impact_id)
    
    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_temporality_impact(request, temporality_impact_id=False):

    if request.method == 'GET' and not temporality_impact_id:
        result = view_helper.execute_by_name("_get_all_temporality_impact", request)
    
    elif request.method == 'GET' and temporality_impact_id:
        result = view_helper.execute_by_name("_get_temporality_impact_by_id", request, temporality_impact_id)
    
    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_general_impact(request, general_impact_id=False):

    if request.method == 'GET' and not general_impact_id:
        result = view_helper.execute_by_name("_get_all_general_impact", request)
    
    elif request.method == 'GET' and general_impact_id:
        result = view_helper.execute_by_name("_get_general_impact_by_id", request, general_impact_id)
    
    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_classifiers(request, classifier_id=False):

    if request.method == 'GET' and not classifier_id:
        result = view_helper.execute_by_name("_get_all_classifier", request)
    
    elif request.method == 'GET' and classifier_id:
        result = view_helper.execute_by_name("_get_classifier_by_id", request, classifier_id)

    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_source_type(request, source_type_id=False):

    if request.method == 'GET' and not source_type_id:
        result = view_helper.execute_by_name("_get_all_source_type", request)
    
    elif request.method == 'GET' and source_type_id:
        result = view_helper.execute_by_name("_get_source_type_by_id", request, source_type_id)
    
    return result

@api_view(['GET'])
@has_permission_decorator('read_adaptation_action')
def get_comments(request, adaptation_action_id, fsm_state=None, review_number=None):
    if request.method == 'GET' and not (fsm_state or review_number):
        result = view_helper.execute_by_name('get_current_comments', request, adaptation_action_id)

    elif request.method == 'GET' and (fsm_state or review_number):
        result = view_helper.execute_by_name('get_comments_by_fsm_state_or_review_number', request, adaptation_action_id, fsm_state, review_number)
        
    return result

@api_view(['GET'])
def get_change_log_from_adaptation_action(request, adaptation_action_id=None):

    if request.method == 'GET':
        result = view_helper.execute_by_name("get_change_log_from_adaptation_action", request, adaptation_action_id)
    return result
