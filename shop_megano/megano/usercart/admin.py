from django.contrib import admin
from .models import UserCart, BasketItem

# Register your models here.
admin.site.register(UserCart)
admin.site.register(BasketItem)
