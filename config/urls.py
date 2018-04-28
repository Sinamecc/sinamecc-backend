from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^', include('report_data.urls')),
    url(r'^', include('mitigation_action.urls')),
    url(r'^', include('workflow.urls')),
    url(r'^', include('general.urls')),
    url(r'^api/v1/token/', obtain_jwt_token),
    url(r'^admin/', admin.site.urls),
]
