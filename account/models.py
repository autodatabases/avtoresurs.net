from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vip_code = models.CharField(max_length=50, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.get_username()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def points(self):
        points = Point.objects.filter(account=self)
        print(points)
        user_points = 0
        for point in points:
            user_points += point.point
        return user_points


class Point(models.Model):
    account = models.ForeignKey(Account)
    point = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Балл'
        verbose_name_plural = 'Баллы'


class Prize(models.Model):
    sku = models.CharField(max_length=50)
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Приз'
        verbose_name_plural = 'Призы'