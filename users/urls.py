from django.urls import re_path, path
from users import views
from users.views.resources import UserResourcesViewSet
from users.views.password_management import PasswordManagementViewSet
from users.views.roles import UserRolesViewSet
from rest_framework.routers import DefaultRouter
from core.auth.utils import CustomTokenObtainPairView

router = DefaultRouter(trailing_slash=False, use_regex_path=False)
router.register(r'users', UserResourcesViewSet, 'users')
router.register(r'users', PasswordManagementViewSet, 'password-management')
router.register(r'users', UserRolesViewSet, 'roles')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
urlpatterns.extend(router.urls)