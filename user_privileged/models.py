
from django.contrib.auth.models import User
from django.db import models


class UserPrivileged(User):
    nickname = models.CharField(max_length=30)
    mail = models.EmailField(max_length=120, unique=True)
    file = models.FileField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    user_ptr = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
    )

    def __str__(self):
        return self.mail
