from django.contrib.auth.models import User
from django.db import models


class Bonus(models.Model):
    id_1c = models.CharField(default=None, null=False, max_length=10, verbose_name='ИД бонусного товара')
    title = models.CharField(max_length=255, default='', verbose_name='Название')
    price = models.IntegerField(default=None, null=True, verbose_name='Цена в баллах')
    image = models.ImageField(default=None, blank=True, null=True, verbose_name='Картинка')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Изменена')

    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'

    def __str__(self):
        return "%s, %s " % (self.id_1c, self.title)


class UserBonus(models.Model):
    user = models.ForeignKey(User)
    bonus = models.ForeignKey(Bonus)

    class Meta:
        verbose_name = 'Бонусы пользователя'
        verbose_name_plural = 'Бонусы пользователя'

    def __str__(self):
        return "%s, %s" % (self.user, self.bonus)
