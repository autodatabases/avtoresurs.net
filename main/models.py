from django.db import models
from registration.signals import user_registered

# Create your models here.
from profile.models import Profile


class Slider(models.Model):
    image = models.ImageField(verbose_name='Картинка')
    caption = models.CharField(max_length=100, verbose_name='Заголовок слайда')
    text = models.CharField(max_length=100, verbose_name='Текст на слайде')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    order = models.SmallIntegerField(default=0, verbose_name='Сортировка')

    class Meta:
        ordering = ["order"]
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'


# class About(models.Model):
#


def user_registered_callback(sender, user, request, **kwargs):
    profile = Profile(user=user)
    profile.save()


user_registered.connect(user_registered_callback)
