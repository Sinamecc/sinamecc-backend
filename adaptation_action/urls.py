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
]