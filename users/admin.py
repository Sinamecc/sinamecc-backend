from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser as UserModel

## It's not to manage the user model in the admin panel
## It's just to show the user model in the admin panel
admin.site.register(UserModel, UserAdmin)