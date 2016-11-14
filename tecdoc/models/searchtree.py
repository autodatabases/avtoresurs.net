from django.db import models
from tecdoc.models import Designation, TecdocManagerWithDes


class SearchTree(models.Model):
    id = models.IntegerField(primary_key=True, db_column='STR_ID')  # Field name made lowercase.
    parent_id = models.IntegerField('self', db_column='STR_ID_PARENT', blank=True,
                                    null=True)  # Field name made lowercase.
    str_type = models.SmallIntegerField(db_column='STR_TYPE', blank=True, null=True)  # Field name made lowercase.
    level = models.SmallIntegerField(db_column='STR_LEVEL', blank=True, null=True)  # Field name made lowercase.
    designation = models.ForeignKey(Designation, db_column='STR_DES_ID', blank=True,
                                    null=True)  # Field name made lowercase.
    str_sort = models.SmallIntegerField(db_column='STR_SORT', blank=True, null=True)  # Field name made lowercase.
    str_node_nr = models.IntegerField(db_column='STR_NODE_NR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'search_tree'

    def __str__(self):
        return "%s %s %s %s" % (self.id, self.parent_id, self.level, self.designation)
        # return "%s %s %s %s" % (self.id, self.parent_id, self.level, self.level)

    objects = TecdocManagerWithDes()