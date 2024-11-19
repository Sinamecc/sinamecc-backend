from django.urls import re_path
from ppcn import views


urlpatterns = [
    re_path(
        r'^api/v1/ppcn/geographic/level/(?P<language>es|en)*/*',
        views.get_geographic_level,
        name='get_geographic_level'
    ),
    re_path(
        r'^api/v1/ppcn/required/level/(?P<language>es|en)/*',
        views.get_required_level,
        name='get_required_level'
    ),
    re_path(
        r'^api/v1/ppcn/recognition/type/(?P<language>[A-Za-z]*)/*$',
        views.get_recognition_type,
        name='get_recognition_type'
    ),
    re_path(
        r'^api/v1/ppcn/(?P<id>[0-9]+)/sector/(?P<language>[A-Za-z]*)/*$',
        views.get_sector,
        name='get_sector'
    ),
    re_path(
        r'^api/v1/ppcn/(?P<pk>[0-9]+)/subsector/(?P<language>[A-Za-z]*)/*$',
        views.get_sub_sector,
        name='get_sub_sector'
    ),

    re_path(r'^api/v1/ppcn/(?P<language>es|en)*/*$',
        views.get_post_ppcn,
        name='get_post_ppcn'
    ), 

    re_path(
        r'^api/v1/ppcn/(?P<id>[0-9a-fA-F-]+)/ppcn_file/(?P<ppcn_file_id>[0-9a-fA-F-]+)/*$',
        views.get_ppcn_file,
        name='get_ppcn_file'
    ),
     re_path(r'^api/v1/ppcn/file/*$',
        views.post_ppcn_file,
        name='post_ppcn_file'
    ),

    re_path(
        r'^api/v1/ppcn/ovv/*$',
        views.get_all_ovv,
        name='get_all_ovv'
    ),
    
    re_path(r'^api/v1/ppcn/all/*(?P<language>es|en)*/*$',
        views.get_all_ppcn,
        name='get_all_ppcn'
    ), 
    re_path(r'^api/v1/ppcn/(?P<id>[0-9a-f-]+)/send/*$',
        views.send_to_review,
        name='send_to_review'
    ), 
    re_path(r'^api/v1/ppcn/(?P<id>[0-9a-f-]+)/(?P<language>es|en)*/*$',
        views.get_one_ppcn,
        name='get_one_ppcn'
    ), 
    re_path(r'^api/v1/ppcn/(?P<id>[0-9a-f-]+)/*$',
        views.put_delete_patch_ppcn,
        name='put_delete_patch_ppcn'
    ),
    re_path(r'^api/v1/ppcn/form/(?P<geographicLevel_id>[0-9]+)/(?P<language>es|en)*/*$',
        views.get_form_ppcn,
        name='get_form_ppcn'
    ),
    re_path(
        r'^api/v1/ppcn/changelog/(?P<id>[0-9a-f-]+)$',
        views.get_ppcn_change_log,
        name='get_ppcn_change_log'
    ),
    re_path(
        r'^api/v1/ppcn/(?P<id>[0-9a-fA-F-]+)/file/(?P<ppcn_file_id>[0-9a-zA-Z-]+)/*$',
        views.get_ppcn_file_version,
        name='get_ppcn_file_version'
    ),

    re_path(r'^api/v1/ppcn/(?P<ppcn_id>[0-9a-f-]+)/comments/*$',
        views.get_comments,
        name='get_comments'
    ),
    re_path(r'^api/v1/ppcn/(?P<ppcn_id>[0-9a-f-]+)/(?P<fsm_state>[A-Za-z0-9\._-]+)/comments/*$',
        views.get_comments,
        name='get_comments'
    ),
    re_path(r'^api/v1/ppcn/(?P<ppcn_id>[0-9a-f-]+)/(?P<fsm_state>[A-Za-z0-9\._-]+)/review/(?P<review_number>[0-9]+)/comments/*$',
        views.get_comments,
        name='get_comments'
    ),
    re_path(r'^api/v1/ppcn/(?P<ppcn_id>[0-9a-f-]+)/review/(?P<review_number>[0-9]+)/comments/*$',
        views.get_comments,
        name='get_comments'
    ),
    re_path(r'^api/v1/ppcn/(?P<ppcn_id>[0-9a-f-]+)/comments/*$',
        views.get_comments,
        name='get_comments'
    ),
]
