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
   
    path(
        'api/v1/mitigation-action/',
        views.get_post_put_patch_delete,
        name='get_post_mitigation_action'
    ),

    path(
        'api/v1/mitigation-action/<uuid:mitigation_action_id>/',
        views.get_post_put_patch_delete,
        name='get_put_patch_delete_mitigation_action'
    ),

    path(
        'api/v1/mitigation-action/data/',
        views.get_catalog_data,
        name='get_catalog_data',
    ),

    path(
        'api/v1/mitigation-action/<uuid:mitigation_action_id>/indicator/',
        views.get_indicator_from_mitigation_action,
        name='get_indicator_from_mitigation_action'
    )

    
]

urlpatterns.extend(urlpatterns_to_delete)


