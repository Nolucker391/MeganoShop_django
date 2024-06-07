from rest_framework import serializers

from product.models import Product
from usercart.models import BasketItem
from product.serializers import ProductSerializer

class BasketSerializer(serializers.ModelSerializer):
    """
    Сериализация продуктов в корзине
    """
    class Meta:
        model = BasketItem
        fields = (
            'id',
            'product',
            'basket',
            'count'
        )
    product = ProductSerializer()
    count = serializers.SerializerMethodField()

    def get_object(self, object):
        pass



