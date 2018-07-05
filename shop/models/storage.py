from django.db import models
from cms.models import CMSPlugin
from shop.models.product import Product, ProductPrice


class StorageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


class Storage(models.Model):
    """ class for Storages """
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название склада')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='E-mail склада')
    active = models.BooleanField(default=True, verbose_name='Активен')
    file_name = models.CharField(max_length=100, default='News_auto_', null=True, verbose_name='Название файла склада на FTP')
    active_file_upload = models.BooleanField(default=False, verbose_name='Автоматическая загрузка')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    image = models.ImageField(null=True, blank=True, verbose_name='Картинка')
    lat = models.FloatField(default=54.660735, verbose_name='Широта')
    lon = models.FloatField(default=21.308233, verbose_name='Долгота')
    address = models.CharField(max_length=1000, default='', verbose_name='Адрес')
    schedule = models.CharField(max_length=500, default='09:00 - 19:00', verbose_name='График работы')
    phones = models.CharField(max_length=500, default='', verbose_name='Телефоны')
    # products = models.ManyToManyField(Product, through='ProductStoragePrice')
    # prices = models.ManyToManyField(ProductPrice, through='ProductStoragePrice')

    objects = StorageManager()

    class Meta:
        ordering = ['pk']
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name


class StoragePlugin(CMSPlugin):
    latest_shops = models.IntegerField(
        default=20,
    )

    def __str__(self):
        return str(self.latest_shops)

    def get_shops(self):
        shops = Storage.objects.all()[:self.latest_shops]
        return shops


# class ProductStoragePrice(models.Model):
#     """ class for M2M relationships between Product and Storage """
#     product = models.ForeignKey(Product, verbose_name='Изделие')
#     storage = models.ForeignKey(Storage, verbose_name='Склад')
#     price = models.ForeignKey(ProductPrice, verbose_name='Цены на изделие')
#     active = models.BooleanField(default=True, verbose_name='Активен')
#     added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
#     updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
#
#     def __str__(self):
#         return "%s" % (self.storage)
