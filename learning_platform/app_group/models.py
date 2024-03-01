from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    product = models.ForeignKey('app_product.Product', on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=100)
    min_users = models.IntegerField(default=0)  # Минимальное количество пользователей в группе
    max_users = models.IntegerField(default=10) # Максимальное количество пользователей в группе
    students = models.ManyToManyField(User, related_name='groups_related')

    def __str__(self):
        return f"{self.name} ({self.product.name})"