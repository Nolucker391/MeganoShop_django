from django.contrib import admin

from .models import Product, ProductImage, CategoryProduct, Tag


@admin.register(CategoryProduct)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'pk', 'title'
    list_display_links = 'pk', 'title'
    ordering = 'pk',


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'title', 'price', 'description', 'archived', 'fullDescription'
    list_display_links = 'pk', 'title'
    ordering = 'pk',

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'product'
    list_display_links = 'pk', 'name'
    ordering = 'pk',

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name',
    list_display_links = 'pk', 'name'
    ordering = 'pk',
