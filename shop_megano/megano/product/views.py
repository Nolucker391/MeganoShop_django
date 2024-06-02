import datetime

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from .models import Product, CategoryProduct, Review, Tag
from .serializers import ProductSerializer, ReviewSerializer, TagSerializer


class SetPagePagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'currentPage'
    max_page_size = 8

    def get_paginated_response(self, data):
        print(self.page.__dict__)
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages
        })


class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    pagination_class = SetPagePagination
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):

        filter_dict = dict()
        sort_list = list()

        filter_dict["count__gt"] = 0

        name = request.query_params.get('filter[name]') or None
        if name:
            filter_dict["title__iregex"] = name

        avail = request.query_params.get('filter[available]', None)
        if avail is not None:
            filter_dict["archived"] = False if avail == 'true' else True
        else:
            sort_list.append('archived')

        deliver = request.query_params.get('filter[freeDelivery]', None)
        if deliver is not None:
            if deliver == 'true':
                filter_dict["freeDelivery"] = True
        else:
            sort_list.append("-freeDelivery")

        tags = request.query_params.getlist('tags[]') or None
        if tags:
            filter_dict["tags__in"] = tags

        min_price = float(request.query_params.get('filter[minPrice]') or 0)
        max_price = float(request.query_params.get('filter[maxPrice]') or 50000)
        filter_dict["price__range"] = (min_price, max_price)

        category = request.META['HTTP_REFERER'].split('/')[4] or None
        sort = request.GET.get('sort')

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
                filter_dict["category_id__in"] = all_categories

        products_list = Product.objects.filter(**filter_dict)

        if request.GET.get('sortType') == 'inc':
            sortType = '-'
        else:
            sortType = ''

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
        queryset = products_list

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ProductsList(APIView):
    """
    Класс view. Отображает продукты на странице.
    """

    def get(self, request: Request) -> Response:
        filter_dict = dict()
        sort_list = list()

        filter_dict["count__gt"] = 0

        name = request.query_params.get('filter[name]') or None
        if name:
            filter_dict["title__iregex"] = name

        avail = request.query_params.get('filter[available]', None)
        if avail is not None:
            filter_dict["archived"] = False if avail == 'true' else True
        else:
            sort_list.append('archived')

        deliver = request.query_params.get('filter[freeDelivery]', None)
        if deliver is not None:
            if deliver == 'true':
                filter_dict["freeDelivery"] = True
        else:
            sort_list.append("-freeDelivery")

        tags = request.query_params.getlist('tags[]') or None
        if tags:
            filter_dict["tags__in"] = tags

        min_price = float(request.query_params.get('filter[minPrice]') or 0)
        max_price = float(request.query_params.get('filter[maxPrice]') or 50000)
        filter_dict["price__range"] = (min_price, max_price)

        category = request.META['HTTP_REFERER'].split('/')[4] or None
        sort = request.GET.get('sort')

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
                filter_dict["category_id__in"] = all_categories

        print(filter_dict)
        products_list = Product.objects.filter(**filter_dict)

        if request.GET.get('sortType') == 'inc':
            sortType = '-'
        else:
            sortType = ''

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

        paginator = SetPagePagination()
        paganation_products = paginator.paginate_queryset(products_list, request)

        serializer = ProductSerializer(paganation_products, many=True)

        return Response({'items': serializer.data})


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
