from django.conf.urls import url
from mitigation_action import views

urlpatterns = [
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
