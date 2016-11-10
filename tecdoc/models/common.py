from django.db import models

from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManagerWithDes)


class Country(TecdocModel):
    id = models.AutoField('Ид', primary_key=True, db_column='COU_ID')

    iso_code = models.CharField('Код ISO2', max_length=6, db_column='COU_ISO2', blank=True, null=True)

    designation = models.ForeignKey('tecdoc.Designation', verbose_name='Обозначение', db_column='COU_DES_ID')

    currency_code = models.CharField('Код Валюты', max_length=9, db_column='COU_CURRENCY_CODE', blank=True, null=True)

    objects = TecdocManagerWithDes()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'countries'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Brand(TecdocModel):
    id = models.AutoField('Ид', primary_key=True, db_column='BRA_ID')

    title = models.CharField('Название', max_length=60, db_column='BRA_BRAND', blank=True, null=True)

    code = models.CharField('Название', max_length=30, db_column='BRA_MFC_CODE', blank=True, null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'brands'
        ordering = ['title']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.title.upper()
        # return self.title.capitalize()


class Manufacturer(TecdocModel):
    YESNO = (('0', 'Нет'),
             ('1', 'Да'),
             )

    id = models.AutoField('Ид', primary_key=True, db_column='MFA_ID')

    title = models.CharField('Название', max_length=60, db_column='MFA_BRAND', blank=True, null=True)

    code = models.CharField('Код', max_length=30, db_column='MFA_MFC_CODE', blank=True, null=True)

    for_car = models.SmallIntegerField('Для легковых', db_column='MFA_PC_MFC', choices=YESNO, blank=True, null=True)

    for_truck = models.SmallIntegerField('Для грузовых', db_column='MFA_CV_MFC', choices=YESNO, blank=True, null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'manufacturers'
        ordering = ['title']
        verbose_name = 'Производитель автомобилей'
        verbose_name_plural = 'Производители автомобилей'

    __str__ = Brand.__str__
