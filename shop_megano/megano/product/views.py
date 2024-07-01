import datetime

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import ListAPIView

from django.db.models import Count

from .models import Product, CategoryProduct, Review, Tag, Sale
from .serializers import (
    ProductSerializer,
    ReviewSerializer,
    TagSerializer,
    SalesSerializer,
    CategorySerializer,
)
from .paginations import SetPagePagination, SetSalesPagePagination


class ProductsListView(ListAPIView):
    """
    Класс для отображения продуктов на странице каталога.
    """

    queryset = Product.objects.all()
    pagination_class = SetPagePagination
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):

        filter_dict = dict()
        sort_list = list()
        filter_dict["count__gt"] = 0

        name = request.query_params.get("filter[name]") or None
        if name:
            filter_dict["title__iregex"] = name

        avail = request.query_params.get("filter[available]", None)
        if avail is not None:
            filter_dict["archived"] = False if avail == "true" else True
        else:
            sort_list.append("archived")

        deliver = request.query_params.get("filter[freeDelivery]", None)
        if deliver is not None:
            if deliver == "true":
                filter_dict["freeDelivery"] = True
        else:
            sort_list.append("-freeDelivery")

        tags = request.query_params.getlist("tags[]") or None
        if tags:
            filter_dict["tags__in"] = tags

        min_price = float(request.query_params.get("filter[minPrice]") or 0)
        max_price = float(request.query_params.get("filter[maxPrice]") or 50000)
        filter_dict["price__range"] = (min_price, max_price)

        # category = request.META['HTTP_REFERER'].split('/')[4] or None
        category = request.query_params.get("category", None)

        sort = request.GET.get("sort")

        if category:
            if category.startswith("?filter="):
                if name is None:
                    name = category[8:]
            else:
                parent_category = CategoryProduct.objects.filter(
                    parent_id=category,
                )
                all_categories = [subcat.pk for subcat in parent_category]
                all_categories.append(int(category))
                filter_dict["category_id__in"] = all_categories

        # {'count__gt': 0, 'archived': True, 'price__range': (0.0, 50000.0)}
        products_list = Product.objects.filter(**filter_dict)

        if request.GET.get("sortType") == "inc":
            sortType = "-"
        else:
            sortType = ""

        if sort == "reviews":
            products_list = products_list.annotate(
                count_reviews=Count("reviews"),
            ).order_by(f"{sortType}count_reviews")
        else:
            products_list = products_list.order_by(
                f"{sortType}{sort}",
            )
        products_list = products_list.prefetch_related(
            "images",
            "tags",
        )
        queryset = products_list

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetails(APIView):
    """
    Класс для отображения деталей продукто.
    """

    def get(self, request: Request, pk: int):
        # print(request.__dict__)
        products = Product.objects.get(pk=pk)
        serializer = ProductSerializer(products, many=False)

        return Response(serializer.data)


class PopularProductsList(APIView):
    """
    Класс для отображения популярных продуктов на главной странице.
    """

    def get(self, request: Request):
        popular_product_to_reviews = (
            Product.objects.filter(
                archived=False,
            )
            .annotate(
                count_reviews=Count("reviews"),
            )
            .order_by("-count_reviews")[:4]
        )

        serializer = ProductSerializer(popular_product_to_reviews, many=True)

        return Response(serializer.data)


class LimitedEditionList(APIView):
    """
    Класс для отображения ограниченных продуктов на главной странице.
    """

    def get(self, request: Request):
        products = Product.objects.filter(limited_edition=True)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


class ReviewCreateProduct(APIView, CreateModelMixin):
    """
    Класc для создания отзыва на продукт.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk):
        product = get_object_or_404(
            Product,
            pk=pk,
        )

        Review.objects.create(
            author=request.data["author"],
            email=request.data["email"],
            text=request.data["text"],
            rate=request.data["rate"],
            date=datetime.datetime.now,
            product_id=product.pk,
        )
        review_rate_update = Review.objects.filter(
            product_id=product.pk,
        )
        review_count = len(review_rate_update)
        summ = sum(review.rate for review in review_rate_update)
        new_rating = summ / review_count

        product.rating = new_rating
        product.save()

        return Response(request.data)


class TagsList(APIView):
    """
    Класс для отображения тэгов, часто-используемых продуктов.
    """

    def get(self, request: Request) -> Response:
        tags = Tag.objects.all()
        serialized = TagSerializer(
            tags,
            many=True,
        )
        return Response(serialized.data)


class SalesList(ListAPIView):
    """
    Класс для отображения списка продуктов для распродажи.
    """

    queryset = Sale.objects.all()
    pagination_class = SetSalesPagePagination
    serializer_class = SalesSerializer

    def list(self, request, *args, **kwargs):
        # queryset = Product.objects.filter(sales__isnull=False).select_related('category')

        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


class CategoriesList(APIView):
    """
    Класс для отображения категориев продуктов.
    """

    def get(self, request: Request) -> Response:
        categories = CategoryProduct.objects.filter(parent=None)
        serialized = CategorySerializer(
            categories,
            many=True,
        )
        # print(serialized.data)
        return Response(serialized.data)


class BannersList(APIView):
    """
    Класс для отображения любимых продуктов на главной странице.
    """

    def get(self, request: Request):

        categories = CategoryProduct.objects.filter(favourite=True)
        categories_list = [category for category in categories]
        banners = Product.objects.filter(category_id__in=categories_list)

        serializer = ProductSerializer(banners, many=True)

        return Response(serializer.data)
