import datetime

from rest_framework import serializers
from.models import Product, Tag, Review, ProductImage


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )

class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            'author',
            'email',
            'text',
            'rate',
            'date',
            'product',
        )

    def get_date(self, instance):
        date = instance.date + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(
            date,
            format='%d.%m.%Y %H:%M',
        )

class ProductSerializer(serializers.ModelSerializer):
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
            'images',
            'tags',
            'reviews',
            'rating',
        )

    images = serializers.SerializerMethodField()

    tags = TagSerializer(
        many=True,
        required=False
    )

    reviews = ReviewSerializer(
        many=True,
        required=False
    )

    price = serializers.SerializerMethodField()

    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)
        data.update(images=self.get_images(instance))
        return data

    def get_price(self, instance):
        sale_price = instance.sales.first()
        if sale_price:
            instance.price = sale_price.salePrice

        return instance.price

    def get_images(self, instance):
        images = []
        for image in instance.images.all():
            images.append(
                {'src': f'/media/{image.image}',
                 'alt': image.name},
            )
        return images


