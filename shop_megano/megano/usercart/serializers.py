from rest_framework import serializers

from product.models import Product
from usercart.models import BasketItem, UserCart
from product.serializers import ProductSerializer

class ProductBasketSerializer(serializers.ModelSerializer):
    """
        Сериализация продуктов в корзине
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
        if self.user:
            return BasketItem.objects.filter(product__pk=instance.pk,
                                             basket__pk=UserCart.objects.get(user=self.curr_user)).count
        else:
            return self.context.get(str(instance.pk)).get('count')

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
    class Meta:
        model = BasketItem
        fields = (
            'product',#'cart': {'14':
            'count' # {'count': 1,
        )


    def to_representation(self, instance):
        # instance = product_id
        product = Product.objects.get(pk=instance)
        data = ProductSerializer(product)
        serializer = ProductBasketSerializer(data)

        return instance

