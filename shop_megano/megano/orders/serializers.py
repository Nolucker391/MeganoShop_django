import datetime

from rest_framework import serializers
from .models import Order, OrdersCountProducts, OrdersDeliveryType
from product.serializers import ProductSerializer

from product.models import Product


class OrderProductSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = OrdersCountProducts
        fields = (
            'product',
            'count',
        )

    def to_representation(self, instance):
        product_serializer = ProductSerializer(instance.get('product'))
        prod_copy = product_serializer.data
        prod_copy["count"] = instance.get("count")
        return prod_copy
        # product_serializer.data.update("count", instance.get("count"))
        # print(product_serializer.data)
        # return product_serializer.data


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
            'products',
            'fullName',
            'email',
            'phone',
            'createdAt',
        )

    def to_representation(self, instance):
        format_dict = [{"product": i.product, "count": i.count} for i in
                       OrdersCountProducts.objects.filter(order__pk=instance.pk)]
        order_product_serializer = OrderProductSerializer(format_dict, many=True)

        data = super().to_representation(instance)
        data['products'] = order_product_serializer.data
        date = datetime.datetime.fromisoformat(data['createdAt'])
        data['createdAt'] = date.strftime('%Y-%m-%d %H:%M')
        # data['deliveryType'] = OrdersDeliveryType.objects.get(id=data['deliveryType']).deliveryType

        if data['deliveryType'] is None:
            data['deliveryType'] = 'ordinary'
        else:
            data['deliveryType'] = OrdersDeliveryType.objects.get(id=int(data['deliveryType'])).deliveryType

        return data

        # data = super().to_representation(instance)
        # date = datetime.datetime.fromisoformat(data['createdAt'])
        # data['createdAt'] = date.strftime('%Y-%m-%d %H:%M')
        #

        #
        # return data
