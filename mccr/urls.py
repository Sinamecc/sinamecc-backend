from django.conf.urls import url
from mccr import views

urlpatterns = [
    url(
        r'^api/v1/mccr/(?P<id>[0-9a-f-]+)/*$',
        views.get_mccr,
        name='get_mccr'
    ),
    url(
        r'^api/v1/mccr/form/*$',
        views.get_mccr_form,
        name='get_mccr_form'
    ),
    url(
        r'^api/v1/mccr/*$',
        views.get_post_mccr,
        name='get_post_mccr'
    )
]