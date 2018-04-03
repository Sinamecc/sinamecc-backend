from django.conf.urls import url
from mitigation_action import views

urlpatterns = [
    url(
        r'^api/v1/mitigation_action/',
        views.get_post_mitigation_actions,
        name='get_post_mitigation_actions'
    )
]
