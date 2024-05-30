from django.contrib import admin

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'price', 'description', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
