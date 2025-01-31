from django.urls import include, re_path, path
from django.contrib import admin

API_VERSION = 'v1'

urlpatterns = [
    path(f'api/v1/', include('users.urls')),
    path(f'api/v1/', include('mitigation_action.urls')),
    re_path(r'^', include('report_data.urls')),
    # re_path(r'^', include('mitigation_action.workflow_steps.urls')),
    re_path(r'^', include('adaptation_action.urls')),
    re_path(r'^', include('workflow.urls')),
    re_path(r'^', include('mccr.workflow_steps.urls')),
    re_path(r'^', include('mccr.urls')),
    re_path(r'^', include('ppcn.workflow_steps.urls')),
    re_path(r'^', include('ppcn.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include('general.urls'))
]
