from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    ProductsList
)

urlpatterns = [
    path('api/catalog/', ProductsList.as_view(), name='products-list'),
]
