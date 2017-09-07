from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название категории')
    active = models.BooleanField(default=True, verbose_name='Активен')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')

class CategoryBrand(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория')
    brand_title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Брэнд')