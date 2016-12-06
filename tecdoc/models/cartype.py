from django.db import models

from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models import Manufacturer, CountryDesignation, CarModel, Designation, \
    TecdocLanguageDesManager


class CarTypeManager(TecdocLanguageDesManager):
    use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        return (super(CarTypeManager, self).get_queryset(*args, **kwargs)
                .filter(model__designation__language=tdsettings.LANG_ID,
                        full_designation__language=tdsettings.LANG_ID,
                        drive_des__language=tdsettings.LANG_ID,
                        body_des__language=tdsettings.LANG_ID,
                        designation__description__text__isnull=False)
                .select_related('model__manufacturer',
                                'model__designation__description',
                                'full_designation__description',
                                'designation__description',
                                'drive_des__description',
                                'body_des__description')
                .prefetch_related('engines')
                )


class CarType(models.Model):
    id = models.IntegerField(db_column='TYP_ID', primary_key=True, verbose_name='Ид')
    designation = models.ForeignKey(CountryDesignation, db_column='TYP_CDS_ID', blank=True, null=True,
                                    verbose_name='Обозначение')
    full_designation = models.ForeignKey(CountryDesignation, db_column='TYP_MMT_CDS_ID', blank=True, null=True,
                                         verbose_name='Полное обозначение', related_name='+')
    model = models.ForeignKey(CarModel, db_column='TYP_MOD_ID', verbose_name='Модель машины',
                              related_name='cartypes')
    sorting = models.IntegerField(db_column='TYP_SORT', verbose_name='Сортировка')
    production_start = models.IntegerField(db_column='TYP_PCON_START', blank=True, null=True,
                                           verbose_name='Начало производства')
    production_end = models.IntegerField(db_column='TYP_PCON_END', blank=True, null=True,
                                         verbose_name='Окончание производства')
    power_kw_from = models.IntegerField(db_column='TYP_KW_FROM', blank=True, null=True,
                                        verbose_name='Мощность двигателя (кВт): ОТ')
    power_kw_upto = models.IntegerField(db_column='TYP_KW_UPTO', blank=True, null=True,
                                        verbose_name='Мощность двигателя (кВт): До')
    power_hp_from = models.IntegerField(db_column='TYP_HP_FROM', blank=True, null=True,
                                        verbose_name='Мощность двигателя (л.с.): ОТ')
    power_hp_upto = models.IntegerField(db_column='TYP_HP_UPTO', blank=True, null=True,
                                        verbose_name='Мощность двигателя (л.с.): До')
    eng_volume = models.IntegerField(db_column='TYP_CCM', blank=True, null=True,
                                     verbose_name='Объём двигателя (куб.см)')
    cylinders = models.SmallIntegerField(db_column='TYP_CYLINDERS', blank=True, null=True,
                                         verbose_name='Количество цилиндров')
    doors = models.SmallIntegerField(db_column='TYP_DOORS', blank=True, null=True, verbose_name='Количество дверей')
    tank = models.SmallIntegerField(db_column='TYP_TANK', blank=True, null=True, verbose_name='Тип поплива')
    engines = models.ManyToManyField('tecdoc.Engine', verbose_name=u'Двигатели', through='tecdoc.CarTypeEngine',
                                     related_name='cartypes')
    engine_des = models.ForeignKey(Designation, db_column='TYP_KV_ENGINE_DES_ID', related_name='+')
    body_des = models.ForeignKey(Designation, db_column='TYP_KV_BODY_DES_ID', related_name='+')
    fuel_des = models.ForeignKey(Designation, db_column='TYP_KV_FUEL_DES_ID', blank=True, null=True, related_name='+')
    drive_des = models.ForeignKey(Designation, db_column='TYP_KV_DRIVE_DES_ID', blank=True, null=True, related_name='+')

    typ_kv_voltage_des_id = models.IntegerField(db_column='TYP_KV_VOLTAGE_DES_ID', blank=True, null=True)
    typ_kv_abs_des_id = models.IntegerField(db_column='TYP_KV_ABS_DES_ID', blank=True, null=True)
    typ_kv_asr_des_id = models.IntegerField(db_column='TYP_KV_ASR_DES_ID', blank=True, null=True)

    typ_kv_brake_type_des_id = models.IntegerField(db_column='TYP_KV_BRAKE_TYPE_DES_ID', blank=True, null=True)
    typ_kv_brake_syst_des_id = models.IntegerField(db_column='TYP_KV_BRAKE_SYST_DES_ID', blank=True, null=True)

    typ_kv_catalyst_des_id = models.IntegerField(db_column='TYP_KV_CATALYST_DES_ID', blank=True, null=True)

    typ_kv_steering_des_id = models.IntegerField(db_column='TYP_KV_STEERING_DES_ID', blank=True, null=True)
    typ_kv_steering_side_des_id = models.IntegerField(db_column='TYP_KV_STEERING_SIDE_DES_ID', blank=True, null=True)
    typ_max_weight = models.DecimalField(db_column='TYP_MAX_WEIGHT', max_digits=5, decimal_places=0, blank=True,
                                         null=True)
    typ_kv_model_des_id = models.IntegerField(db_column='TYP_KV_MODEL_DES_ID', blank=True, null=True)
    typ_kv_axle_des_id = models.IntegerField(db_column='TYP_KV_AXLE_DES_ID', blank=True, null=True)
    typ_ccm_tax = models.IntegerField(db_column='TYP_CCM_TAX', blank=True, null=True)
    typ_litres = models.DecimalField(db_column='TYP_LITRES', max_digits=6, decimal_places=0, blank=True, null=True)
    typ_kv_trans_des_id = models.IntegerField(db_column='TYP_KV_TRANS_DES_ID', blank=True, null=True)
    typ_kv_fuel_supply_des_id = models.IntegerField(db_column='TYP_KV_FUEL_SUPPLY_DES_ID', blank=True, null=True)
    typ_valves = models.SmallIntegerField(db_column='TYP_VALVES', blank=True, null=True)
    typ_rt_exists = models.SmallIntegerField(db_column='TYP_RT_EXISTS', blank=True, null=True)

    objects = CarTypeManager()

    class Meta:
        managed = False
        db_table = tdsettings.DB_PREFIX + 'types'
        verbose_name = 'Тип модели автомобиля'
        verbose_name_plural = 'Типы модели автомобиля'
        ordering = ['sorting', 'production_start']

    def __str__(self):
        return '%s (%s-%s)' % (self.full_designation, self.get_production_start(), self.get_production_end())

    def get_production_start(self):
        start = divmod(self.production_start, 100)
        return '%02d/%d' % (start[1], start[0])

    def get_production_end(self):
        if self.production_end is None:
            return 'н.д.'
        end = divmod(self.production_end, 100)
        return '%02d/%d' % (end[1], end[0])


class EngineManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (super(EngineManager, self).get_queryset(*args, **kwargs)
                .filter(fuel_des__language=tdsettings.LANG_ID)
                .select_related('manufacturer',
                                'fuel_des__description')
                )


class Engine(models.Model):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='ENG_ID')

    manufacturer = models.ForeignKey(Manufacturer,
                                     verbose_name=u'Производитель',
                                     db_column='ENG_MFA_ID')

    code = models.CharField(u'Код', max_length=180, db_column='ENG_CODE')

    production_start = models.IntegerField(u'Начало производства',
                                           db_column='ENG_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                         db_column='ENG_PCON_END')

    power_kw_from = models.IntegerField(u'Мощность двигателя (кВт): ОТ',
                                        db_column='ENG_KW_FROM',
                                        blank=True, null=True)
    power_kw_upto = models.IntegerField(u'Мощность двигателя (кВт): До',
                                        db_column='ENG_KW_UPTO',
                                        blank=True, null=True)
    power_hp_from = models.IntegerField(u'Мощность двигателя (л.с.): ОТ',
                                        db_column='ENG_HP_FROM',
                                        blank=True, null=True)
    power_hp_upto = models.IntegerField(u'Мощность двигателя (л.с.): До',
                                        db_column='ENG_HP_UPTO',
                                        blank=True, null=True)

    fuel_des = models.ForeignKey('tecdoc.Designation',
                                 verbose_name=u'Кузов',
                                 db_column='ENG_KV_FUEL_TYPE_DES_ID',
                                 related_name='+'
                                 )

    objects = EngineManager()

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'engines'


class CarTypeEngine(models.Model):
    car_type = models.OneToOneField(CarType, primary_key=True,
                                 verbose_name=u'Модификация модели',
                                 db_column='LTE_TYP_ID')

    engine = models.ForeignKey(Engine,
                               verbose_name=u'Двигатель',
                               db_column='LTE_ENG_ID')

    production_start = models.IntegerField(u'Начало производства',
                                           db_column='LTE_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                         db_column='LTE_PCON_END')

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'link_typ_eng'
