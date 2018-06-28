from django.conf.urls import url
from report_data import views


urlpatterns = [
    url(
        r'^api/v1/report_file/(?P<pk>[0-9]+)$',
        views.get_delete_update_report_file,
        name='get_delete_update_report_file'
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
        r'^api/v1/report_file/$',
        views.get_post_report_files,
        name='get_post_report_files'
    )
]