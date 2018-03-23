from django.conf.urls import url
from mitigation_action import views

urlpatterns = [
    url(
        r'^api/v1/mitigation_action/',
        views.mitigation_action_test_request,
        name='mitigation_action_test_request'
    )
]
