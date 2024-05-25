from django.db import models
from django.contrib.auth.models import User


def avatar_directory_path(instance: 'User', filename: str) -> str:
    return 'users/user_{pk}/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
    )
    fullName = models.CharField(
        max_length=200,
        default='',
        null=False,
        blank=True,
    )
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=50)
    avatar = models.ImageField(null=True,
                               blank=True,
                               upload_to=avatar_directory_path,
                               )

