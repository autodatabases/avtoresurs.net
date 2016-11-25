from django.db import models

from tecdoc.models import TecdocLanguageManager, Designation, TecdocLanguageDesManager
from tecdoc.apps import TecdocConfig as tdsettings


class Section(models.Model):
    id = models.IntegerField(primary_key=True, db_column='STR_ID')
    # parent_id = models.ForeignKey('self', db_column='STR_ID_PARENT', blank=True, null=True)
    parent_id = models.IntegerField(db_column='STR_ID_PARENT', blank=True, null=True)
    str_type = models.SmallIntegerField(db_column='STR_TYPE', blank=True, null=True)
    level = models.SmallIntegerField(db_column='STR_LEVEL', blank=True, null=True)
    designation = models.ForeignKey(Designation, db_column='STR_DES_ID', blank=True,
                                    null=True)
    str_sort = models.SmallIntegerField(db_column='STR_SORT', blank=True, null=True)
    str_node_nr = models.IntegerField(db_column='STR_NODE_NR', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_tree'

    def __str__(self):
        return "%s %s %s" % (self.id, self.parent_id, self.level)
        # return "%s %s %s %s" % (self.id, self.parent_id, self.level, self.designation)

    objects = TecdocLanguageDesManager()
