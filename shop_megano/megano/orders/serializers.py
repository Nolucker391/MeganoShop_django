import datetime

from rest_framework import serializers
from .models import Order
from product.serializers import ProductSerializer


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

    products = ProductSerializer(
        many=True,
        required=True,
    )

    # fullName = serializers.SerializerMethodField()
    # email = serializers.SerializerMethodField()
    # phone = serializers.SerializerMethodField()
    #
    # def get_fullName(self, instance):
    #     return instance.user.userprofile.fullName
    #
    # def get_email(self, instance):
    #     return instance.user.userprofile.email
    #
    # def get_phone(self, instance):
    #     return instance.user.userprofile.phone

    def to_representation(self, instance):
        data = super().to_representation(instance)

        date = datetime.datetime.fromisoformat(data['createdAt'])
        data['createdAt'] = date.strftime('%Y-%m-%d %H:%M')

        return data
