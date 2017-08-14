from django.db import models

from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models import Language


class Supplier(models.Model):
    id = models.BigIntegerField(db_column='id', primary_key=True)
    dataversion = models.CharField(db_column='dataversion', max_length=512, blank=True, null=True)
    title = models.CharField(db_column='description', max_length=512, blank=True, null=True, verbose_name='Название брэнда')
    matchcode = models.CharField(db_column='matchcode', max_length=512, blank=True, null=True)
    nbrofarticles = models.CharField(db_column='nbrofarticles', max_length=512, blank=True, null=True)
    hasnewversionarticles = models.CharField(db_column='hasnewversionarticles', max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'suppliers'
        ordering = ['title']
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'

    def __str__(self):
        return self.title

        # class Supplier(models.Model):
        #     id = models.AutoField(db_column='SUP_ID', primary_key=True, verbose_name='Ид')
        #     title = models.CharField(db_column='SUP_BRAND', max_length=60, blank=True, null=True, verbose_name='Название')
        #
        #     class Meta:
        #         db_table = tdsettings.DB_PREFIX + 'suppliers'
        #         verbose_name = u'Производитель запчастей'
        #         verbose_name_plural = u'Производители запчастей'
        #
        #     def __str__(self):
        #         return self.title

        # def get_country(self):
        #     return self.addresses.filter(type=1,
        #                                  country_flag=0).get().country_postal

# class SupplierLogo(models.Model):
#     id = models.AutoField(primary_key=True, db_column='SLO_ID', verbose_name='Ид')
#     supplier = models.ForeignKey(Supplier, db_column='SLO_SUP_ID', verbose_name='Поставщик', )
#     language = models.ForeignKey(Language, db_column='SLO_LNG_ID', verbose_name='Язык')
#
#     class Meta:
#         db_table = tdsettings.DB_PREFIX + 'supplier_logos'


# class SupplierAddress(models.Model):
#     # XXX not a primary key
#     supplier = models.ForeignKey(Supplier, db_column='SAD_SUP_ID', primary_key=True, verbose_name=u'Поставщик',
#                                  related_name='addresses')
#     type = models.IntegerField(db_column='SAD_TYPE_OF_ADDRESS', verbose_name='Тип')
#     # needed with value 0
#     country_flag = models.IntegerField(db_column='SAD_COU_ID', verbose_name='Страна')
#     country_postal = models.ForeignKey('tecdoc.Country',
#                                        verbose_name=u'Почтовый адресс. Страна',
#                                        db_column='SAD_COU_ID_POSTAL',
#                                        related_name="addresses")
#
#     class Meta(TecdocModel.Meta):
#         db_table = tdsettings.DB_PREFIX + 'supplier_addresses'
