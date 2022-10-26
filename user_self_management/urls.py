from django.urls import path
from user_self_management import views


urlpatterns = [
    path(
        'api/v1/user-self-management/',
        views.get_post_user_self_management,
        name='get_post_user_self_management'
    ),
]