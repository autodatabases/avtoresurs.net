from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings


class Manufacturer(models.Model):
    YESNO = (
        ('0', 'Нет'),
        ('1', 'Да'),
    )

    id = models.AutoField(db_column='MFA_ID', primary_key=True, verbose_name='Ид')
    title = models.CharField(db_column='MFA_BRAND', max_length=60, blank=True, null=True, verbose_name='Название')
    code = models.CharField(db_column='MFA_MFC_CODE', max_length=30, blank=True, null=True, verbose_name='Код')
    for_car = models.SmallIntegerField(db_column='MFA_PC_MFC', choices=YESNO, blank=True, null=True,
                                       verbose_name='Для легковых')
    for_truck = models.SmallIntegerField(db_column='MFA_CV_MFC', choices=YESNO, blank=True, null=True,
                                         verbose_name='Для грузовых')

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'manufacturers'
        ordering = ['title']
        verbose_name = 'Производитель автомобилей'
        verbose_name_plural = 'Производители автомобилей'

    def __str__(self):
        return self.title.upper()


