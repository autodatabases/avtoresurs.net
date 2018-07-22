from cms.models import CMSPlugin
from colorfield.fields import ColorField
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from registration.signals import user_registered

from main.utils import get_file_path
from news.models import Post, Categories
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


class PostPlugin(CMSPlugin):
    latest_articles = models.IntegerField(
        default=6,
        # help_text=_('The maximum number of latest articles to display.')
    )
    category = models.CharField(max_length=10, choices=Categories.as_choices(), default='normal',
                                verbose_name='Категория')
    render_template = models.CharField(max_length=255, default='main/includes/right_news_list.html')

    def __str__(self):
        return str(self.latest_articles)

    def get_posts(self):
        posts = Post.objects.filter(category=self.category)[:self.latest_articles]
        return posts


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


class StockModelPlugin(CMSPlugin):
    text_left = HTMLField(max_length=255, default='', verbose_name='Текст слева')
    text_right = HTMLField(max_length=255, default='', verbose_name='Текст справа')
    url = models.CharField(max_length=255, null=True, verbose_name='Ссылка')
    color = ColorField(default='#FF0000', verbose_name='Цвет фона справа')
    image = models.ImageField(upload_to=get_file_path,
                              null=True,
                              blank=True,
                              verbose_name=_('Картинка'))

    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')

    def rgba(self):
        hex_value = self.color.lstrip('#')
        lv = len(hex_value)
        rgba_value = tuple(int(hex_value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        return rgba_value

    def image_src(self):
        try:
            return self.image.url
        except ValueError:
            return None


def user_registered_callback(sender, user, request, **kwargs):
    profile = Profile(user=user)
    profile.save()


user_registered.connect(user_registered_callback)
