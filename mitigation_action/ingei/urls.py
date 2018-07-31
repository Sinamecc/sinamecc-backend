from django.conf.urls import url
from mitigation_action.ingei import views

urlpatterns = [
    url(
        r'^api/v1/mitigations/harmonization/ingei/$',
        views.post,
        name='post_harmonization_ingei_files'
    ),
    url(
        r'^api/v1/harmonization_ingei/(?P<id>[0-9]+)/file/(?P<harmonization_ingei_file_id>[0-9]+)/*$',
        views.get_harmonization_ingei_file_version,
        name='get_harmonization_ingei_file_version'
    )
]
