from django.conf.urls import url
from mitigation_action import views

urlpatterns = [
    url(
        r'^api/v1/mitigation/(?P<pk>[0-9a-f-]+)$',
        views.get_delete_update_mitigation,
        name='get_delete_update_mitigation'
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
