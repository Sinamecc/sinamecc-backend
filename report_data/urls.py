from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/v1/report_file/(?P<pk>[0-9]+)$',
        views.get_delete_update_report_file,
        name='get_delete_update_report_file'
    ),
    url(
        r'^api/v1/report_file/$',
        views.get_post_report_files,
        name='get_post_report_files'
    ),
    url(
        r'^api/v1/health/$',
        views.get_health_status,
        name='get_health_status'
    ),
    
]