from django.db import models

from tecdoc.models import CarType


# from tecdoc.models.base import Designation, TecdocLanguageDesManager


# class Section(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='STR_ID')
#     # parent_id = models.ForeignKey('self', db_column='STR_ID_PARENT', blank=True, null=True)
#     parent_id = models.IntegerField(db_column='STR_ID_PARENT', blank=True, null=True)
#     str_type = models.SmallIntegerField(db_column='STR_TYPE', blank=True, null=True)
#     level = models.SmallIntegerField(db_column='STR_LEVEL', blank=True, null=True)
#     designation = models.ForeignKey(Designation, db_column='STR_DES_ID', blank=True,
#                                     null=True)
#     str_sort = models.SmallIntegerField(db_column='STR_SORT', blank=True, null=True)
#     str_node_nr = models.IntegerField(db_column='STR_NODE_NR', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'search_tree'
#
#     def __str__(self):
#         return "%s %s %s" % (self.id, self.parent_id, self.level)
#         # return "%s %s %s %s" % (self.id, self.parent_id, self.level, self.designation)
#
#     objects = TecdocLanguageDesManager()


class Section(models.Model):
    class Meta:

        db_table = 'passanger_car_trees'

    car_type = models.ForeignKey(CarType, db_column='passangercarid')
    type = models.BigIntegerField(db_column='searchtreeid')
    id = models.BigIntegerField(db_column='id', primary_key=True)
    parent_id = models.BigIntegerField(db_column='parentid', blank=True, null=True)
    title = models.CharField(db_column='description', max_length=512, blank=True, null=True)

    def __gt__(self, other):
        return self.title > other.title
