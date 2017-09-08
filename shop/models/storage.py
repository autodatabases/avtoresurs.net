from django.db import models

from shop.models.product import Product


class Storage(models.Model):
    """ class for Storages """
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название склада')
    active = models.BooleanField(default=True, verbose_name='Активен')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')


class ProductStorage(models.Model):
    """ class for M2M relationships between Product and Storage """
    product = models.ManyToManyField(Product, verbose_name='Изделие')
    storage = models.ManyToManyField(Storage, verbose_name='Склад')
    active = models.BooleanField(default=True, verbose_name='Активен')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')