from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class OrdersDeliveryType(models.Model):

    deliveryType = models.CharField(
        max_length=100,
        default='',
    )



class Order(models.Model):
    """
    Модель заказа продукта.
    """
    CHOICES = (
        ('aw', 'awaiting'),
        ('ac', 'accepted'),
    )
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.PROTECT,
    )
    createdAt = models.DateTimeField(auto_now_add=True)

    paymentType = models.CharField(
        max_length=100,
        default='',
    )

    deliveryType = models.ForeignKey(
        OrdersDeliveryType,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    totalCost = models.DecimalField(
        max_digits=8,
        default=1,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=100,
        choices=CHOICES,
    )
    city = models.CharField(
        max_length=100,
        default='',
    )
    address = models.CharField(
        max_length=200,
        default='',
    )

    fullName = models.CharField(
        max_length=200,
        default='',
        null=False,
        blank=True,
    )
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    products = models.ManyToManyField(
        Product,
        related_name='orders',
        through='OrdersCountProducts',
    )

class OrdersCountProducts(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )
    count = models.PositiveIntegerField(
        null=True,
    )

