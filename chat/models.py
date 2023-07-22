
from django.db import models
from django.contrib.auth.models import User

from user_ordinary.models import UserOrdinary
from user_privileged.models import UserPrivileged


class UserChat(models.Model):
    nick = models.CharField(max_length=30, null=False)
    remark = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    #..
    user_chat = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE, parent_link=True
    )
    or_chat = models.ForeignKey(
        UserOrdinary, null=True, blank=True, on_delete=models.CASCADE
    )
    pr_chat = models.ForeignKey(
        UserPrivileged, null=True, blank=True, on_delete=models.CASCADE
    )
    # ..
    recipient = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.nick
