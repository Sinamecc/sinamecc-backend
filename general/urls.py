from django.conf.urls import url
from general import views

urlpatterns = [
    url(
        r'^api/v1/user/(?P<username>[a-zA-Z0-9]+)$',
        views.get_user_info_by_name,
        name='get_user_info_by_name'
    ),
]