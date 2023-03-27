from django.conf.urls import url
from django.urls import path, include
from users.views import general
from users.views import user_request
from rest_framework import routers

NAMESPACE = 'users'

router = routers.DefaultRouter()
router.register(r'user-request', user_request.UserRequestViewSet, basename='user-request')

urlpatterns = [
    
    path('api/v1/', include((router.urls, NAMESPACE))),
    
    url(
        r'^api/v1/user/(?P<user_id>[0-9]+)/profile_picture/(?P<image_id>[0-9]+)/*$',
        general.get_profile_picture_version,
        name='get_profile_picture_version',
    ),

    url(
        r'^api/v1/user/(?P<user_id>[0-9]+)/profile_picture/*$',
        general.post_get_all_profile_picture,
        name='post_get_all_profile_picture',
    ),

    url(
        r'^api/v1/user/permission/*$',
        general.post_get_permissions,
        name='post_get_permissions'
    ),

    url(
        r'^api/v1/user/*$',
        general.post_get_user,
        name='post_get_user'
    ),
    url(
        r'^api/v1/user/(?P<user_id>[0-9]+)/*$',
        general.put_delete_user,
        name='put_delete_user'
    ),
    url(
        r'^api/v1/user/password/(?P<user_id>[0-9]+)/*$',
        general.put_password,
        name='put_password'
    ),
    url(
        r'^api/v1/user/(?P<username>[A-Za-z0-9\._-]+)/permission/*$',
        general.assign_user_to_permission,
        name='assign_user_to_permission'
    ),

    url(
        r'^api/v1/user/roles/*$',
        general.get_roles,
        name='get_roles'
    ),
    
    url(
        r'^api/v1/user/(?P<user_id>[0-9]+)/roles/*$',
        general.assign_role_to_user,
        name='assign_role_to_user'
    ),

    url(
        r'^api/v1/user/change_password/*$',
        general.request_to_change_password,
        name='request_to_change_password'
    ),

    url(
        r'^api/v1/user/change_password/(?P<code>[A-Za-z0-9\._-]+)/(?P<token>[A-Za-z0-9\._-]+)/*$',
        general.update_password_by_request,
        name='update_password_by_request'
    ),

]
