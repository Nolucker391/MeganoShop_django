from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Order, OrdersCountProducts, OrdersDeliveryType
from product.models import Product
from .serializers import OrdersSerializer

from usercart.models import UserCart, BasketItem


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
        data = request.data #прилетает запрос оформить заказ, продукта'ов'

        products_in_order = [
            (obj['id'], obj['count'], obj['price']) for obj in data
        ] # берем нужные параметры с запроса

        products_pk = [product_id[0] for product_id in products_in_order] # берем id продуктов

        products = Product.objects.filter(id__in=products_pk) #фильтруем по pk продукты
        sum = 0
        for prod in products:
            sum += prod.price

        order = Order.objects.create(
            user=request.user,
            totalCost=sum,
        )
        order.products.set(products)
        order.save()

        return Response({
            'orderId': order.pk
        })

class OrderDetails(APIView):
    """
    Класс для отображения деталей заказа.
    """

    def get(self, request: Request, pk):

        data = Order.objects.get(pk=pk)

        serializer = OrdersSerializer(data)
        usercart = UserCart.objects.get(user=request.user)
        data = serializer.data
        product_in_request_order = data['products']

        for item in product_in_request_order:
            basket_product = BasketItem.objects.filter(basket=usercart, product__pk=int(item['id']))
            for value in basket_product:
                item['count'] = value.count

        return Response(data)

    def post(self, request: Request, pk) -> Response:
        """
        Функция для оформления заказа.
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
        order.status = 'awaiting'
        # a = OrdersDeliveryType(deliveryType=data['deliveryType'])
        # a.save() deliveryType='ordinary
        # order.deliveryType = a

        if data['deliveryType'] is None:
            order_delivery = OrdersDeliveryType.objects.get_or_create(deliveryType='ordinary')
            order_delivery.save()
            order.deliveryType = order_delivery
        else:
            order_delivery = OrdersDeliveryType.objects.get_or_create(deliveryType=data['deliveryType'])
            order_delivery.save()
            order.deliveryType = order_delivery



        for product in data['products']:
            OrdersCountProducts.objects.get_or_create(
                order_id=order.pk,
                product_id=product['id'],
                count=product['count'],
            )
        # # order.save()
        if data['deliveryType'] is not None:
            if data['deliveryType'] == 'express':
                order.totalCost += 500
        else:
            if order.totalCost < 2000:
                order.totalCost += 200
        order.save()

        UserCart.objects.get(user=request.user).delete()

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
        usercart = UserCart.objects.get(user=request.user)
        usercart.clear()

        return Response(request.data, status=200)


