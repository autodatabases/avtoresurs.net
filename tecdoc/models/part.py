from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models import Section, Designation


class Part(models.Model):
    art_id = models.IntegerField(primary_key=True, db_column='ART_ID')  # Field name made lowercase.
    art_article_nr = models.CharField(db_column='ART_ARTICLE_NR', max_length=66)  # Field name made lowercase.
    art_sup_id = models.SmallIntegerField(db_column='ART_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    art_des_id = models.IntegerField(db_column='ART_DES_ID', blank=True, null=True)  # Field name made lowercase.
    art_complete_des_id = models.IntegerField(db_column='ART_COMPLETE_DES_ID', blank=True,
                                              null=True)  # Field name made lowercase.
    art_pack_selfservice = models.SmallIntegerField(db_column='ART_PACK_SELFSERVICE', blank=True,
                                                    null=True)  # Field name made lowercase.
    art_material_mark = models.SmallIntegerField(db_column='ART_MATERIAL_MARK', blank=True,
                                                 null=True)  # Field name made lowercase.
    art_replacement = models.SmallIntegerField(db_column='ART_REPLACEMENT', blank=True,
                                               null=True)  # Field name made lowercase.
    art_accessory = models.SmallIntegerField(db_column='ART_ACCESSORY', blank=True,
                                             null=True)  # Field name made lowercase.
    art_batch_size1 = models.IntegerField(db_column='ART_BATCH_SIZE1', blank=True,
                                          null=True)  # Field name made lowercase.
    art_batch_size2 = models.IntegerField(db_column='ART_BATCH_SIZE2', blank=True,
                                          null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = tdsettings.DB_PREFIX + 'articles'


class Group(models.Model):
    id = models.AutoField(db_column='ga_id', primary_key=True, verbose_name='Ид')
    ga_nr = models.SmallIntegerField(db_column='ga_nr', blank='True', null='True')
    designation = models.ForeignKey(Designation, db_column='ga_des_id', verbose_name='Описание', related_name='+')
    standart = models.ForeignKey(Designation, db_column='ga_des_id_standart', verbose_name='Стандарт', related_name='+')
    assembly = models.ForeignKey(Designation, db_column='ga_des_id_assembly', verbose_name='Где устанавливается',
                                 related_name='+')
    intended = models.ForeignKey(Designation, db_column='ga_des_id_intended', verbose_name='Во что входит',
                                 related_name='+')
    ga_universal = models.SmallIntegerField(db_column='ga_universal')
    section = models.ManyToManyField(Section, through='tecdoc.SectionGroup', verbose_name='Категории')
    #
    class Meta:
        db_table = tdsettings.DB_PREFIX + 'generic_articles'


class SectionGroup(models.Model):
    car_section = models.OneToOneField(Section, db_column='lgs_str_id', primary_key=True)
    group = models.OneToOneField(Group, db_column='lgs_ga_id', primary_key=True)

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'link_ga_str'
        # unique_together = (("car_section", "group"),)
