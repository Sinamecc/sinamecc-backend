from django.conf.urls import url
from ppcn import views

urlpatterns = [
    url(
        r'^api/v1/ppcn/geographic/level/(?P<language>es|en)/*',
        views.get_geographic_level,
        name='get_geographic_level'
    ),
    url(
        r'^api/v1/ppcn/(?P<id>[0-9a-fA-F-]+)/file/(?P<ppcn_file_id>[0-9a-fA-F-]+)/*$',
        views.get_ppcn_file_version,
        name='get_ppcn_file_version'
    ),
    url(
        r'^api/v1/ppcn/required/level/(?P<language>es|en)/*',
        views.get_required_level,
        name='get_required_level'
    ),
    url(
        r'^api/v1/ppcn/recognition/type/(?P<language>[A-Za-z]*)/*$',
        views.get_recognition_type,
        name='get_recognition_type'
    ),
     url(r'^api/v1/ppcn/file/*$',
        views.post_ppcn_file,
        name='post_ppcn_file'
    ),
    url(
        r'^api/v1/ppcn/(?P<id>[0-9]+)/sector/(?P<language>[A-Za-z]*)/*$',
        views.get_sector,
        name='get_sector'
    ),
    url(
        r'^api/v1/ppcn/(?P<pk>[0-9]+)/subsector/(?P<language>[A-Za-z]*)/*$',
        views.get_sub_sector,
        name='get_sub_sector'
    ),
   
    url(r'^api/v1/ppcn/(?P<language>es|en)*/*$',
        views.get_post_ppcn,
        name='get_post_ppcn'
    ), 

    url(r'^api/v1/ppcn/(?P<id>[0-9a-f-]+)/(?P<language>[A-Za-z]*)/*$',
        views.get_one_ppcn,
        name='get_one_ppcn'
    ), 
    url(r'^api/v1/ppcn/(?P<id>[0-9a-f-]+)/*$',
        views.put_delete_ppcn,
        name='put_delete_ppcn'
    ),
    url(r'^api/v1/ppcn/form/(?P<geographicLevel_id>[0-9]+)/(?P<language>es|en)*/*$',
        views.get_form_ppcn,
        name='get_form_ppcn'
    )
   
]