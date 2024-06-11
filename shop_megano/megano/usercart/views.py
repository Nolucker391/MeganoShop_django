from django.shortcuts import render
from rest_framework.request import Request
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
    """
    Функция для сериализации данных.
    :param cart:
    :return:
    """
    if isinstance(cart, dict):

        cart_object = cart

        serializer = BasketSerializer(
            cart_object,
            many=True,
        )

        return Response(serializer.data)

    else:
        cart_object = cart.cart

        serializer = BasketSerializer(
            cart_object,
            many=True,
        )

        return Response(serializer.data)



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
            return products_in_basket(cart)

        else:
            user_basket, _ = UserCart.objects.get_or_create(user=self.request.user)
            data = request.data
            format_dict = {}

            print(data['id'], data['count'])
            product = Product.objects.get(pk=int(data['id']))

            existing_basket_item = BasketItem.objects.filter(product=product, basket=user_basket)

            if existing_basket_item.exists():
                for basket_item in existing_basket_item:
                    basket_item.count += data['count']
                    basket_item.save()
            else:
                basket_item = BasketItem(product=product, count=data['count'], basket=user_basket)

                basket_item.save()

            format_dict[f'{data['id']}'] = {
                    f'count': data['count'],
                }
            return products_in_basket(format_dict)
            #basket = BasketItem.objects.filter(basket=user_basket)

            # format_dict = {}
            #
            # for items in basket:
            #     format_dict[f'{items.product_id}'] = {
            #         f'count': items.count,
            #     }


            # if product_pk_exist.exists():
            #     for basket_item in product_pk_exist:
            #         basket_item.count += count
            #         basket_item.save()
            #     return products_in_basket(cart)
            # else:
            #     for product_pk, values in cart.cart.items():
            #         product = Product.objects.get(pk=int(product_pk))
            #         basket_item = BasketItem(product=product, count=values['count'], basket=user_basket)
            #
            #         basket_item.save()
            #
            #     return products_in_basket(cart)
    def get(self, request: Request):
        """
        Отображение товаров в корзине.
        :param args:
        :param kwargs:
        :return:
        """
        if not self.request.user.is_authenticated:
            cart = UserBasket(self.request)

            return products_in_basket(cart)
        else:
            user_cart = UserCart.objects.get(user=self.request.user)
            user_basket = BasketItem.objects.filter(basket=user_cart)

            format_dict = {}

            for items in user_basket.all():

                format_dict[f'{items.product_id}'] = {
                        f'count': items.count,

                }

            return products_in_basket(format_dict)
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

            return products_in_basket(cart)
        else:
            user_cart = UserCart.objects.get(user=self.request.user)
            product = get_object_or_404(
                Product,
                id=self.request.data.get('id'),
            )
            count = self.request.data.get('count')

            user_basket_items = BasketItem.objects.filter(basket=user_cart, product=product, count=count)
            user_basket_items.delete()

            format_dict = {}
            for items in user_basket_items.all():
                format_dict[f'{items.product_id}'] = {
                    f'count': items.count,
                }

            return products_in_basket(format_dict)
            #return Response(status=200)
