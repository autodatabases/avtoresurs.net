from cms.models import CMSPlugin
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from registration.signals import user_registered

from main.utils import get_file_path
from news.models import Post
from profile.models import Profile
from django.utils.translation import ugettext_lazy as _

from shop.models import Storage


class Assortment(models.Model):
    image = models.ImageField(verbose_name='Картинка')
    title = models.CharField(max_length=100, verbose_name='Название')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]
        verbose_name = 'Ассортимент'
        verbose_name_plural = 'Ассортимент'


class ArrivalItem(models.Model):
    image = models.ImageField(verbose_name='Картинка')
    title = models.CharField(max_length=100, verbose_name='Название')
    post = models.ForeignKey(Post, verbose_name='Ссылка на новость', null=True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    active = models.BooleanField(default=True, verbose_name='Активный')

    class Meta:
        ordering = ['-added']
        verbose_name = 'Поступление товара'
        verbose_name_plural = 'Поступление товаров'


class ArrivalItemModelPlugin(CMSPlugin):
    latest_goods = models.IntegerField(
        default=6,
        help_text=_('The maximum number of latest goods to display.')
    )

    def get_goods(self):
        goods = ArrivalItem.objects.filter(active=True)[:self.latest_goods]
        return goods


class ProposalModelPlugin(CMSPlugin):
    caption = models.CharField(max_length=25, default='Лучшее предложение!', verbose_name='Заголовок')
    brand = models.CharField(max_length=25, default='', verbose_name='Брэнд')
    sku = models.CharField(max_length=25, default='', verbose_name='Артикул')
    url = models.CharField(max_length=255, null=True, verbose_name='Ссылка на продукт')
    image = models.ImageField(upload_to=get_file_path,
                              null=True,
                              blank=True,
                              verbose_name=_('Картинка'))

    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')


class StoreAddressModelPlugin(CMSPlugin):
    @property
    def stores(self):
        storages = Storage.objects.filter(active=True)
        return storages


def user_registered_callback(sender, user, request, **kwargs):
    profile = Profile(user=user)
    profile.save()


user_registered.connect(user_registered_callback)
