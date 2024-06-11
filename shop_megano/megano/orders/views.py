from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from usercart.cart import UserBasket
from .models import Order, OrdersCountProducts
from product.models import Product
from .serializers import OrdersSerializer

from usercart.models import UserCart
from usercart.models import BasketItem


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
        data = request.data
        products_in_order = [
            (obj['id'], obj['count'], obj['price']) for obj in data
        ]
        products_pk = [product_id[0] for product_id in products_in_order]
        products = Product.objects.filter(id__in=products_pk)
        order = Order.objects.create(
            user=request.user,
            totalCost=UserBasket(request).total_summ(),
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
        products_in_order = data['products']

        for product in products_in_order:
            basket = BasketItem.objects.filter(product_id=product['id'], basket=usercart)
            for item in basket:
                product['count'] = item.count

        return Response(data)

    def post(self, request: Request, pk) -> Response:
        data = request.data
        order = Order.objects.get(pk=pk)
        order.fullName = data['fullName']
        order.phone = data['phone']
        order.email = data['email']
        order.deliveryType = data['deliveryType']
        order.city = data['city']
        order.address = data['address']
        order.paymentType = data['paymentType']
        order.status = 'awaiting'

        for product in data['products']:
            OrdersCountProducts.objects.get_or_create(
                order_id=order.pk,
                product_id=product['id'],
                count=product['count'],
            )
        # order.save()

        if data['deliveryType'] is not None:
            if data['deliveryType'] == 'express':
                order.totalCost += 500
        else:
            if order.totalCost < 2000:
                order.totalCost += 200
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
        usercart = UserCart.objects.get(user=request.user)
        usercart.clear()

        return Response(request.data, status=200)


