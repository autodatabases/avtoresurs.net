from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models import TecdocLanguageDesManager, Manufacturer, CountryDesignation


# class CarModelManager(TecdocLanguageDesManager):
#     use_for_related_fields = True
#
#     def get_queryset(self, *args, **kwargs):
#         return (super(CarModelManager, self)
#                 .get_queryset(*args, **kwargs)
#                 .select_related('manufacturer', 'designation__description')
#                 .order_by('designation__description__text')
#                 .distinct()
#                 )

class CarModelManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        qs = super(CarModelManager, self).get_queryset(*args, **kwargs)
        qs = qs.filter(passenger_car='True', can_display='True').select_related('manufacturer')
        return qs

class CarModel(models.Model):
    id = models.BigIntegerField(db_column='id', primary_key=True, verbose_name='Ид')
    can_display = models.CharField(db_column='canbedisplayed', max_length=512, blank=True, null=True)
    construction_interval = models.CharField(db_column='constructioninterval', max_length=512, blank=True, null=True)
    title = models.CharField(db_column='description', max_length=512, blank=True, null=True)
    description = models.CharField(db_column='fulldescription', max_length=512, blank=True, null=True)
    link = models.CharField(db_column='haslink', max_length=512, blank=True, null=True)
    axle = models.CharField(db_column='isaxle', max_length=512, blank=True, null=True)
    commercial_vehicle = models.CharField(db_column='iscommercialvehicle', max_length=512, blank=True, null=True)
    cv_manufacturer_id = models.CharField(db_column='iscvmanufacturerid', max_length=512, blank=True, null=True)
    engine = models.CharField(db_column='isengine', max_length=512, blank=True, null=True)
    motorbike = models.CharField(db_column='ismotorbike', max_length=512, blank=True, null=True)
    passenger_car = models.CharField(db_column='ispassengercar', max_length=512, blank=True, null=True)
    transporter = models.CharField(db_column='istransporter', max_length=512, blank=True, null=True)
    valid_for_current_country = models.CharField(db_column='isvalidforcurrentcountry', max_length=512, blank=True,
                                                null=True)
    link_item_type = models.CharField(db_column='linkitemtype', max_length=512, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, db_column='manufacturerid', verbose_name='Производитель')

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'models'
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'
        ordering = ['title']

# class CarModel(models.Model):
#     id = models.AutoField(db_column='MOD_ID', primary_key=True, verbose_name='Ид')
#     manufacturer = models.ForeignKey(Manufacturer, db_column='MOD_MFA_ID', verbose_name='Производитель')
#     production_start = models.IntegerField(db_column='MOD_PCON_START', verbose_name='Начало производства')
#     production_end = models.IntegerField(db_column='MOD_PCON_END', verbose_name='Конец производства')
#     designation = models.ForeignKey(CountryDesignation, db_column='MOD_CDS_ID', verbose_name='Обозначение')
#     for_car = models.SmallIntegerField(db_column='MOD_PC', blank=True, null=True)
#     for_truck = models.SmallIntegerField(db_column='MOD_CV', blank=True, null=True)
#
#     objects = CarModelManager()
#
#     def __str__(self):
#         return u'%s %s (%s-%s)' % (self.manufacturer,
#                                    self.designation,
#                                    self.production_start, self.production_end or u'н.д.')
#
#     def get_datestart(self):
#         date_start = str(self.production_start)
#         return "%s/%s" % (date_start[4:], date_start[:4])
#
#     def get_dateend(self):
#         date_end = self.production_end
#         if date_end:
#             date_end = str(date_end)
#             return "%s/%s" % (date_end[4:], date_end[:4])
#         else:
#             return 'По настоящее время'
#
#     class Meta:
#         db_table = tdsettings.DB_PREFIX + 'models'
#         # ordering = [self]
#         verbose_name = 'Модель автомобиля'
#         verbose_name_plural = 'Модели автомобилей'
