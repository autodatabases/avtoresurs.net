import re
from django.db import models

from tecdoc.apps import TecdocConfig as tdsettings


class TecdocManager(models.Manager):
    def get_queryset(self):
        qs = super(TecdocManager, self).get_queryset()
        qs = qs.filter(passenger_car='True', can_display='True')
        return qs


class TecdocLanguageManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        return super(TecdocLanguageManager, self). \
            get_queryset(*args, **kwargs). \
            filter(designation__language=tdsettings.LANG_ID).select_related('designation__description')


class TecdocLanguageDesManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        query = super(TecdocLanguageDesManager, self).get_queryset(*args, **kwargs)
        query = query.filter(designation__language=tdsettings.LANG_ID)
        return query.select_related('designation__description')


class Description(models.Model):
    id = models.AutoField(db_column='TEX_ID', primary_key=True, verbose_name='Ид')
    text = models.CharField(db_column='TEX_TEXT', blank=True, null=True, verbose_name='Текст', max_length=1200)

    def __str__(self):
        return self.text

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
    description = models.ForeignKey(Description, db_column='CDS_TEX_ID', verbose_name='Описание')

    def __str__(self):
        return self.description.text or u'-'

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'country_designations'


class Designation(models.Model):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='DES_ID')

    language = models.ForeignKey(Language,
                                 verbose_name=u'Язык',
                                 related_name='+',
                                 db_column='DES_LNG_ID')

    description = models.ForeignKey(Description,
                                    verbose_name=u'Описание',
                                    db_column='DES_TEX_ID')

    def __str__(self):
        return self.description.text or u'-'

    def __lt__(self, other):
        return self.description.text.upper() <= other.description.text.upper()

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'designations'
