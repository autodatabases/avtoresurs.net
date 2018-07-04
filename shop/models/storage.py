from django.db import models


class Storage(models.Model):
    """ class for Storages """
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название склада')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='E-mail склада')
    active = models.BooleanField(default=True, verbose_name='Активен')
    file_name = models.CharField(max_length=100, default='News_auto_', null=True,
                                 verbose_name='Название файла склада на FTP')
    active_file_upload = models.BooleanField(default=False, verbose_name='Автоматическая загрузка')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')

    class Meta:
        ordering = ['pk']
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name
