# Generated by Django 5.0.6 on 2024-05-25 16:01

import userprofile.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=userprofile.models.avatar_directory_path),
        ),
    ]