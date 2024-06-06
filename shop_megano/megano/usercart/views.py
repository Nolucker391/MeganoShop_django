from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from usercart.cart import UserBasket
from usercart.serializers import BasketSerializer
from product.models import Product
from usercart.models import UserCart

from rest_framework.generics import get_object_or_404

def products_in_basket(cart: UserBasket):
    products_id = [product_id for product_id in cart.cart.keys()]
    products = Product.objects.filter(pk__in=products_id)

    serializer = BasketSerializer(
        products,
        many=True,
        context=cart.cart,
    )

    return Response(serializer.data, status=200)

class UserBasketView(APIView):
    def post(self, *args, **kwargs):
        """
        Добавление товара в корзину.
        :param args:
        :param kwargs:
        :return:
        """
        cart = UserBasket(self.request)
        product = get_object_or_404(
            Product,
            id=self.request.data.get('id'),
        )
        count = self.request.data.get('count')
        cart.add(
            product=product,
            count=count,
        )

        return products_in_basket(cart)

    def delete(self, *args, **kwargs):
        """
        Удаление товара из корзины.
        :param args:
        :param kwargs:
        :return:
        """
        cart = UserBasket(self.request)
        product = get_object_or_404(
            Product,
            id=self.request.data.get('id'),
        )
        count = self.request.data.get('count', False)

        cart.remove(product, count)
        return products_in_basket(cart)

    def get(self, *args, **kwargs):
        """
        Отображение товара в корзине.
        :param args:
        :param kwargs:
        :return:
        """

        user = UserCart.objects.filter(user_id=self.request.user.id)

        if user:
            products_in_basket(UserBasket(user))
        cart = UserBasket(self.request)

        return products_in_basket(cart)
