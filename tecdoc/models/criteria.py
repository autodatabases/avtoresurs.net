from django.db import models

from tecdoc.apps import TecdocConfig as tdsettings

from tecdoc.models import Designation, TecdocLanguageDesManager


class CriteriaManager(TecdocLanguageDesManager):
    use_for_related_fields = True
    def get_queryset(self, *args, **kwargs):
        query = super(CriteriaManager, self).get_queryset(*args, **kwargs)
        query = query.filter(short_designation__language=tdsettings.LANG_ID, unit__language=tdsettings.LANG_ID)
        return query.select_related('designation__description',
                                    'short_designation__description',
                                    'unit__description')


class Criteria(models.Model):
    id = models.AutoField(db_column='CRI_ID', primary_key=True, verbose_name='Ид')
    designation = models.ForeignKey('tecdoc.Designation', db_column='CRI_DES_ID', related_name='+')
    short_designation = models.ForeignKey('tecdoc.Designation', db_column='CRI_SHORT_DES_ID', blank=True, null=True,
                                          related_name='+')
    unit = models.ForeignKey('tecdoc.Designation', db_column='CRI_UNIT_DES_ID', blank=True, null=True,
                             related_name='+')
    type = models.CharField(db_column='CRI_TYPE', max_length=1)
    cri_kt_id = models.IntegerField(db_column='CRI_KT_ID', blank=True, null=True)
    is_interval = models.BooleanField(u'Интервальный', db_column='CRI_IS_INTERVAL')
    cri_successor = models.IntegerField(db_column='CRI_SUCCESSOR', blank=True, null=True)

    objects = CriteriaManager()

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'criteria'

    def get_unit(self):
        return self.unit if self.unit_id else ''

    def get_display_value(self):
        return self.short_designation.description.text or self.designation.description.text

    def __str__(self):
        return self.get_display_value()


class PartCriteriaManager(TecdocLanguageDesManager):
    def get_queryset(self, *args, **kwargs):
        query = super(PartCriteriaManager, self).get_queryset(*args, **kwargs)
        query = query.filter(criteria__short_designation__language=tdsettings.LANG_ID,
                             criteria__designation__language=tdsettings.LANG_ID)
        return query.select_related('designation__description',
                                    'criteria__short_designation__description',
                                    'criteria__designation__description')


class PartCriteria(models.Model):
    part = models.OneToOneField('tecdoc.Part', db_column='ACR_ART_ID', primary_key=True, verbose_name='Ид')
    acr_ga_id = models.IntegerField(db_column='ACR_GA_ID')
    sort = models.IntegerField(db_column='ACR_SORT')
    criteria = models.ForeignKey(Criteria, db_column='ACR_CRI_ID')
    value = models.CharField(db_column='ACR_VALUE', blank=True, null=True, max_length=60)
    designation = models.ForeignKey('tecdoc.Designation', db_column='ACR_KV_DES_ID', blank=True, null=True,
                                    related_name='+')
    display = models.IntegerField(db_column='ACR_DISPLAY', blank=True, null=True)

    def __str__(self):
        return '%s: %s' % (self.criteria, self.value)

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'article_criteria'
