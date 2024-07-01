from django.db import models
from django.conf import settings
from product.models import Product


class UserCart(models.Model):
    """
    Модель корзины пользователя.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, through="BasketItem", related_name="products"
    )


class BasketItem(models.Model):
    """
    Модель данных корзины пользователя.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name="items")
    count = models.PositiveIntegerField(default=1)
