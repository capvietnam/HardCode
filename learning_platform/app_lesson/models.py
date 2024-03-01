from django.db import models
from app_product.models import Product

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    video_link = models.URLField()

    def __str__(self):
        return self.title