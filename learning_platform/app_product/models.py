from django.db import models
from django.contrib.auth.models import User
from app_group.models import Group
from collections import deque


class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_products')
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)  # Изменил точность для большей гибкости

    def __str__(self):
        return self.name


class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accesses')
    product = models.ForeignKey('app_product.Product', on_delete=models.CASCADE, related_name='accesses')

    # Эта модель позволяет нам понимать, что у пользователя есть доступ к продукту

    class Meta:
        unique_together = (('user', 'product'),)  # Гарантируем уникальность доступа

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"

    def save(self, *args, **kwargs):
        # Вызываем оригинальную функцию save
        super(Access, self).save(*args, **kwargs)
        # После сохранения доступа, запускаем алгоритм распределения
        distribute_users_evenly(self.user, self.product)


def distribute_users_evenly(user, product):
    # Получаем все группы для данного продукта
    groups = Group.objects.filter(product=product)

    # Пересчитываем количество участников в каждой группе
    group_sizes = [group.students.count() for group in groups]

    # Сортируем группы по количеству участников по возрастанию
    sorted_groups = sorted(groups, key=lambda x: x.students.count())

    # Создаем очередь из пользователей, которых нужно распределить
    user_queue = deque([user])

    # Пока в очереди есть пользователи для распределения
    while user_queue:
        # Извлекаем пользователя из очереди
        current_user = user_queue.popleft()

        # Ищем группу с минимальным количеством участников
        min_group = sorted_groups[0]

        # Если в этой группе уже достигнуто максимальное количество участников,
        # добавляем новую группу
        if min_group.students.count() >= min_group.max_users:
            new_group = Group.objects.create(product=product, name=f"Group {len(groups) + 1}")
            sorted_groups.append(new_group)
            min_group = new_group

        # Добавляем пользователя в группу с минимальным количеством участников
        min_group.students.add(current_user)

        # Пересчитываем количество участников в каждой группе
        group_sizes = [group.students.count() for group in sorted_groups]

        # Сортируем группы по количеству участников по возрастанию
        sorted_groups = sorted(sorted_groups, key=lambda x: x.students.count())

        # Проверяем, есть ли группы, в которых количество участников больше
        # чем в соседней группе на 2 или более
        for i in range(len(sorted_groups) - 1):
            if group_sizes[i] - group_sizes[i + 1] >= 2:
                # Если такие группы найдены, добавляем лишних участников в очередь для перераспределения
                excess_users = sorted_groups[i].students.all()[:group_sizes[i] - group_sizes[i + 1] - 1]
                user_queue.extend(excess_users)
                # Удаляем лишних участников из группы
                sorted_groups[i].students.remove(*excess_users)
