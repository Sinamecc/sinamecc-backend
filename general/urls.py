from django.conf.urls import url
from general import views

urlpatterns = [
    url(
        r'^api/v1/user/(?P<username>[A-Za-z0-9\._-]+)$',
        views.get_user_info_by_name,
        name='get_user_info_by_name'
    ),
]
