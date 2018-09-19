from django.conf.urls import url
from mitigation_action import views

urlpatterns = [
    url(
        r'^api/v1/mitigations/$',
        views.post_mitigations,
        name='post_mitigations'
    ),
    url(
        r'^api/v1/mitigations/changelog/(?P<pk>[0-9a-f-]+)$',
        views.get_mitigation_change_log,
        name='get_mitigation_change_log'
    ),
    url(
        r'^api/v1/mitigations/form/(?P<language>[A-Za-z]+)/(?P<option>[A-Za-z]+)$',
        views.get_mitigations_form_es_en,
        name='get_mitigations_form_es_en',
    ),
    url(
        r'^api/v1/mitigations/form',
        views.get_mitigations_form,
        name='get_mitigations_form'
    ),
    url(
        r'^api/v1/mitigations/(?P<language>[A-Za-z0-9]+)$',
        views.get_mitigation,
        name='get_mitigation'
    ),
    url(
        r'^api/v1/mitigations(/(?P<language>[A-Za-z]{2}))?/(?P<pk>[0-9a-zA-Z\-]+)$',
        views.get_delete_put_patch_mitigation,
        name='get_delete_put_patch_mitigation'
    ),
    url(
        r'^api/v1/mitigations/(?P<id>[0-9a-fA-F-]+)/file/(?P<file_id>[0-9a-fA-F-]+)/*$',
        views.get_mitigation_action_file,
        name='get_mitigation_action_file'
    ),
]
