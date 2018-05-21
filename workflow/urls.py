from django.conf.urls import url
from workflow import views

urlpatterns = [
    url(
        r'^api/v1/workflow/status',
        views.get_review_status,
        name='get_review_status'
    )
]
