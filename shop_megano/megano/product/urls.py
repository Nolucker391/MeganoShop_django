from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    ProductsList,
    ProductDetails
)

urlpatterns = [
    path('api/catalog/', ProductsList.as_view(), name='products-list'),
    path('api/product/<int:pk>/', ProductDetails.as_view(), name='product-details')
]
