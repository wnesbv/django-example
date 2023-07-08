
from datetime import datetime

from django.contrib.admin import site
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password

from .models import UserPrivileged

from import_export import resources, fields as fld
from import_export.admin import ImportMixin


class UserPrivilegedImpotAdmin(ImportMixin, UserAdmin):
    class PrivilegedResource(resources.ModelResource):

        password = fld.Field(attribute="password", default=make_password("password"))

        class Meta:

            if getattr(UserPrivileged, "created_at") is not None:
                exclude = "created_at"

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
                )
            },
        ),
    )


site.register(UserPrivileged, UserPrivilegedImpotAdmin)
