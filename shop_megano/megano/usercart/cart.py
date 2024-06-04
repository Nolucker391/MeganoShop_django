from decimal import Decimal
from django.conf import settings
from rest_framework.request import Request

from shop_megano.megano.product.models import Product

class UserBasket(object):
    """
    Класс объект корзины.
    """

    def __init__(self, request: Request):
        """
        Инициализация корзины.
        :param request:
        """
        pass