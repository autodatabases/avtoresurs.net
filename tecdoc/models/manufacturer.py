from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings


class ManufacturerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ispassengercar=True, canbedisplayed=True)


class Manufacturer(models.Model):
    id = models.BigIntegerField(db_column='id', primary_key=True, verbose_name='Ид')
    canbedisplayed = models.CharField(db_column='canbedisplayed', max_length=512, blank=True, null=True)
    title = models.CharField(db_column='description', max_length=512, blank=True, null=True)
    fulldescription = models.CharField(db_column='fulldescription', max_length=512, blank=True, null=True)
    haslink = models.CharField(db_column='haslink', max_length=512, blank=True, null=True)
    isaxle = models.CharField(db_column='isaxle', max_length=512, blank=True, null=True)
    iscommercialvehicle = models.CharField(db_column='iscommercialvehicle', max_length=512, blank=True, null=True)
    iscvmanufacturerid = models.CharField(db_column='iscvmanufacturerid', max_length=512, blank=True, null=True)
    isengine = models.CharField(db_column='isengine', max_length=512, blank=True, null=True)
    ismotorbike = models.CharField(db_column='ismotorbike', max_length=512, blank=True, null=True)
    ispassengercar = models.CharField(db_column='ispassengercar', max_length=512, blank=True, null=True)
    istransporter = models.CharField(db_column='istransporter', max_length=512, blank=True, null=True)
    isvalidforcurrentcountry = models.CharField(db_column='isvalidforcurrentcountry', max_length=512, blank=True,
                                                null=True)
    isvgl = models.CharField(db_column='isvgl', max_length=512, blank=True, null=True)
    linkitemtype = models.CharField(db_column='linkitemtype', max_length=512, blank=True, null=True)
    matchcode = models.CharField(db_column='matchcode', max_length=512, blank=True, null=True)

    objects = ManufacturerManager()

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'manufacturers'
        ordering = ['title']
        verbose_name = 'Производитель автомобилей'
        verbose_name_plural = 'Производители автомобилей'

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
