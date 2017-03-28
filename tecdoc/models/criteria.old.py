# -*- coding: utf-8 -
from django.db import models

from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models import TecdocLanguageDesManager, TecdocLanguageManager


class CriteriaManager(TecdocLanguageDesManager):
    # use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        query = super(CriteriaManager, self).get_queryset(*args, **kwargs)
        query = query.filter(short_designation__language=tdsettings.LANG_ID, unit__language=tdsettings.LANG_ID)
        return query.select_related('designation__description',
                                    'short_designation__description',
                                    'unit__description')


class Criteria(models.Model):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='CRI_ID')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='CRI_DES_ID')

    short_designation = models.ForeignKey('tecdoc.Designation',
                                          verbose_name=u'Краткое Обозначение',
                                          db_column='CRI_SHORT_DES_ID',
                                          related_name='+',
                                          blank=True, null=True)

    unit = models.ForeignKey('tecdoc.Designation',
                             verbose_name=u'Упаковка',
                             db_column='CRI_UNIT_DES_ID',
                             related_name='+',
                             blank=True, null=True)

    '''
    A – (почти аналогичен N) критерий текстовый, однако он содержится в VALUE (ARTICLE_CRITERIA=>ACR_VALUE)
    B – информационный номер
    D – годы выпуска (почти аналогичен N) критерий текстовый, однако он содержится в VALUE (ARTICLE_CRITERIA=>ACR_VALUE)
    K – критерий текстовый, значение содержится в DES_ID (ARTICLE_CRITERIA=>ACR_KV_DES_ID),
        также для этих критериев нужно рассматривать значение KV_KT_ID
    N – критерий номерной, значение содержится в VALUE (ARTICLE_CRITERIA=>ACR_VALUE)
    V – критерий сам является значением. Поля DES_ID или VALUE пустые.
    '''
    type = models.CharField(u'Тип', max_length=1,
                            db_column='CRI_TYPE')

    is_interval = models.BooleanField(u'Интервальный',
                                      db_column='CRI_IS_INTERVAL')

    child = models.ForeignKey('self', verbose_name=u'Второй критерий',
                              db_column='CRI_SUCCESSOR',
                              related_name='parents')

    objects = CriteriaManager()

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'criteria'

    def __str__(self):
        return u'%s %s' % (self.designation or self.short_designation,
                           # self.get_unit(),
                           self.is_interval and u'Интервальный' or '')

    def get_unit(self):
        return self.unit if self.unit_id else ''

    def get_display_value(self):
        return self.short_designation or self.designation


class PartCriteriaManager(TecdocLanguageDesManager):
    # use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        query = super(PartCriteriaManager, self).get_queryset(*args, **kwargs)
        query = query.filter(criteria__short_designation__language=tdsettings.LANG_ID,
                             criteria__designation__language=tdsettings.LANG_ID)
        return query.select_related('designation__description',
                                    'criteria__short_designation__description',
                                    'criteria__designation__description')


class PartCriteria(models.Model):
    # XXX not a primary key
    part = models.OneToOneField('tecdoc.Part', verbose_name=u'Запчасть', db_column='ACR_ART_ID', primary_key=True)

    group = models.ForeignKey('tecdoc.Group', verbose_name=u'Группа Запчастей',
                              db_column='ACR_GA_ID')

    criteria = models.ForeignKey(Criteria, verbose_name=u'Запчасть',
                                 db_column='ACR_CRI_ID')

    value = models.CharField(u'Значение', max_length=60,
                             db_column='ACR_VALUE')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Описание',
                                    db_column='ACR_KV_DES_ID',
                                    blank=True, null=True)

    sorting = models.IntegerField(u'Порядок', db_column='ACR_SORT')

    display = models.BooleanField(u'Показывать',
                                  db_column='ACR_DISPLAY')

    # XXX join remove rows with ACR_KV_DES_ID==0
    objects = PartCriteriaManager()

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'article_criteria'
        ordering = ['sorting']

    def __str__(self):
        return u'%s: %s' % (self.criteria.get_display_value(),
                            self.get_value())

    def get_value(self):
        # criteria_type = self.criteria.type
        return self.value or self.designation
