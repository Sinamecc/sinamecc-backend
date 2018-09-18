from django.conf.urls import url
from ppcn.workflow_steps import views
urlpatterns = [
    url(
        r'^api/v1/ppcn/step/(?P<step_label>[a-z_]+)/*$',
        views.post,
        name='post_workflow_step'
    ),
    url(
        r'^api/v1/ppcn/step/(?P<step_label>[a-z_]+)/(?P<step_id>[0-9]+)/*$',
        views.get,
        name='get_workflow_step'
    ),
    url(
        r'^api/v1/ppcn/step/(?P<step_label>[a-z_]+)/(?P<step_id>[0-9]+)/file/(?P<step_file_id>[0-9]+)/*$',
        views.get_workflow_step_file,
        name='get_workflow_step_file'
    )
]