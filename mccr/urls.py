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
        r'^api/v1/mccr/(?P<mccr_id>[0-9a-fA-F-]+)/ovv/(?P<ovv_id>[0-9]+)/*$',
        views.patch_mccr_ovv,
        name='patch_mccr_ovv'
    ),
    url(
        r'^api/v1/mccr/ovv/*$',
        views.get_all_ovv,
        name='get_all_ovv'
    ),
    url(
        r'^api/v1/mccr/*$',
        views.get_post_mccr,
        name='get_post_mccr'
    )
]