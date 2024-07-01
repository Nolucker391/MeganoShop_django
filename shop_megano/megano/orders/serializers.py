import datetime

from rest_framework import serializers
from .models import Order, OrdersCountProducts, OrdersDeliveryType
from product.serializers import ProductSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = OrdersCountProducts
        fields = (
            "product",
            "count",
        )

    def to_representation(self, instance):
        product_serializer = ProductSerializer(instance.get("product"))
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
            "id",
            "user",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
            "fullName",
            "email",
            "phone",
            "createdAt",
        )

    def to_representation(self, instance):
        format_dict = [
            {"product": i.product, "count": i.count}
            for i in OrdersCountProducts.objects.filter(order__pk=instance.pk)
        ]
        order_product_serializer = OrderProductSerializer(format_dict, many=True)

        data = super().to_representation(instance)
        data["products"] = order_product_serializer.data
        date = datetime.datetime.fromisoformat(data["createdAt"])
        data["createdAt"] = date.strftime("%Y-%m-%d %H:%M")
        # data['deliveryType'] = OrdersDeliveryType.objects.get(id=data['deliveryType']).deliveryType

        if data["deliveryType"] is None:
            data["deliveryType"] = "ordinary"
        else:
            data["deliveryType"] = OrdersDeliveryType.objects.get(
                id=int(data["deliveryType"])
            ).deliveryType

        return data

        # data = super().to_representation(instance)
        # date = datetime.datetime.fromisoformat(data['createdAt'])
        # data['createdAt'] = date.strftime('%Y-%m-%d %H:%M')
        #

        #
        # return data


class PaymentSerializer(serializers.Serializer):
    """
    Сериализатор для валидации данных, оплачиваемой картой.
    """

    card_number = serializers.CharField(max_length=20)
    month = serializers.IntegerField(min_value=1, max_value=12)
    year = serializers.IntegerField(min_value=15, max_value=50)
    cvv_code = serializers.CharField(max_length=3)
    fullname = serializers.CharField(max_length=50)

    def validate_card_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Номер карты должен состоять только из цифр."
            )
        if len(value) < 16 or len(value) > 20:
            raise serializers.ValidationError(
                "Номер карты должен иметь длину от 16 до 20 символов."
            )

        return value

    def validate_month(self, value):
        if not (1 <= value <= 12):
            raise serializers.ValidationError("Месяц карты должен быть двухзначным.")
        return value

    def validate_year(self, value):
        if not (15 <= value <= 50):
            raise serializers.ValidationError("Год должен быть двузначным числом (от 15 до 50).")
        return value

    def validate_cvv_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("CVV должен состоять только из цифр.")
        if len(value) != 3:
            raise serializers.ValidationError(
                "CVV-код должен состоять ровно из 3 цифр."
            )

        return value

    def validate_fullname(self, value):
        # pattern = r'^[a-zA-Z\s\]*$'
        # if not re.match(pattern, value):
        # if not value.isalpha():
        # pattern = r'^[a-zA-Z\s]*$'
        # if not re.match(pattern, value):
        words = value.split()

        for word in words:
            if not word.isalpha():
                raise serializers.ValidationError(
                    "Имя на карте должно содержать только буквы."
                )
        return value
