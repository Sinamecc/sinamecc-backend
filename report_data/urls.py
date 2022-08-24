from django.conf.urls import url
from django.urls import path, re_path
from report_data import views


urlpatterns = [
    url(
        r'^api/v1/report-data/report/(?P<pk>[0-9]+)/*$',
        views.get_delete_update_patch_report_data,
        name='get_delete_update_patch_report_data'
    ),
    url(
        r'^api/v1/report_file/(?P<pk>[0-9]+)/versions$',
        views.get_report_file_versions,
        name='get_report_file_versions'
    ),
    url(
        r'^api/v1/report_file/(?P<report_file_id>[0-9]+)/version/(?P<report_file_version_id>[0-9]+)$',
        views.get_report_file_version_url,
        name='get_report_file_version_url'
    ),
    url(
        r'^api/v1/report-data/report/$',
        views.get_post_report_data,
        name='get_post_report_data'
    ),
    path(
        'api/v1/report-data/data/', 
        views.get_catalog_data, 
        name='get_catalog_data'
    ),
    path(
        'api/v1/report-data/report/<int:report_data_id>/file/',
        views.upload_file_to_report_data, 
        name='upload_file_to_report_data'
    ),
    path(
        'api/v1/report-data/report/file/<int:report_file_id>/',
        views.get_file_to_report_data, 
        name='get_file_to_report_data'
    ),
    path(
        'api/v1/report-data/report/<int:report_data_id>/source-file/',
        views.get_source_file_to_report_data, 
        name='get_source_file_to_report_data'
    ),
    path(
        'api/v1/report-data/report/<int:report_data_id>/<str:fsm_state>/comments/',
        views.get_comments,
        name='get_comments'
    ),
    path(
        'api/v1/report-data/report/<int:report_data_id>/comments/',
        views.get_comments,
        name='get_comments'
    ),
    path(
        'api/v1/report-data/report/<int:report_data_id>/<str:fsm_state>/review/<int:review_number>/comments/',
        views.get_comments,
        name='get_comments'
    ),
    path(
        'api/v1/report-data/report/<int:report_data_id>/review/<int:review_number>/comments/',
        views.get_comments,
        name='get_comments'
    ),

]
