from django.contrib import admin

# from .models import Order, OrdersCountProducts, OrdersDeliveryType


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = 'pk', 'user', 'createdAt', 'paymentType', 'city', 'address', 'fullName', 'status', 'phone', 'email'
#     list_display_links = 'pk', 'status'
#     ordering = 'pk',
#
#
# @admin.register(OrdersCountProducts)
# class OrderCount(admin.ModelAdmin):
#     list_display = 'pk', 'product', 'count'
#     list_display_links = 'pk', 'product'
#     ordering = 'pk',
#
#
# @admin.register(OrdersDeliveryType)
# class OrderDelivery(admin.ModelAdmin):
#     list_display = 'pk', 'deliveryType', 'totalCost'
#     list_display_links = 'pk', 'deliveryType'
#     ordering = 'pk',
