import uuid

from django.db import models


class UserOrdinary(models.Model):
    nickname = models.CharField(max_length=30, unique=True)
    mail = models.EmailField(max_length=120, unique=True)
    password = models.BinaryField()
    file = models.FileField(null=True, blank=True)
    identifier = models.CharField(
        max_length=64,
        unique=True,
        default=uuid.uuid4().hex,
        editable=False,
    )
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.mail)
