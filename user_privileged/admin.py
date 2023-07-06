
from django.contrib.admin import site
from django.contrib.auth.admin import UserAdmin
from .models import UserPrivileged

from import_export import resources
from import_export.admin import ImportMixin


class UserPrivilegedImpotAdmin(ImportMixin, UserAdmin):
    class PrivilegedResource(resources.ModelResource):
        class Meta:
            model = UserPrivileged
            fields = (
                "id",
                "username",
                "nickname",
                "password",
                "mail",
                "email_verified",
                "created_at",
                "modified_at",
                "user_ptr_id",
            )

    resource_class = PrivilegedResource

    list_display = (
        "id",
        "username",
        "nickname",
        "user_ptr",
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


site.register(UserPrivileged, UserPrivilegedImpotAdmin)