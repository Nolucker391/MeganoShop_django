# Generated by Django 4.2 on 2024-07-01 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userprofile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fullName", models.CharField(blank=True, default="", max_length=200)),
                ("email", models.EmailField(max_length=200)),
                ("phone", models.CharField(max_length=50)),
                (
                    "avatar",
                    models.ImageField(
                        null=True, upload_to=userprofile.models.upload_avatar_path
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "profile",
                "verbose_name_plural": "profiles",
            },
        ),
    ]
