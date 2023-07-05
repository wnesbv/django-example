from django.contrib.admin import ModelAdmin, site
from django.contrib.auth.admin import UserAdmin
from .models import UserPrivileged


class UserPrivilegedAdmin(UserAdmin):
    list_display = (
        "username",
        "nickname",
        "password",
        "mail",
        "email_verified",
        "created_at",
        "modified_at",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "nickname",
                    "password",
                    "mail",
                    "email_verified",
                    "created_at",
                    "modified_at",
                )
            },
        ),
    )


site.register(UserPrivileged, UserPrivilegedAdmin)
