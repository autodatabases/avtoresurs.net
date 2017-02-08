from django.db import models


# Create your models here.



class Slider(models.Model):
    image = models.ImageField(verbose_name='Картинка')
    caption = models.CharField(max_length=100, verbose_name='Заголовок слайда')
    text = models.CharField(max_length=100, verbose_name='Текст на слайде')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    order = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
