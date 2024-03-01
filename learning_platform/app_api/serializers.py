from rest_framework import serializers

from app_product.models import Product
from app_lesson.models import Lesson


class AvailableProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'start_date', 'cost']


class ProductWithLessonsSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'start_date', 'cost', 'num_lessons']

    def get_num_lessons(self, obj):
        return obj.lessons.count()

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link']
