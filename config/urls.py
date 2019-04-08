from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^', include('report_data.urls')),
    url(r'^', include('mitigation_action.workflow_steps.urls')),
    url(r'^', include('mitigation_action.urls')),
    url(r'^', include('workflow.urls')),
    url(r'^', include('mccr.workflow_steps.urls')),
    url(r'^', include('mccr.urls')),
    url(r'^', include('ppcn.workflow_steps.urls')),
    url(r'^', include('ppcn.urls')),
    url(r'^', include('users.urls')),
    url(r'^api/v1/token/', obtain_jwt_token),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('general.urls'))
]
