from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from usercart.cart import UserBasket

from usercart.serializers import BasketSerializer, GetBasketSerializer

from product.models import Product
from usercart.models import UserCart, BasketItem

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

        # user = UserCart.objects.filter(user_id=self.request.user.id)

        # if user:
        #     products_in_basket(UserBasket(user))
        # cart = UserBasket(self.request)


        # cart = UserBasket(self.request)
        # products = Product.objects.filter()
        # products = Product.objects.get(pk=cart.products.pk)
        #return products_in_basket(cart)

        # cart = UserCart.objects.get(user__pk=self.request.user.pk)
        # products = BasketItem.objects.filter(basket__pk=cart.pk)

        # serializer = GetBasketSerializer(products, many=True)
        #
        # return Response(serializer.data)

        cart = UserCart.objects.get(user__pk=self.request.user.pk)
        products = BasketItem.objects.filter(basket__pk=cart.pk)
        print(products)
        return Response(status=200)