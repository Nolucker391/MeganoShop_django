from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'pk', 'user', 'totalCost', 'status',
    list_display_links = 'pk', 'status'
    ordering = 'pk',
