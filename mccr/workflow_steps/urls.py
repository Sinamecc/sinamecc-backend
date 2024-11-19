from django.urls import re_path
from mccr.workflow_steps import views

urlpatterns = [
    re_path(
        r'^api/v1/mccr/step/(?P<step_label>[a-z_]+)/*$',
        views.post,
        name='post_workflow_step'
    ),
    re_path(
        r'^api/v1/mccr/step/(?P<step_label>[a-z_]+)/(?P<step_id>[0-9]+)/*$',
        views.get,
        name='get_workflow_step'
    ),
    re_path(
        r'^api/v1/mccr/step/(?P<step_label>[a-z_]+)/(?P<step_id>[0-9]+)/file/(?P<step_file_id>[0-9]+)/*$',
        views.get_workflow_step_file_version,
        name='get_workflow_step_file_version'
    )
]
