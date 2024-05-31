from django.contrib import admin

from .models import Product, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'title', 'price', 'description', 'archived'
    list_display_links = 'pk', 'title'
    ordering = 'pk',

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'product'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
