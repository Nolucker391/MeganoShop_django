import datetime

from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.mixins import CreateModelMixin


from .models import Product, CategoryProduct, Review, Tag
from .serializers import ProductSerializer, ReviewSerializer, TagSerializer


class ProductsList(APIView):
    """
    Класс view. Отображает продукты на странице.
    """
    def get(self, request: Request) -> Response:
        # str = ("filter[name]="
        #        "&filter[minPrice]=0"
        #        "&filter[maxPrice]=50000"
        #        "&filter[freeDelivery]=false"
        #        "&filter[available]=true"
        #        "&currentPage=1"
        #        "&sort=price"
        #        "&sortType=inc"
        #        "&limit=20") # дефолтный запрос выглядит так
        # Берем параметры, которые отправляются при запросе

        name = request.query_params.get('filter[name]') or None

        if request.query_params.get('filter[available]') == 'true':
            archived = False
        else:
            archived = True

        if request.query_params.get('filter[freeDelivery]') == 'true':
            freeDelivery = True
        else:
            freeDelivery = False

        tags = request.query_params.getlist('tags[]') or None
        min_price = request.query_params.get('filter[minPrice]')
        max_price = request.query_params.get('filter[maxPrice]')
        category = request.META['HTTP_REFERER'].split('/')[4] or None
        sort = request.GET.get('sort')

        if request.GET.get('sortType') == 'inc':
            sortType = '-'
        else:
            sortType = ''

        current_page = request.GET.get('currentPage')

        products_list = Product.objects.filter(
            page_number=current_page,
            price__range=(min_price, max_price),
            count__gt=0,
        )

        if category:
            if category.startswith('?filter='):
                if name is None:
                    name = category[8:]
            else:
                parent_category = CategoryProduct.objects.filter(
                    parent_id=category,
                )
                all_categories = [subcat.pk for subcat in parent_category]
                all_categories.append(int(category))
                products_list = products_list.filter(
                    category_id__in=all_categories,
                )

        if name:
            products_list = products_list.filter(
                title__iregex=name,
            )
        if tags:
            products_list = products_list.filter(
                tags__in=tags,
            )
        if freeDelivery:
            products_list = products_list.filter(
                freeDelivery=freeDelivery,
            )
        if archived:
            products_list = products_list.filter(
                archived=archived,
            )
        if sort == 'reviews':
            products_list = products_list.annotate(
                count_reviews=Count('reviews'),
            ).order_by(
                f'{sortType}count_reviews'
            )
        else:
            products_list = products_list.order_by(
                f'{sortType}{sort}',
            )
        products_list = products_list.prefetch_related(
            'images',
            'tags',
        )

        serializer = ProductSerializer(products_list, many=True)

        return Response({'items': serializer.data,
                         'lastPage': 4})



class ProductDetails(APIView):
    def get(self, request: Request, pk: int):
        products = Product.objects.get(pk=pk)
        serializer = ProductSerializer(products, many=False)

        return Response(serializer.data)

class PopularProductsList(APIView):
    """
    Класс
    """
    def get(self, request: Request):
        popular_product_to_reviews = Product.objects.filter(
            archived=False,
        ).annotate(
            count_reviews=Count('reviews'),
        ).order_by('-count_reviews')[:4]

        serializer = ProductSerializer(popular_product_to_reviews, many=True)

        return Response(serializer.data)

class LimitedEditionList(APIView):
    def get(self, request: Request):
        products = Product.objects.filter(limited_edition=True)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

class ReviewCreateProduct(APIView, CreateModelMixin):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk):
        product = get_object_or_404(
            Product,
            pk=pk,
        )

        Review.objects.create(
            author=request.data['author'],
            email=request.data['email'],
            text=request.data['text'],
            rate=request.data['rate'],
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
    def get(self, request: Request) -> Response:
        tags = Tag.objects.all()
        serialized = TagSerializer(
            tags,
            many=True,
        )
        return Response(serialized.data)
