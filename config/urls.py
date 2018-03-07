from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^', include('report_data.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^admin/', admin.site.urls),
]
