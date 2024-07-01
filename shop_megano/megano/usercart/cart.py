from decimal import Decimal
from django.conf import settings
from rest_framework.request import Request

from product.models import Product


class UserBasket(object):
    """
    Класс объект корзины.
    """

    def __init__(self, request: Request):
        """
        Инициализация корзины.
        :param request:
        """

        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, count=1):
        """
        Добавление товара и количество в корзину.
        :param product:
        :param count:
        :return:
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {"count": count, "price": str(product.price)}
        else:
            self.cart[product_id]["count"] += count
        self.save()

    def save(self):
        """
        Сохранить корзину.

        """

        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, count):
        """
        Удаление товара или изменение его количества в корзине.
        :param product:
        :return:
        """
        product_id = str(product.id)

        if product_id in self.cart:
            if count == 1 and self.cart[product_id]["count"] > 1:
                self.cart[product_id]["count"] -= int(count)
            else:
                del self.cart[product_id]
            self.save()

            # if self.cart[product_id]['count'] > 1:
            #     self.cart[product_id]['count'] -= 1
            # elif self.cart[product_id]['count'] == 2:
            #     #del self.cart[product_id]
            #     self.cart.pop(product_id)
            # self.save()

    def __len__(self):
        """
        Функция для подсчета всех товаров в корзине.
        """
        print(self.__dict__)
        return sum(prod["count"] for prod in self.cart.values())

    def clear(self):
        """
        Функция для очистка корзины.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def total_summ(self):
        """
        Функция для отображении общей суммы товаров в заказе.
        """
        return sum(
            [
                Decimal(
                    prod["price"],
                )
                * prod["count"]
                for prod in self.cart.values()
            ],
        )

    def to_rep(self):
        l = []
        for product_pk, val in self.cart.items():
            l.append(
                {"product": Product.objects.get(pk=product_pk), "count": val["count"]}
            )
            # l.append(a)
        return l
