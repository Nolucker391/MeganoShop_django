from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count

from .models import Product
from .serializers import ProductSerializer

class ProductsList(APIView):
    def get(self, request: Request) -> Response:
        products_list = Product.objects.all()
        serializer = ProductSerializer(products_list, many=True)
        pum = {
          "items": [
            {
              "id": 123,
              "category": 55,
              "price": 500.67,
              "count": 12,
              "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
              "title": "video card",
              "description": "description of the product",
              "freeDelivery": True,
              "images": [
                {
                  "src": "/Users/skillbox/PycharmProjects/MeganoShop_django/images/admin.jpeg",
                  "alt": "Image alt string"
                }
              ],
              "tags": [
                {
                  "id": 12,
                  "name": "Gaming"
                }
              ],
              "reviews": 5,
              "rating": 4.6
            }
          ],
          "currentPage": 5,
          "lastPage": 10
        }
        if len(products_list):
            return Response(data=pum, status=200)
        return Response(status=400)