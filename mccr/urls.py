from django.urls import re_path
from mccr import views

urlpatterns = [
    re_path(
        r'^api/v1/mccr/(?P<id>[0-9a-fA-F-]+)/*$',
        views.get_put_patch_delete_mccr,
        name='get_put_patch_delete_mccr'
    ),
    re_path(
        r'^api/v1/mccr/(?P<id>[0-9a-fA-F-]+)/file/(?P<mccr_file_id>[0-9a-fA-F-]+)/*$',
        views.get_mccr_file_version,
        name='get_mccr_file_version'
    ),
    re_path(
        r'^api/v1/mccr/form/*$',
        views.get_mccr_form,
        name='get_mccr_form'
    ),
    re_path(
        r'^api/v1/mccr/(?P<mccr_id>[0-9a-fA-F-]+)/ovv/(?P<ovv_id>[0-9]+)/*$',
        views.patch_mccr_ovv,
        name='patch_mccr_ovv'
    ),
    re_path(
        r'^api/v1/mccr/ovv/*$',
        views.get_all_ovv,
        name='get_all_ovv'
    ),
    re_path(
        r'^api/v1/mccr/*$',
        views.get_post_mccr,
        name='get_post_mccr'
    ),
]