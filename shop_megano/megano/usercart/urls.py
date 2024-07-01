from django.urls import path

from .views import UserBasketView

urlpatterns = [
    path("api/basket", UserBasketView.as_view(), name="user-basket"),
]
