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
    ),
    path(
        'api/v1/general/dimension/',
        views.get_dimension,
        name='get_dimension'
    ),
    path(
        'api/v1/general/category_group/',
        views.get_category_group,
        name='get_category_group'
    ),
    path(
        'api/v1/general/category/',
        views.get_category,
        name='get_category'
    ),
    path(
        'api/v1/general/category_ct/',
        views.get_category_ct,
        name='get_category_ct'
    ),
    path(
        'api/v1/general/characteristic/',
        views.get_characteristic,
        name='get_characteristic'
    )
]

urlpatterns.extend(urlpatterns_to_delete)