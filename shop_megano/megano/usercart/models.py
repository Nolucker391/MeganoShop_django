from django.db import models
from django.conf import settings
from product.models import Product

class UserCart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='BasketItem')

class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='items')
    count = models.PositiveIntegerField(default=1)