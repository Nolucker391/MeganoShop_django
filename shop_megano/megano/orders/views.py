import json

from django.contrib.auth import login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Order, OrdersCountProducts, OrdersDeliveryType
from product.models import Product
from .serializers import OrdersSerializer

from usercart.models import UserCart, BasketItem

from product.models import Sale


class OrdersList(APIView):
    """
    Класс для отображения историй заказов.
    """

    def get(self, request: Request):
        """
        Функция для отображения списка заказов.
        :param request:
        :return:
        """
        orders = Order.objects.filter(user_id=request.user.pk)
        serialized = OrdersSerializer(orders, many=True)

        return Response(serialized.data)

    def post(self, request: Request, *args, **kwargs):
        """
        Функция для оформления заказа.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.user.is_authenticated:
            data = request.data
            products_in_order = [
                (obj['id'], obj['count'], obj['price']) for obj in data
            ]
            products = Product.objects.filter(id__in=[product_id[0] for product_id in products_in_order])

            order = Order.objects.create(
                user=request.user,
            )

            for index in range(len(products_in_order)):
                pk, count, price = products_in_order[index]
                product = products[index]
                print(Sale.objects.get(product=product).salePrice)
                print(product.sales)
                OrdersCountProducts.objects.create(order=order, product=product, count=count)

            order.save()

            UserCart.objects.get(user=request.user).delete()

            return Response({
                'orderId': order.pk
            })

        else:
            return Response('Bad request', status=500)


class OrderDetails(APIView):
    """
    Класс для отображения деталей заказа.
    """

    def get(self, request: Request, pk):
        data = Order.objects.get(pk=pk)
        # print(data.products)
        # print(OrdersCountProducts.objects.get(order=data).product)
        serializer = OrdersSerializer(data)
        return Response(serializer.data)

    def post(self, request: Request, pk) -> Response:
        """
        Функция для оформления деталей заказа.
        :param request:
        :param pk:
        :return:
        """
        data = request.data
        order = Order.objects.get(pk=pk)
        order.fullName = data['fullName']
        order.phone = data['phone']
        order.email = data['email']
        order.city = data['city']
        order.address = data['address']
        order.paymentType = data['paymentType']
        order.status = Order.CHOICES[0][1]

        if data['deliveryType'] is None:
            order_delivery, _ = OrdersDeliveryType.objects.get_or_create(deliveryType='ordinary')

        else:
            order_delivery, _ = OrdersDeliveryType.objects.get_or_create(deliveryType=data['deliveryType'])

        order.deliveryType = order_delivery

        order.save()

        return Response(data, status=status.HTTP_201_CREATED)


class Payment(APIView):
    """
    Класс для оплаты заказа.
    """

    def post(self, request: Request, pk):
        order = Order.objects.get(pk=pk)
        print(order.__dict__)
        order.status = 'accepted'
        order.save()
        # usercart = UserCart.objects.get(user=request.user)
        # usercart.delete()

        return Response(request.data, status=200)
