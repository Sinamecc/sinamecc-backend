from django.urls import re_path
from workflow import views

urlpatterns = [
    re_path(
        r'^api/v1/workflow/status',
        views.get_review_status,
        name='get_review_status'
    )
]
