from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Order, OrdersCountProducts, OrdersDeliveryType
from usercart.models import UserCart, BasketItem
from product.models import Product

from .serializers import OrdersSerializer, PaymentSerializer


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
                (obj["id"], obj["count"], obj["price"]) for obj in data
            ]
            products = Product.objects.filter(
                id__in=[product_id[0] for product_id in products_in_order]
            )

            order = Order.objects.create(
                user=request.user,
            )

            for index in range(len(products_in_order)):
                pk, count, price = products_in_order[index]
                product = products[index]

                print(product.get_curr_price())
                OrdersCountProducts.objects.create(
                    order=order, product=product, count=count
                )

            order.save()

            UserCart.objects.get(user=request.user).delete()

            return Response({"orderId": order.pk})

        else:
            # return HttpResponseRedirect(redirect_to="/sign-in/")
            # return redirect("http://127.0.0.1:8000/sign-in/")
            return Response("Bad request", status=500)


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
        order.fullName = data["fullName"]
        order.phone = data["phone"]
        order.email = data["email"]
        order.city = data["city"]
        order.address = data["address"]
        order.paymentType = data["paymentType"]
        order.status = Order.CHOICES[0][1]

        if data["deliveryType"] is None:
            order_delivery, _ = OrdersDeliveryType.objects.get_or_create(
                deliveryType="ordinary"
            )

        else:
            order_delivery, _ = OrdersDeliveryType.objects.get_or_create(
                deliveryType=data["deliveryType"]
            )

        order.deliveryType = order_delivery

        order.save()

        return Response(data, status=status.HTTP_201_CREATED)


class Payment(APIView):
    """
    Класс для оплаты заказа.
    """

    def post(self, request: Request, pk):
        data = {
            "card_number": f"{request.data.get('number')}",
            "month": f"{request.data.get('month')}",
            "year": f"{request.data.get('year')}",
            "cvv_code": f"{request.data.get('code')}",
            "fullname": f"{request.data.get('name')}",
        }
        serializer = PaymentSerializer(data=data)

        if serializer.is_valid():
            order = Order.objects.get(pk=pk)
            order.status = "accepted"
            order.save()

            return Response(request.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)
