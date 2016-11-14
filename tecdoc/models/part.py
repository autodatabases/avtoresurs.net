# -*- coding: utf-8 -
import re

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models import Q

from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes, Designation)
from tecdoc.models.car import CarType

CACHE_PREFIX = settings.CACHE_MIDDLEWARE_KEY_PREFIX

number_re = re.compile('[^a-zA-Z0-9]+')


def clean_number(number):
    return number_re.sub('', number)


class PartManager(TecdocManagerWithDes):
    def get_queryset(self, *args, **kwargs):
        query = super(PartManager, self).get_queryset(*args, **kwargs)
        query = query.select_related('designation__description',
                                     'supplier')

        # query = query.prefetch_related('analogs', 'images')
        query = query.prefetch_related('analogs')
        return query

    def lookup(self, number, manufacturer=None):
        query = Q(search_number=clean_number(number))
        if manufacturer:
            if isinstance(manufacturer, int):
                query &= Q(part__supplier=manufacturer) | Q(brand=manufacturer)
            elif hasattr(manufacturer, '__iter__'):
                query &= Q(part__supplier__title__in=manufacturer) | Q(brand__title__in=manufacturer)
            else:
                query &= Q(part__supplier__title=manufacturer) | Q(brand__title=manufacturer)
        return PartAnalog.objects.filter(query)


class Part(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='ART_ID')

    sku = models.CharField(u'Название', max_length=66,
                           db_column='ART_ARTICLE_NR')

    supplier = models.ForeignKey('tecdoc.Supplier', verbose_name=u'Поставщик',
                                 db_column='ART_SUP_ID')

    # don`t use
    # short_designation = models.ForeignKey('tecdoc.Designation',
    #                                      verbose_name=u'Краткое Обозначение',
    #                                      db_column='ART_DES_ID',
    #                                      related_name='parts_with_short_designation')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='ART_COMPLETE_DES_ID')

    # car_types = models.ManyToManyField('tecdoc.CarType',
    #                                   verbose_name=u'Модификации авто',
    #                                   through='tecdoc.PartTypeGroupSupplier',
    #                                   related_name='parts')

    groups = models.ManyToManyField('tecdoc.Group',
                                    verbose_name=u'Группа запчастей',
                                    through='tecdoc.PartGroup',
                                    related_name='parts')

    criteries = models.ManyToManyField('tecdoc.Criteria',
                                       verbose_name=u'Оговорки',
                                       through='tecdoc.PartCriteria',
                                       related_name='parts')

    texts = models.ManyToManyField('tecdoc.TextModule',
                                   verbose_name=u'Описание',
                                   through='tecdoc.PartDescription',
                                   related_name='parts')

    # images = models.ManyToManyField('tecdoc.Image',
    #                                 verbose_name=u'Изображения',
    #                                 through='tecdoc.PartImage',
    #                                 related_name='parts')

    pdfs = models.ManyToManyField('tecdoc.PdfFile',
                                  verbose_name=u'Инструкция',
                                  through='tecdoc.PartPdf',
                                  related_name='parts')

    objects = PartManager()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'articles'

    def __str__(self):
        return u'%s %s %s' % (self.designation,
                              self.supplier,
                              self.sku)

    # def list_sections(self):
    #     groups = self.groups.distrint()
    #     return Section.objects.filter(groups__in=groups)

    def list_car_types(self):
        return CarType.objects.filter(parttypegroupsupplier__part__part=self).distinct()

    def get_images(self):
        """Returns all images of the product, including the main image.
        """
        cache_key = "%s-tecdoc-product-%s-images" % (CACHE_PREFIX, self.id)
        images = cache.get(cache_key)

        if images is not None:
            return images

        images = self.images.all()
        cache.set(cache_key, images)

        return images

    def get_image(self):
        """Returns the first image (the main image) of the product.
        """
        try:
            return self.get_images()[0]
        except IndexError:
            return None

    def get_sub_images(self):
        """Returns all images of the product, except the main image.
        """
        return self.get_images()[1:]


class GroupManager(TecdocManagerWithDes):
    def get_queryset(self, *args, **kwargs):
        query = super(GroupManager, self).get_queryset(*args, **kwargs)
        query = query.filter(designation__lang=tdsettings.LANG_ID,
                             standard__lang=tdsettings.LANG_ID,
                             assembly__lang=tdsettings.LANG_ID,
                             intended__lang=tdsettings.LANG_ID)
        return query.select_related('designation__description',
                                    'standard__description',
                                    'assembly__description',
                                    'intended__description')


class Group(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='GA_ID')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='GA_DES_ID')

    standard = models.ForeignKey('tecdoc.Designation',
                                 verbose_name=u'Стандарт',
                                 db_column='GA_DES_ID_STANDARD',
                                 related_name='+')

    assembly = models.ForeignKey('tecdoc.Designation',
                                 verbose_name=u'Где устанавливается',
                                 db_column='GA_DES_ID_ASSEMBLY',
                                 related_name='+')

    intended = models.ForeignKey('tecdoc.Designation',
                                 verbose_name=u'Во что входит',
                                 db_column='GA_DES_ID_INTENDED',
                                 related_name='+')

    sections = models.ManyToManyField('tecdoc.CarSection',
                                      verbose_name=u'Категории',
                                      through='tecdoc.SectionGroup',
                                      related_name='groups')

    objects = GroupManager()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'generic_articles'

    def full_title(self):
        return u'%s - %s - %s - %s' % (self.designation,
                                       self.standard,
                                       self.assembly,
                                       self.intended)

    def __str__(self):
        # return ""
        # import pdb; pdb.set_trace()
        return str(self.designation)


class PartDescription(TecdocModel):
    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='AIN_ART_ID')

    group = models.ForeignKey(Group, verbose_name=u'Группа запчастей',
                              db_column='AIN_GA_ID')

    text = models.ForeignKey('tecdoc.TextModule',
                             verbose_name=u'Обозначение',
                             db_column='AIN_TMO_ID')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'article_info'


class SectionGroup(TecdocModel):
    car_section = models.ForeignKey('tecdoc.CarSection',
                                    verbose_name=u'Категория',
                                    db_column='LGS_STR_ID')

    group = models.ForeignKey(Group,
                              verbose_name=u'Группа запчатей',
                              db_column='LGS_GA_ID')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'link_ga_str'


class PartGroup(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='LA_ID')

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LA_ART_ID')

    group = models.ForeignKey(Group,
                              verbose_name=u'Группа запчастей',
                              db_column='LA_GA_ID')

    sorting = models.IntegerField(u'Порядок', db_column='LA_SORT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'link_art'


# Redundant Model
class PartGroupSupplier(TecdocModel):
    # part and group primary key
    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LAG_ART_ID')

    group = models.ForeignKey(Group, verbose_name=u'Группа запчастей',
                              db_column='LAG_GA_ID')

    supplier = models.ForeignKey('tecdoc.Supplier',
                                 verbose_name=u'Поставщик',
                                 db_column='LAG_SUP_ID')

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'link_art_ga'


class PartTypeGroupSupplier(TecdocModel):
    # car_type, part, group and sort are primary key
    car_type = models.ForeignKey(CarType,
                                 verbose_name=u'Модификация модели',
                                 db_column='LAT_TYP_ID',
                                 primary_key=True
                                 )

    part = models.ForeignKey(PartGroup, verbose_name=u'Запчасть',
                             db_column='LAT_LA_ID')

    # group = models.ForeignKey(Group, verbose_name=u'Группа Запчастей',
    #                           db_column='LAT_GA_ID')

    supplier = models.ForeignKey('tecdoc.Supplier', verbose_name=u'Поставщик',
                                 db_column='LAT_SUP_ID')

    sorting = models.IntegerField(u'Порядок', db_column='LAT_SORT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'link_la_typ'


class PartAnalog(TecdocModel):
    KIND = ((1, u'не оригинал'),
            (2, u'торговый'),
            (3, u'оригинал'),
            (4, u'номер замен'),
            (5, u'штрих-код'),
            )

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             primary_key=True,
                             db_column='ARL_ART_ID',
                             related_name='analogs')

    number = models.CharField(u'Номер', max_length=105,
                              db_column='ARL_DISPLAY_NR',
                              )

    # derived from number
    search_number = models.CharField(u'Номер для поиска', max_length=105,
                                     db_column='ARL_SEARCH_NUMBER',
                                     )

    kind = models.IntegerField(u'Тип', choices=KIND,
                               db_column='ARL_KIND')

    brand = models.ForeignKey('tecdoc.Brand',
                              verbose_name=u'Производитель',
                              null=True, blank=True,
                              db_column='ARL_BRA_ID')

    sorting = models.IntegerField(u'Порядок', db_column='ARL_SORT')

    def __str__(self):
        return u'%s %s %s' % (self.get_kind_display(), self.get_manufacturer(), self.get_sku())

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'art_lookup'

    def get_manufacturer(self):
        if self.kind in ['3', '4']:
            return self.brand
        else:
            return self.part.supplier

    def get_sku(self):
        return self.search_number
        # if self.kind in ['2', '3']:
        #     return self.number
        # else:
        #     return self.part.sku


class PartList(TecdocModel):
    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='ALI_ART_ID')

    inner_part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                                   db_column='ALI_ART_ID_COMPONENT',
                                   related_name='inner_parts')

    group = models.ForeignKey(Group, verbose_name=u'Группа Запчастей',
                              db_column='ALI_GA_ID')

    quantity = models.IntegerField(u'Количество',
                                   db_column='ALI_QUANTITY')

    sorting = models.IntegerField(u'Порядок', db_column='ALI_SORT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'article_lists'


# TODO
class PartListCriteria(TecdocModel):
    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'article_list_criteria'


class CountryProperty(TecdocModel):
    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='ACS_ART_ID',
                             related_name='properties')

    pack = models.ForeignKey('tecdoc.Designation', verbose_name=u'Упаковка',
                             db_column='ACS_PACK_UNIT',
                             related_name='+')

    quantity = models.ForeignKey('tecdoc.Designation',
                                 verbose_name=u'Количество',
                                 db_column='ACS_QUANTITY_PER_UNIT',
                                 related_name='+')

    status = models.ForeignKey('tecdoc.Designation',
                               verbose_name=u'Статус',
                               db_column='ACS_KV_STATUS_DES_ID',
                               related_name='+')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'art_country_specifics'
