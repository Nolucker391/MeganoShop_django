from django.contrib.auth.models import User
from django.db import models

from product.models import Product

class Order(models.Model):
    """
    Модель заказа продукта.
    """
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.PROTECT,
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    deliveryType = models.CharField(
        max_length=100,
        default='',
    )
    paymentType = models.CharField(
        max_length=100,
        default='',
    )
    totalCost = models.DecimalField(
        max_digits=8,
        default=1,
        decimal_places=2,
    )
    status = models.CharField(
        max_length=100,
        default='',
    )
    city = models.CharField(
        max_length=100,
        default='',
    )
    address = models.CharField(
        max_length=200,
        default='',
    )
    products = models.ManyToManyField(
        Product,
        related_name='orders',
    )

class OrdersCountProducts(models.Model):
    """
    Количество продуктов в заказе.

    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )
    count = models.PositiveIntegerField()


