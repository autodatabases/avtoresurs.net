from cms.models import CMSPlugin
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from registration.signals import user_registered
from profile.models import Profile
from django.utils.translation import ugettext_lazy as _


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


# class SliderPlugin(CMSPlugin):
#     right_caption = models.CharField(max_length=128, verbose_name='Заголовок справа', blank=True, null=True)
#     text = HTMLField(max_length=2000, verbose_name='Описание', blank=True, null=True)
#
#     def __str__(self):
#         return self.right_caption
#
#     def get_slides(self):
#         slides = Slide.objects.all()
#         return slides
#
#
# class PhonePlugin(CMSPlugin):
#     phone_text = HTMLField(max_length=2000, verbose_name='Телефоны', blank=True, null=True)


#
# class Slide(models.Model):
#     image = models.ImageField(verbose_name='Картинка')
#     caption = models.CharField(max_length=100, verbose_name='Заголовок слайда')
#     text = models.CharField(max_length=100, verbose_name='Текст на слайде')
#     added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
#     updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
#     order = models.SmallIntegerField(default=0, verbose_name='Сортировка')
#
#     class Meta:
#         ordering = ["order"]
#         verbose_name = 'Слайд'
#         verbose_name_plural = 'Слайды'


class AssortmentPlugin(CMSPlugin):
    def assortment(self):
        assort = Assortment.objects.all().filter(active=True)
        return assort


def user_registered_callback(sender, user, request, **kwargs):
    profile = Profile(user=user)
    profile.save()


user_registered.connect(user_registered_callback)
