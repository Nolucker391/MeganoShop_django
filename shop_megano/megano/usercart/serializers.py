from rest_framework import serializers

from product.models import Product
from usercart.models import BasketItem, UserCart
from product.serializers import ProductSerializer

class ProductBasketSerializer(serializers.ModelSerializer):
    """
        Сериализация продуктов с корзины.
    """

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'fullDescription',
            'freeDelivery',
            'specifications',
            'tags',
            'images',
            'reviews'
        )

    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_count(self, instance):
        return self.context.get('count')
        #return self.context.get(str(instance.pk)).get('count')

    def get_price(self, instance):
        sale_price = instance.sales.first()
        if sale_price:
            instance.price = sale_price.salePrice

        return instance.price

    def get_images(self, instance):
        images = []
        for image in instance.images.all():
            images.append(
                {'src': f'/media/{image.__str__()}',
                 'alt': image.name},
            )
        return images


class BasketSerializer(serializers.ModelSerializer):
    """
    Сериализатор корзины пользователя.
    """

    class Meta:
        model = BasketItem
        fields = (
            'product',#'cart': {'14':
            'count' # {'count': 1,
        )


    def to_representation(self, instance):
        if isinstance(instance, dict):
            product = instance["product"]
            count = instance["count"]
        else:
            product = instance.product
            count = instance.count
        product_basket_serializer = ProductBasketSerializer(product, context={'count': count})

        return product_basket_serializer.data




# # instance = product_id
#product_serializer = ProductSerializer(product)

# data = ProductSerializer(product)
# serializer = ProductBasketSerializer(data)
#
#return instance