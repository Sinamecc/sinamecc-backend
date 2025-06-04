from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from mitigation_action import _views

from .views import attachments

router = DefaultRouter(trailing_slash=False)
router.register('/attachments', attachments.AttachmentViewSet, basename='attachments')

MODULE = 'mitigation_action'

urlpatterns_to_delete =[
    # ID: 1 replace with ID 1
    re_path(
        r'^mitigations/form/(?P<language>[A-Za-z]+)/(?P<option>[A-Za-z]+)$',
        _views.get_catalog_data,
        name='get_catalog_data_tmp',
    ),
]

urlpatterns = [
    path(
        'mitigation-action/<uuid:pk>', include((router.urls, MODULE))
    ),
]
urlpatterns.extend( 
    [
        path(
            'mitigation-action/',
            _views.get_post_put_patch_delete,
            name='get_post_mitigation_action'
        ),

        path(
            'mitigation-action/<uuid:mitigation_action_id>/',
            _views.get_post_put_patch_delete,
            name='get_put_patch_delete_mitigation_action'
        ),
        path(
            'mitigation-action/<uuid:mitigation_action_id>/sent-to-review/',
            _views.send_to_review,
            name='send_to_review'
        ),
        path(
            'mitigation-action/data/',
            _views.get_catalog_data,
            name='get_catalog_data',
        ),
        path(
            'mitigation-action/data/<str:parent>/<int:parent_id>/<str:child>/',
            _views.get_catalog_data,
            name='get_child_data_catalog_by_parent_id',
        ),
        path(
            'mitigation-action/<uuid:mitigation_action_id>/indicator/',
            _views.get_indicator_from_mitigation_action,
            name='get_indicator_from_mitigation_action'
        ),
        path(
            'mitigation-action/<uuid:mitigation_action_id>/indicator/<int:indicator_id>/',
            _views.delete_indicator_from_mitigation_action,
            name='delete_indicator_from_mitigation_action'
        ),
        path(
            'mitigation-action/<uuid:mitigation_action_id>/file/<str:model_type>/',
            _views.upload_file_from_mitigation_action,
            name='upload_file_from_mitigation_action'
        ),
        path(
            'mitigation-action/<uuid:mitigation_action_id>/change-log/',
            _views.get_change_log_from_mitigation_action,
            name='get_change_log_from_mitigation_action'
        ),
        path('mitigation-action/<uuid:mitigation_action_id>/comments/',
            _views.get_comments,
            name='get_current_comments'
        ),
        path('mitigation-action/<uuid:mitigation_action_id>/<str:fsm_state>/comments/',
            _views.get_comments,
            name='get_comments_by_fsm_state'
        ),
        path('mitigation-action/<uuid:mitigation_action_id>/<str:fsm_state>/review/<int:review_number>/comments/',
            _views.get_comments,
            name='get_comments_by_fsm_state_and_review_number'
        ),
        path('mitigation-action/<uuid:mitigation_action_id>/review/<int:review_number>/comments/',
            _views.get_comments,
            name='get_comments_by_review_number'
        ),

    ]
)

urlpatterns.extend(urlpatterns_to_delete)


print(urlpatterns)