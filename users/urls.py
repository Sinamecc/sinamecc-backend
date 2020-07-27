from django.conf.urls import url
from users import views

urlpatterns = [

    url(
        r'^api/v1/user/(?P<user_id>[0-9]+)/profile_picture/(?P<image_id>[0-9]+)/*$',
        views.get_profile_picture_version,
        name='get_profile_picture_version',
    ),

    url(
        r'^api/v1/user/(?P<user_id>[0-9]+)/profile_picture/*$',
        views.post_get_all_profile_picture,
        name='post_get_all_profile_picture',
    ),

    url(
        r'^api/v1/user/permission/*$',
        views.post_get_permissions,
        name='post_get_permissions'
    ),

    url(
        r'^api/v1/user/*$',
        views.post_get_user,
        name='post_get_user'
    ),
    url(
        r'^api/v1/user/(?P<user_id>[0-9]+)/*$',
        views.put_user,
        name='put_user'
    ),
    url(
        r'^api/v1/user/password/(?P<user_id>[0-9]+)/*$',
        views.put_password,
        name='put_password'
    ),
    url(
        r'^api/v1/user/(?P<username>[A-Za-z0-9\._-]+)/permission/*$',
        views.assign_user_to_permission,
        name='assign_user_to_permission'
    ),

    url(
        r'^api/v1/user/roles/*$',
        views.get_roles,
        name='get_roles'
    ),
    
    url(
        r'^api/v1/user/(?P<user_id>[0-9]+)/roles/*$',
        views.assign_role_to_user,
        name='assign_role_to_user'
    ),

    url(
        r'^api/v1/user/change_password/*$',
        views.request_to_change_password,
        name='request_to_change_password'
    ),



    

    
]