from django.urls import re_path
from general import views
from django.urls import path, re_path


urlpatterns_to_delete = [

    re_path(r'^.*$', views.handler404),
]

urlpatterns = [ 
    path(
        'api/v1/general/province/',
        views.get_post_province,
        name='get_post_province'
    ),
    path(
        'api/v1/general/canton/',
        views.get_post_canton,
        name='get_post_canton'
    ),
    path(
        'api/v1/general/canton/<int:canton_id>/',
        views.get_post_canton,
        name='get_post_canton'
    ),
    path(
        'api/v1/general/district/',
        views.get_post_district,
        name='get_post_district'
    ),
    path(
        'api/v1/general/district/<int:district_id>/',
        views.get_post_district,
        name='get_post_district'
    )
]

urlpatterns.extend(urlpatterns_to_delete)