from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.db.models import QuerySet
# QuerySet().update()

from django.conf import settings

from usercart.cart import UserBasket

from usercart.serializers import BasketSerializer

from product.models import Product
from usercart.models import UserCart, BasketItem

from rest_framework.generics import get_object_or_404


def products_in_basket(cart: UserBasket):
    """
    Функция для сериализации данных.
    :param cart:
    :return:
    """

    cart_object = cart

    serializer = BasketSerializer(
        cart_object,
        many=True,
    )
    return Response(serializer.data)
    # if isinstance(cart, dict):
    #
    #     cart_object = cart
    #
    #     serializer = BasketSerializer(
    #         cart_object,
    #         many=True,
    #     )
    #
    #     return Response(serializer.data)
    #
    # else:
    #     cart_object = cart.cart
    #
    #     serializer = BasketSerializer(
    #         cart_object,
    #         many=True,
    #     )
    #
    #     return Response(serializer.data)


class UserBasketView(APIView):
    def post(self, request: Request):
        """
        Добавление товара в корзину.
        :param args:
        :param kwargs:
        :return:
        """

        if not self.request.user.is_authenticated:
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
            return products_in_basket(cart.to_rep())
            # return products_in_basket(cart)

        else:
            user_basket, _ = UserCart.objects.get_or_create(user=self.request.user) #получаем юзер бакет
            data = request.data # получаем данные из запроса
            product = Product.objects.get(pk=int(data['id'])) # берем продукт

            basket_list = BasketItem.objects.filter(basket=user_basket)

            # print(basket_list)
            # print(basket_list.filter(product__pk=product.pk))

            if product in (e.product for e in basket_list.filter(product=product)):
                for item in basket_list:
                    if item.product.pk == data['id']:
                        item.count += data['count']
                        item.save()
            else:
                basket_item = BasketItem(product=product, count=data['count'], basket=user_basket)
                basket_item.save()

            return products_in_basket(basket_list)

    def get(self, request: Request):
        """
        Отображение товаров в корзине.
        :param args:
        :param kwargs:
        :return:
        """
        if not self.request.user.is_authenticated:
            cart = UserBasket(self.request)

            #{'session': <django.contrib.sessions.backends.db.SessionStore object at 0x10f5d9220>, 'cart': {'8': {'count': 2, 'price': '3347.00'}, '7': {'count': 1, 'price': '2121.22'}}}
            #[{'product': <Product: Apple iMac 2021>, 'count': 2}, {'product': <Product: Apple iMac>, 'count': 1}]

            #return products_in_basket(cart.to_rep())
            return products_in_basket(cart.to_rep())

        else:
            try:
                user_cart = UserCart.objects.get(user=self.request.user)
                user_basket = BasketItem.objects.filter(basket=user_cart)
            except ObjectDoesNotExist:
                return Response('Not exist', status=500)
            basket_list = []

            for item in user_basket:
                # print(item)
                basket_list.append(item)

            return products_in_basket(basket_list)
    def delete(self, *args, **kwargs):
        """
        Удаление товаров из корзины.
        :param args:
        :param kwargs:
        :return:
        """

        if not self.request.user.is_authenticated:
            cart = UserBasket(self.request)

            product = get_object_or_404(
                Product,
                id=self.request.data.get('id'),
            )
            count = self.request.data.get('count')

            cart.remove(product, count=count)

            return products_in_basket(cart.to_rep())
        else:
            user_cart = UserCart.objects.get(user=self.request.user)
            count = self.request.data.get('count')
            basket_list = BasketItem.objects.filter(basket=user_cart)

            # if product in (e.product for e in basket_list.filter(product=product)):
            basket_item = BasketItem.objects.get(basket=user_cart, product__pk=int(self.request.data.get('id')))

            basket_item.count = max(basket_item.count - count, 0)
            if basket_item.count == 0:
                basket_item.delete()
            else:
                basket_item.save()

            return products_in_basket(basket_list)
