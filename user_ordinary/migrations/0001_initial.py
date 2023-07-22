# Generated by Django 4.2.2 on 2023-07-22 06:41

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserOrdinary",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nickname", models.CharField(max_length=30, unique=True)),
                ("mail", models.EmailField(max_length=120, unique=True)),
                ("password", models.BinaryField()),
                ("file", models.FileField(blank=True, null=True, upload_to="")),
                (
                    "identifier",
                    models.CharField(
                        default="983299929745415fa340a5ea69b77116",
                        editable=False,
                        max_length=64,
                        unique=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("email_verified", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(null=True)),
                ("modified_at", models.DateTimeField(null=True)),
            ],
        ),
    ]
