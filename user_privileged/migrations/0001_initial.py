# Generated by Django 4.2.2 on 2023-07-23 07:25

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserPrivileged",
            fields=[
                ("nickname", models.CharField(max_length=30)),
                ("mail", models.EmailField(max_length=120, unique=True)),
                ("file", models.FileField(blank=True, null=True, upload_to="")),
                (
                    "identifier",
                    models.CharField(
                        default="c492b2a8cc7d4e3da6f35c822d4a33ad",
                        editable=False,
                        max_length=64,
                        unique=True,
                    ),
                ),
                ("email_verified", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("modified_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user_ptr",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
