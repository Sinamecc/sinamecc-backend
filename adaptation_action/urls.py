from django.urls import path
from adaptation_action import views

urlpatterns = [
    path(
            'api/v1/adaptation-action/',
            views.get_post_put_patch_delete,
            name='get_post_adaptation_action'
        ),
    path(
            'api/v1/adaptation-action/<uuid:adaptation_action_id>/',
            views.get_post_put_patch_delete,
            name='get_put_patch_delete_adaptation_action'
        ),
    path(
            'api/v1/adaptation-action/type_climated_threat/',
            views.get_type_climated_threat,
            name='get_type_climated_threat'
    ),
    path(
            'api/v1/adaptation-action/get_ods/',
            views.get_ods,
            name='get_ods'
    ),
    path(
            'api/v1/adaptation-action/get_topics/',
            views.get_topics,
            name='get_topics'
    ),
    path(
            'api/v1/adaptation-action/get_subtopics/',
            views.get_subtopics,
            name='get_subtopics'
    ),
    path(
            'api/v1/adaptation-action/get_activities/',
            views.get_activities,
            name='get_activities'
    ),
    path(
            'api/v1/adaptation-action/get_information_source_type/',
            views.get_information_source_type,
            name='get_information_source_type'
    ),
    path(
            'api/v1/adaptation-action/get_general_impact/',
            views.get_general_impact,
            name='get_general_impact'
    ),

]