# from django.core.urlresolvers import reverse
from cms.models import CMSPlugin
from django.db import models

# Create your models here.
from django.urls import reverse
from djangocms_text_ckeditor.fields import HTMLField
from enum import Enum


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Categories(Enum):
    Normal = 'Обычная'
    Supplier = 'Поставщики'
    Arrival = 'Поступление товара'

    @classmethod
    def as_choices(cls):
        return tuple((x.name, x.value) for x in cls)


class Post(models.Model):
    class Meta:
        ordering = ["-added"]
        verbose_name = 'Новость'
        verbose_name_plural = 'Публикации'

    title = models.CharField(max_length=255, verbose_name='Название новости')
    content = HTMLField(null=True, blank=True, verbose_name='Содержание')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    image = models.ImageField(null=True, blank=True, verbose_name='Картинка')
    status = models.BooleanField(default=True, verbose_name='Активен')
    category = models.CharField(max_length=10, choices=Categories.as_choices(), default='normal',
                                verbose_name='Категория')

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/news/{id}".format(id=self.id)
