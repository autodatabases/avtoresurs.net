from django.contrib.auth.models import User
from django.db import models


class Bonus(models.Model):
    id_1c = models.IntegerField(default=None, null=False)
    model = models.CharField(max_length=150, default='')
    brand = models.CharField(max_length=100, default='')
    price = models.IntegerField(default=None, null=False)
    image = models.ImageField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    sku = models.CharField(max_length=50)
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'

    def __str__(self):
        return "%s, %s (%s)" % (self.id_1c, self.model, self.brand)


class UserBonus(models.Model):
    user = models.ForeignKey(User)
    bonus = models.ForeignKey(Bonus)

    class Meta:
        verbose_name = 'Бонусы пользователя'
        verbose_name_plural = 'Бонусы пользователя'

    def __str__(self):
        return "%s, %s" % (self.user, self.bonus)
