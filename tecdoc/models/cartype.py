from django.db import models

from tecdoc.models.base import CountryDesignation, DesignationManager


class CarType(models.Model):
    id = models.AutoField(db_column='TYP_ID', primary_key=True, verbose_name='Ид')
    designation = models.ForeignKey(CountryDesignation, db_column='TYP_CDS_ID', verbose_name='Обозначение')
    full_designation = models.ForeignKey(CountryDesignation, db_column='TYP_MMT_CDS_ID', verbose_name='Полное обозначение')
