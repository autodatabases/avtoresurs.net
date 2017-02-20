from django.db import models


# Create your models here.

class Prize(models.Model):
    # todo rename to Bonus and move from account app

    sku = models.CharField(max_length=50)
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Приз'
        verbose_name_plural = 'Призы'
