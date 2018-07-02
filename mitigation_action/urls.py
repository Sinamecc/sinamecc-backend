from django.conf.urls import url
from mitigation_action import views

urlpatterns = [
    url(
        r'^api/v1/mitigations/(?P<pk>[0-9a-f-]+)$',
        views.get_delete_update_patch_mitigation,
        name='get_delete_update__patch_mitigation'
    ),
    url(
        r'^api/v1/mitigations/changelog/(?P<pk>[0-9a-f-]+)$',
        views.get_mitigation_change_log,
        name='get_mitigation_change_log'
    ),
    url(
        r'^api/v1/mitigations/form/(?P<language>[A-Za-z0-9]+)$',
        views.get_mitigations_form_es_en,
        name='get_mitigations_form_es_en',
    ),
    url(
        r'^api/v1/mitigations/form',
        views.get_mitigations_form,
        name='get_mitigations_form'
    ),
    url(
        r'^api/v1/mitigations/',
        views.get_post_mitigations,
        name='get_post_mitigations'
    )
]
