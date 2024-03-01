from django.urls import path
from .views import AvailableProductsListAPIView, ProductsListWithLessonsAPIView, LessonListAPIView, \
    ProductPurchasePercentageAPIView

urlpatterns = [
    path('available-products/', AvailableProductsListAPIView.as_view(), name='available-products-list'),
    path('products-with-lessons/', ProductsListWithLessonsAPIView.as_view(), name='products-with-lessons-list'),
    path('products/<int:product_id>/lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('product-purchase-percentage/', ProductPurchasePercentageAPIView.as_view(),
         name='product-purchase-percentage'),
]
