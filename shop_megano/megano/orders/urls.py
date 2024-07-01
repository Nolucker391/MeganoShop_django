from django.urls import path

from .views import OrdersList, OrderDetails, Payment

urlpatterns = [
    path("api/orders", OrdersList.as_view(), name="orders_list"),
    path("api/order/<int:pk>", OrderDetails.as_view(), name="order_details"),
    path("api/payment/<int:pk>", Payment.as_view(), name="payment"),
]
