
from django.contrib.admin import ModelAdmin, site
from .models import UserPrivileged


class UserPrivilegedAdmin(ModelAdmin):

    list_display = (
        "username",
        "nickname",
        "mail",
        "password",
        "email_verified",
        "created_at",
        "modified_at",
    )

site.register(UserPrivileged, UserPrivilegedAdmin)
