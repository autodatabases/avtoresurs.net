from django.db import models

from shop.models.product import Product, ProductPrice


class Storage(models.Model):
    """ class for Storages """
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название склада')
    active = models.BooleanField(default=True, verbose_name='Активен')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    products = models.ManyToManyField(Product, through='ProductStoragePrice')
    prices = models.ManyToManyField(ProductPrice, through='ProductStoragePrice')

    class Meta:
        ordering = ['name']
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name


class ProductStoragePrice(models.Model):
    """ class for M2M relationships between Product and Storage """
    product = models.ForeignKey(Product, verbose_name='Изделие')
    storage = models.ForeignKey(Storage, verbose_name='Склад')
    price = models.ForeignKey(ProductPrice, verbose_name='Цены на изделие')
    active = models.BooleanField(default=True, verbose_name='Активен')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
