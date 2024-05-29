from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'pk', 'fullName', 'email', 'phone'
    list_display_links = 'pk', 'fullName'
    ordering = 'pk',

