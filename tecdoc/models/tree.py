from django.db import models

from tecdoc.models import CarType


class CarTree(models.Model):
    car_type = models.ForeignKey(CarType, db_column='passangercarid')
    type = models.BigIntegerField(db_column='searchtreeid')
    id = models.BigIntegerField(db_column='id')
    parent_id = models.BigIntegerField(db_column='parentid', blank=True, null=True)
    title = models.CharField(db_column='description',max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'passanger_car_trees'
