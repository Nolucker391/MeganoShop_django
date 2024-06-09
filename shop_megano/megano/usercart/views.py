from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.conf import settings

from usercart.cart import UserBasket

from usercart.serializers import BasketSerializer

from product.models import Product
from usercart.models import UserCart, BasketItem

from rest_framework.generics import get_object_or_404


def products_in_basket(cart: UserBasket):
    cart_object = cart.cart

    serializer = BasketSerializer(
        cart_object,
        many=True,
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

        if not self.request.user.is_authenticated:
            return products_in_basket(cart)

        else:
            user_basket, _ = UserCart.objects.get_or_create(user=self.request.user)

            for product_pk, values in cart.cart.items():
                product = Product.objects.get(pk=int(product_pk))
                basket_item = BasketItem(product=product, count=values['count'], basket=user_basket)

                basket_item.save()

            return products_in_basket(cart)

