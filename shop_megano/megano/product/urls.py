from django.urls import path

from .views import (
    ProductsList,
    ProductDetails,
    PopularProductsList,
    LimitedEditionList,
    ReviewCreateProduct,
    TagsList,
ProductsListView
)

urlpatterns = [
    path('api/catalog/', ProductsListView.as_view(), name='products-list'),
    path('api/product/<int:pk>/', ProductDetails.as_view(), name='product-details'),
    path('api/products/popular/', PopularProductsList.as_view(), name='popular-products'),
    path('api/products/limited/', LimitedEditionList.as_view(), name='limited-products'),
    path('api/product/<int:pk>/reviews', ReviewCreateProduct.as_view(), name='review-create'),
    path('api/tags/', TagsList.as_view(), name='tags-list'),
]
