from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings


class Description(models.Model):
    id = models.AutoField(db_column='TEX_ID', primary_key=True, verbose_name='Ид')
    text = models.CharField(db_column='TEX_TEXT', blank=True, null=True, verbose_name='Текст')

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'des_texts'


class Language(models.Model):
    id = models.AutoField(db_column='LNG_ID', primary_key=True, verbose_name='Ид')
    designation = models.ForeignKey(Description, db_column='LNG_DES_ID', blank=True, null=True,
                                    verbose_name=u'Обозначение')
    iso_code = models.CharField(db_column='LNG_ISO2', max_length=6, blank=True, null=True, verbose_name='Код ISO2')
    codepage = models.CharField(db_column='LNG_CODEPAGE', max_length=30, blank=True, null=True,
                                verbose_name='Кодировка')

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'languages'


class CountryDesignation(models.Model):
    id = models.AutoField(db_column='CDS_ID', primary_key=True, verbose_name='Ид')
    language = models.ForeignKey(Language, db_column='CDS_LNG_ID', verbose_name='Язык')
    cds_text_id = models.ForeignKey(Designation, db_column='CDS_TEX_ID', verbose_name='Описание')


class Designation(models.Model):
    pass
