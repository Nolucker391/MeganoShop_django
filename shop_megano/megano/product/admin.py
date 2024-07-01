from django.contrib import admin

from .models import (
    Product,
    ProductImage,
    CategoryProduct,
    Tag,
    Sale,
    CategoryImage,
    ProductSpecification,
    Review,
)


@admin.register(CategoryProduct)
class CategoryAdmin(admin.ModelAdmin):
    """
    Раздел категории для админ панели.
    """

    list_display = "pk", "title"
    list_display_links = "pk", "title"
    ordering = ("pk",)


@admin.register(CategoryImage)
class CategoryAdmin(admin.ModelAdmin):
    """
    Раздел фотографии у категория для админ панели.
    """

    list_display = "pk", "src"
    list_display_links = "pk", "src"
    ordering = ("pk",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Раздел продуктов для админ панели.
    """

    list_display = "pk", "title", "price", "description", "archived", "fullDescription"
    list_display_links = "pk", "title"
    ordering = ("pk",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Раздел фотографии у продуктов для админ панели.
    """

    list_display = "pk", "name", "product"
    list_display_links = "pk", "name"
    ordering = ("pk",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Раздел тэгов для админ панели.
    """

    list_display = (
        "pk",
        "name",
    )
    list_display_links = "pk", "name"
    ordering = ("pk",)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Раздел распродажи для админ панели.
    """

    list_display = (
        "pk",
        "product",
    )
    list_display_links = ("pk",)
    ordering = ("pk",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Раздел отзыва у продукта для админ панели.
    """

    list_display = "pk", "author", "product", "date"
    list_display_links = ("pk",)
    ordering = ("pk",)


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    """
    Раздел харакетристика продукта для админ панели.
    """

    list_display = "pk", "name", "value", "product"
    list_display_links = "pk", "name"
    ordering = ("pk",)
