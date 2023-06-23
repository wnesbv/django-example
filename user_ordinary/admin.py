
from django.contrib.admin import ModelAdmin, site
from .models import UserOrdinary


class UserOrdinaryAdmin(ModelAdmin):

    list_display = (
        "nickname",
        "mail",
        "is_active",
        "email_verified",
        "created_at",
        "modified_at",
    )

site.register(UserOrdinary, UserOrdinaryAdmin)
