from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models.base import CountryDesignation, TecdocLanguageManager
from tecdoc.models.manufacturer import Manufacturer


class CarModelManager(TecdocLanguageManager):
    use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        return super(CarModelManager, self). \
            get_queryset(*args, **kwargs). \
            select_related('manufacturer', 'designation__description'). \
            distinct()


class CarModel(models.Model):
    id = models.AutoField(db_column='MOD_ID', primary_key=True, verbose_name='Ид')
    manufacturer = models.ForeignKey(Manufacturer, db_column='MOD_MFA_ID', verbose_name='Производитель')
    production_start = models.IntegerField(db_column='MOD_PCON_START', verbose_name='Начало производства')
    production_end = models.IntegerField(db_column='MOD_PCON_END', verbose_name='Конец производства')
    designation = models.ForeignKey(CountryDesignation, db_column='MOD_CDS_ID', verbose_name='Обозначение')
    for_car = models.SmallIntegerField(db_column='MOD_PC', blank=True, null=True)
    for_truck = models.SmallIntegerField(db_column='MOD_CV', blank=True, null=True)

    objects = CarModelManager()

    def get_datestart(self):
        date_start = str(self.production_start)
        return "%s/%s" % (date_start[4:], date_start[:4])

    def get_dateend(self):
        date_end = self.production_end
        if date_end:
            date_end = str(date_end)
            return "%s/%s" % (date_end[4:], date_end[:4])
        else:
            return 'По настоящее время'

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'models'
        # ordering =
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'
