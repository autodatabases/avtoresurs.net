from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models import TecdocManager

YES = 'True'
NO = 'False'
CAN_DISPLAY = (
    (YES, 'True'),
    (NO, 'False')
)


class ManufacturerManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        qs = super(ManufacturerManager, self).get_queryset()
        qs = qs.filter(can_display='True', passenger_car='True')
        return qs

    def all(self):
        qs = super(ManufacturerManager, self).get_queryset()
        qs = qs.filter(passenger_car='True')
        return qs


class Manufacturer(models.Model):
    objects = ManufacturerManager()

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'manufacturers'
        ordering = ['title']
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        manager_inheritance_from_future = True
        # base_manager_name = 'manufacturer'

    id = models.BigIntegerField(db_column='id', primary_key=True, verbose_name='Ид')
    can_display = models.CharField(
        db_column='canbedisplayed',
        max_length=512,
        blank=True,
        null=True,
        choices=CAN_DISPLAY,
        default=YES,
    )
    title = models.CharField(db_column='description', max_length=512, blank=True, null=True)
    description = models.CharField(db_column='fulldescription', max_length=512, blank=True, null=True)
    link = models.CharField(db_column='haslink', max_length=512, blank=True, null=True)
    axle = models.CharField(db_column='isaxle', max_length=512, blank=True, null=True)
    commercial_vehicle = models.CharField(db_column='iscommercialvehicle', max_length=512, blank=True, null=True)
    engine = models.CharField(db_column='isengine', max_length=512, blank=True, null=True)
    motorbike = models.CharField(db_column='ismotorbike', max_length=512, blank=True, null=True)
    passenger_car = models.CharField(db_column='ispassengercar', max_length=512, blank=True, null=True)
    transporter = models.CharField(db_column='istransporter', max_length=512, blank=True, null=True)
    vgl = models.CharField(db_column='isvgl', max_length=512, blank=True, null=True)
    match_code = models.CharField(db_column='matchcode', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.title.upper()

# class Manufacturer(models.Model):
#     YESNO = (
#         ('0', 'Нет'),
#         ('1', 'Да'),
#     )
#
#     id = models.AutoField(db_column='MFA_ID', primary_key=True, verbose_name='Ид')
#     canbedisplayed = models.BooleanField(db_column='canbedisplayed')
#     title = models.CharField(db_column='description', max_length=512, blank=True, null=True, verbose_name='Название')
#     full_title = models.CharField(db_column='fulldescription', max_length=512, blank=True, null=True, verbose_name='Полное название')
#
#     for_car = models.SmallIntegerField(db_column='MFA_PC_MFC', choices=YESNO, blank=True, null=True,
#                                        verbose_name='Для легковых')
#     for_truck = models.SmallIntegerField(db_column='MFA_CV_MFC', choices=YESNO, blank=True, null=True,
#                                          verbose_name='Для грузовых')
#
#     class Meta:
#         db_table = tdsettings.DB_PREFIX + 'manufacturers'
#         ordering = ['title']
#         verbose_name = 'Производитель автомобилей'
#         verbose_name_plural = 'Производители автомобилей'
#
#
