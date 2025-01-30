from django.urls import path, re_path
from mitigation_action import views


urlpatterns_to_delete =[
    # ID: 1 replace with ID 1
    re_path(
        r'^mitigations/form/(?P<language>[A-Za-z]+)/(?P<option>[A-Za-z]+)$',
        views.get_catalog_data,
        name='get_catalog_data_tmp',
    ),
]


urlpatterns = [
    path(
        'mitigation-action/',
        views.get_post_put_patch_delete,
        name='get_post_mitigation_action'
    ),

    path(
        'mitigation-action/<uuid:mitigation_action_id>/',
        views.get_post_put_patch_delete,
        name='get_put_patch_delete_mitigation_action'
    ),
    path(
        'mitigation-action/<uuid:mitigation_action_id>/sent-to-review/',
        views.send_to_review,
        name='send_to_review'
    ),
    path(
        'mitigation-action/data/',
        views.get_catalog_data,
        name='get_catalog_data',
    ),
    path(
        'mitigation-action/data/<str:parent>/<int:parent_id>/<str:child>/',
        views.get_catalog_data,
        name='get_child_data_catalog_by_parent_id',
    ),
    path(
        'mitigation-action/<uuid:mitigation_action_id>/indicator/',
        views.get_indicator_from_mitigation_action,
        name='get_indicator_from_mitigation_action'
    ),
    path(
        'mitigation-action/<uuid:mitigation_action_id>/indicator/<int:indicator_id>/',
        views.delete_indicator_from_mitigation_action,
        name='delete_indicator_from_mitigation_action'
    ),
    path(
        'mitigation-action/<uuid:mitigation_action_id>/file/<str:model_type>/',
        views.upload_file_from_mitigation_action,
        name='upload_file_from_mitigation_action'
    ),
    path(
        'mitigation-action/<uuid:mitigation_action_id>/change-log/',
        views.get_change_log_from_mitigation_action,
        name='get_change_log_from_mitigation_action'
    ),
    path('mitigation-action/<uuid:mitigation_action_id>/comments/',
        views.get_comments,
        name='get_current_comments'
    ),
    path('mitigation-action/<uuid:mitigation_action_id>/<str:fsm_state>/comments/',
        views.get_comments,
        name='get_comments_by_fsm_state'
    ),
    path('mitigation-action/<uuid:mitigation_action_id>/<str:fsm_state>/review/<int:review_number>/comments/',
        views.get_comments,
        name='get_comments_by_fsm_state_and_review_number'
    ),
    path('mitigation-action/<uuid:mitigation_action_id>/review/<int:review_number>/comments/',
        views.get_comments,
        name='get_comments_by_review_number'
    ),

]

urlpatterns.extend(urlpatterns_to_delete)


