from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class OrdersDeliveryType(models.Model):

    deliveryType = models.CharField(
        max_length=100,
        default="",
    )
    # cost =
    # type = choices


class Order(models.Model):
    """
    Модель заказа продукта.
    """

    CHOICES = (
        ("aw", "awaiting"),
        ("ac", "accepted"),
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    user = models.ForeignKey(
        User,
        related_name="orders",
        on_delete=models.PROTECT,
    )
    createdAt = models.DateTimeField(auto_now_add=True)

    paymentType = models.CharField(
        max_length=100,
        default="",
    )

    deliveryType = models.ForeignKey(
        OrdersDeliveryType,
        related_name="orders",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    totalCost = models.DecimalField(
        max_digits=8,
        default=0.0,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=100,
        choices=CHOICES,
    )
    city = models.CharField(
        max_length=100,
        default="",
    )
    address = models.CharField(
        max_length=200,
        default="",
    )

    fullName = models.CharField(
        max_length=200,
        default="",
        null=False,
        blank=True,
    )
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    products = models.ManyToManyField(
        Product,
        related_name="orders",
        through="OrdersCountProducts",
    )

    def save(self, *args, **kwargs):
        if self.pk:
            order = Order.objects.get(pk=self.pk)
            pro = OrdersCountProducts.objects.filter(order=order)

            delivery_price = 0
            # delivery = delivery_price if self.totalCost else 0

            if self.totalCost:
                if self.deliveryType.deliveryType == "express":
                    delivery_price = 500
                else:
                    if self.totalCost < 2000:
                        delivery_price = 200
            else:
                delivery_price = 0
            # if self.deliveryType is not None:
            #     if self.deliveryType.deliveryType == 'express':
            #         print('express')
            #         delivery_price = 500
            #     else:
            #         print('ordinary')
            #         if self.totalCost < 2000:
            #             delivery_price = 200

            new_total = (
                sum([index.product.get_curr_price() * index.count for index in pro])
                + delivery_price
            )
            self.totalCost = new_total
        super().save()

        # if self.totalCost:
        #     self.totalCost += delivery_price
        # else:
        #     new_total = sum([index.product.price * index.count for index in pro])
        #     self.totalCost = new_total


class OrdersCountProducts(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        # related_name='product',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="product",
    )
    count = models.PositiveIntegerField(
        null=True,
    )
