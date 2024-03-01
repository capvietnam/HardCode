from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg, F
from rest_framework.response import Response
from django.contrib.auth.models import User

from app_product.models import Product
from .serializers import AvailableProductSerializer, ProductWithLessonsSerializer, LessonSerializer
from app_lesson.models import Lesson
from app_group.models import Group
from app_product.models import Access

class AvailableProductsListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(accesses__isnull=True)  # Фильтруем доступные для покупки продукты
    serializer_class = AvailableProductSerializer
    permission_classes = [AllowAny]


class ProductsListWithLessonsAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithLessonsSerializer
    permission_classes = [IsAuthenticated]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем идентификатор продукта из URL запроса
        product_id = self.kwargs['product_id']
        # Получаем уроки для указанного продукта, на который у пользователя есть доступ
        return Lesson.objects.filter(product_id=product_id, product__accesses__user=self.request.user)


class GroupFillPercentageAPIView(generics.GenericAPIView):
    queryset = Group.objects.all()

    def get(self, request, *args, **kwargs):
        # Получаем среднее значение заполненности групп по формуле:
        # (количество участников в группе) / (максимальное количество участников в группе) * 100
        avg_fill_percentage = self.get_queryset().annotate(
            fill_percentage=Avg(F('students__count') / F('product__max_users') * 100)
        ).aggregate(avg_fill_percentage=Avg('fill_percentage'))['avg_fill_percentage']

        return Response({'fill_percentage': avg_fill_percentage})

class ProductPurchasePercentageAPIView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        # Получаем общее количество пользователей на платформе
        total_users_count = User.objects.count()

        # Получаем количество доступов к продуктам
        accesses_count = Access.objects.count()

        # Рассчитываем процент приобретения продукта
        if total_users_count > 0:
            purchase_percentage = (accesses_count / total_users_count) * 100
        else:
            purchase_percentage = 0

        return Response({'purchase_percentage': purchase_percentage})