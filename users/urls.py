from django.urls import re_path, path
from users import views
from users._views.resources import UserResourcesViewSet
from users._views.password_management import PasswordManagementViewSet
from rest_framework.routers import DefaultRouter



## NOTE: This urlpattern gonna be remove in the future
urlpatterns_old = [

    re_path(
        r'^user/(?P<user_id>[0-9]+)/profile_picture/(?P<image_id>[0-9]+)/*$',
        views.get_profile_picture_version,
        name='get_profile_picture_version',
    ),

    re_path(
        r'^user/(?P<user_id>[0-9]+)/profile_picture/*$',
        views.post_get_all_profile_picture,
        name='post_get_all_profile_picture',
    ),

    re_path(
        r'^user/permission/*$',
        views.post_get_permissions,
        name='post_get_permissions'
    ),

    re_path(
        r'^user/*$',
        views.post_get_user,
        name='post_get_user'
    ),
    re_path(
        r'^user/(?P<user_id>[0-9]+)/*$',
        views.put_delete_user,
        name='put_delete_user'
    ),
    re_path(
        r'^user/password/(?P<user_id>[0-9]+)/*$',
        views.put_password,
        name='put_password'
    ),
    re_path(
        r'^user/(?P<username>[A-Za-z0-9\._-]+)/permission/*$',
        views.assign_user_to_permission,
        name='assign_user_to_permission'
    ),

    re_path(
        r'^user/roles/*$',
        views.get_roles,
        name='get_roles'
    ),
    
    re_path(
        r'^user/(?P<user_id>[0-9]+)/roles/*$',
        views.assign_role_to_user,
        name='assign_role_to_user'
    ),

    re_path(
        r'^user/change_password/*$',
        views.request_to_change_password,
        name='request_to_change_password'
    ),

    re_path(
        r'^user/change_password/(?P<code>[A-Za-z0-9\._-]+)/(?P<token>[A-Za-z0-9\._-]+)/*$',
        views.update_password_by_request,
        name='update_password_by_request'
    ),

    
]

router = DefaultRouter(trailing_slash=False, use_regex_path=False)
router.register(r'users', UserResourcesViewSet, 'users')
router.register(r'users', PasswordManagementViewSet, 'password-management')

urlpatterns = []
urlpatterns.extend(router.urls)
urlpatterns.extend(urlpatterns_old)