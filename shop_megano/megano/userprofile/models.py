from django.db import models
from django.contrib.auth.models import User


def upload_avatar_path(instance: 'Profile', filename: str) -> str:
    return "users/user_{pk}/avatars/{filename}".format(
        pk=instance.user.pk, filename=filename
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
    avatar = models.ImageField(null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return 'profile {user}'.format(user=self.user.username)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

