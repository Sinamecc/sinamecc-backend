from django.conf.urls import url
from users import views

urlpatterns = [
    url(
        r'^api/v1/user/permissions/*$',
        views.get_permissions,
        name='get_permissions'
    ),
    url(
        r'^api/v1/user/groups/*$',
        views.get_groups,
        name='get_groups'
    ),
    url(
        r'^api/v1/user/*$',
        views.post_get_user,
        name='post_get_user'
    ),
    url(
        r'^api/v1/user/(?P<username>[A-Za-z0-9\._-]+)/permission/*$',
        views.assign_user_to_permission,
        name='assign_user_to_permission'
    ),

    url(
        r'^api/v1/user/(?P<username>[A-Za-z0-9\._-]+)/group/*$',
        views.assign_user_to_group,
        name='assign_user_to_group'
    )

    
]