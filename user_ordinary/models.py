
from datetime import datetime, timedelta
from django.utils import timezone

from django.db import models


class UserOrdinary(models.Model):
    nickname = models.CharField(max_length=30, unique=True)
    mail = models.EmailField(max_length=120, unique=True)
    password = models.BinaryField()
    file = models.FileField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField("Date of creation", null=True)
    modified_at = models.DateTimeField("Date of change", null=True)

    def __str__(self):
        return self.mail
