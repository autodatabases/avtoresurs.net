import re
from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models import Section, Designation, CarType, Supplier, TecdocLanguageDesManager


class PartManager(TecdocLanguageDesManager):
    use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        query = super(PartManager, self).get_queryset(*args, **kwargs)
        query = query.select_related('designation__description',
                                     'supplier')

        # query = query.prefetch_related('analogs', 'images')
        # query = query.prefetch_related('analogs')
        return query


class Part(models.Model):
    id = models.AutoField(db_column='ART_ID', primary_key=True)
    sku = models.CharField(db_column='ART_ARTICLE_NR', max_length=66)
    supplier = models.ForeignKey(Supplier, db_column='ART_SUP_ID', blank=True, null=True)
    art_des_id = models.IntegerField(db_column='ART_DES_ID', blank=True, null=True)
    designation = models.ForeignKey(Designation, db_column='ART_COMPLETE_DES_ID', blank=True,
                                    null=True)
    # groups = models.ManyToManyField('tecdoc.Group', through='tecdoc.PartGroup', related_name='parts')

    art_pack_selfservice = models.SmallIntegerField(db_column='ART_PACK_SELFSERVICE', blank=True,
                                                    null=True)
    art_material_mark = models.SmallIntegerField(db_column='ART_MATERIAL_MARK', blank=True,
                                                 null=True)
    art_replacement = models.SmallIntegerField(db_column='ART_REPLACEMENT', blank=True,
                                               null=True)
    art_accessory = models.SmallIntegerField(db_column='ART_ACCESSORY', blank=True,
                                             null=True)
    art_batch_size1 = models.IntegerField(db_column='ART_BATCH_SIZE1', blank=True,
                                          null=True)
    art_batch_size2 = models.IntegerField(db_column='ART_BATCH_SIZE2', blank=True,
                                          null=True)
    # car_type = models.ManyToManyField(CarType, through='tecdoc.PartTypeGroupSupplier')
    group = models.ManyToManyField('tecdoc.Group', through='tecdoc.PartGroup', verbose_name='Группа запчастей')

    objects = PartManager()

    def __str__(self):
        return "%s %s %s" % (self.designation.description.text, self.supplier, self.sku)

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


class PartGroup(models.Model):
    id = models.AutoField(db_column='la_id', primary_key=True, verbose_name='Ид')
    part = models.ForeignKey(Part, db_column='la_art_id', verbose_name='Запчасть')
    group = models.ForeignKey(Group, db_column='la_ga_id', verbose_name='Группа запчастей')
    sorting = models.IntegerField(db_column='la_sort', verbose_name='Порядок')
    car_type = models.ManyToManyField(CarType, through='tecdoc.PartTypeGroupSupplier', verbose_name='')

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'link_art'


class PartTypeGroupSupplier(models.Model):
    car_type = models.OneToOneField(CarType, db_column='lat_typ_id', primary_key=True)
    group = models.OneToOneField(Group, db_column='lat_ga_id', primary_key=True)
    part_group = models.OneToOneField(PartGroup, db_column='lat_la_id', primary_key=True)
    supplier = models.OneToOneField(Supplier, db_column='lat_sup_id')
    sorting = models.IntegerField(db_column='lat_sort', verbose_name='Порядок', primary_key=True)

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'link_la_typ'


class PartAnalogManager(models.Manager):
    # use_for_related_fields = True

    def get_queryset(self):
        return super(PartAnalogManager, self).\
            get_queryset().\
            filter(part__designation__language=tdsettings.LANG_ID).\
            select_related('part', 'part__designation__description')


class PartAnalog(models.Model):
    KIND = ((1, u'не оригинал'),
            (2, u'торговый'),
            (3, u'оригинал'),
            (4, u'номер замен'),
            (5, u'штрих-код'),
            )

    part = models.OneToOneField(Part, db_column='ARL_ART_ID', primary_key=True, verbose_name='Запчасть')
    number = models.CharField(db_column='ARL_DISPLAY_NR', max_length=105, verbose_name='Номер')
    search_number = models.CharField(db_column='ARL_SEARCH_NUMBER', max_length=105, verbose_name='Номер для поиска')
    kind = models.CharField(db_column='ARL_KIND', max_length=1, verbose_name='Тип')
    brand = models.ForeignKey('tecdoc.Brand', db_column='ARL_BRA_ID', null=True, blank=True,
                              verbose_name=u'Производитель', )
    sorting = models.IntegerField(db_column='ARL_SORT', verbose_name='Порядок')

    objects = PartAnalogManager()

    def __str__(self):
        return u'%s %s %s' % (self.kind, self.get_manufacturer(), self.get_sku())

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'art_lookup'

    def get_manufacturer(self):
        if self.kind in ['3', '4']:
            return self.brand
        else:
            return self.part.supplier

    def get_sku(self):
        # return self.search_number
        if self.kind in ['2', '3']:
            return self.number
        else:
            return self.part.sku


class Brand(models.Model):
    id = models.AutoField(db_column='BRA_ID', primary_key=True, verbose_name='Ид')
    title = models.CharField(db_column='BRA_BRAND', max_length=60, verbose_name='Название', blank=True, null=True)
    code = models.CharField(db_column='BRA_MFC_CODE', max_length=30, blank=True, null=True, verbose_name='Название')

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'brands'
        ordering = ['title']
        verbose_name = u'Бренд'
        verbose_name_plural = u'Бренды'

    def __str__(self):
        return self.title.upper()
        # return self.title.capitalize()
