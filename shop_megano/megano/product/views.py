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
        serializer = ProductSerializer(data=products_list)

        if serializer.is_valid():
            return Response(data=serializer.data, status=200)
        return Response(status=400)