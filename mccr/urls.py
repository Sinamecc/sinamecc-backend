from django.conf.urls import url
from mccr import views

urlpatterns = [
    url(
        r'^api/v1/mccr/(?P<id>[0-9a-fA-F-]+)/*$',
        views.get_mccr,
        name='get_mccr'
    ),
    url(
        r'^api/v1/mccr/(?P<id>[0-9a-fA-F-]+)/file/(?P<mccr_file_id>[0-9a-fA-F-]+)/*$',
        views.get_mccr_file_version,
        name='get_mccr_file_version'
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