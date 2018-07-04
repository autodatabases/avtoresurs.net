from django.db import models
from cms.models import CMSPlugin


class ShopManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Shop(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название новости')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    image = models.ImageField(null=True, blank=True, verbose_name='Картинка')
    lat = models.FloatField(default=54.660735, verbose_name='Широта')
    lon = models.FloatField(default=21.308233, verbose_name='Долгота')
    address = models.CharField(max_length=1000, default='', verbose_name='Адрес')
    schedule = models.CharField(max_length=500, default='09:00 - 19:00', verbose_name='График работы')
    phones = models.CharField(max_length=500, default='', verbose_name='Телефоны')
    objects = ShopManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class ShopPlugin(CMSPlugin):
    latest_shops = models.IntegerField(
        default=20,
    )

    def __str__(self):
        return str(self.latest_shops)

    def get_shops(self):
        shops = Shop.objects.all()[:self.latest_shops]
        return shops
