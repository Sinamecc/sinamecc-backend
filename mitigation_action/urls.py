from django.urls import path, re_path
from mitigation_action import views


urlpatterns_to_delete =[
    # ID: 1 replace with ID 1
    re_path(
        r'^api/v1/mitigations/form/(?P<language>[A-Za-z]+)/(?P<option>[A-Za-z]+)$',
        views.get_catalog_data,
        name='get_catalog_data_tmp',
    ),
]


urlpatterns = [
    # ID 1
    re_path(
        'api/v1/mitigation-action/data/$',
        views.get_catalog_data,
        name='get_catalog_data',
    )
]


