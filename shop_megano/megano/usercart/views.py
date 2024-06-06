from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from cart.cart import UserBasket


class UserBasketView(APIView):
    def get(self, *args, **kwargs):
        cart = UserBasket(self.request)

        return cart