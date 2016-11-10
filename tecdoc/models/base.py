from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings


class TecdocManager(models.Manager):
    # pass
    def getquery_set(self, *args, **kwargs):
        return super(TecdocManager, self).get_queryset(*args, **kwargs).using(tdsettings.DATABASE)


class TecdocModel(models.Model):
    pass

    class Meta:
        abstract = True
        managed = False
        app_label = 'tecdoc'


class Description(TecdocModel):
    id = models.AutoField('Ид', primary_key=True, db_column='TEX_ID')
    text = models.TextField('Текст', db_column='TEX_TEXT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'des_texts'
        verbose_name = 'Текст обозначения'

    def __str__(self):
        return self.text


class Text(TecdocModel):
    id = models.AutoField('Ид', primary_key=True, db_column='TMT_ID')

    text = models.TextField('Текст', db_column='TMT_TEXT', null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'text_module_texts'

    def __str__(self):
        return self.text


class Language(TecdocModel):
    id = models.AutoField('Ид', primary_key=True, db_column='LNG_ID')

    designation = models.ForeignKey('tecdoc.Designation', verbose_name='Обозначение', db_column='LNG_DES_ID',
                                    blank=True, null=True)
    iso_code = models.CharField('Код ISO2', max_length=6, db_column='LNG_ISO2', blank=True, null=True)

    codepage = models.CharField('Кодировка', max_length=30, db_column='LNG_CODEPAGE', blank=True, null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'languages'


class DesignationManager(TecdocManager):
    use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        return super(DesignationManager, self).get_queryset(*args, **kwargs).filter(
            lang=tdsettings.LANG_ID).select_related('description')


class DesignationBase(TecdocModel):
    objects = DesignationManager()

    class Meta(TecdocModel.Meta):
        abstract = True

    def __str__(self):
        return self.description.text or '-'


class TextModule(DesignationBase):
    # XXX not a key
    id = models.AutoField('Ид', primary_key=True, db_column='TMO_ID')

    lang = models.ForeignKey(Language, verbose_name='Язык', related_name='+', db_column='TMO_LNG_ID')

    description = models.ForeignKey(Text, verbose_name='Описание', db_column='TMO_TMT_ID')

    class Meta(DesignationBase.Meta):
        db_table = tdsettings.DB_PREFIX + 'text_modules'


class TecdocManagerWithDes(TecdocManager):
    def get_queryset(self, *args, **kwargs):
        query = super(TecdocManagerWithDes, self).get_queryset(*args, **kwargs)
        query = query.filter(designation__lang=tdsettings.LANG_ID)
        return query.select_related('designation__description')


class Designation(DesignationBase):
    # XXX not a key
    id = models.AutoField('Ид', primary_key=True, db_column='DES_ID')

    lang = models.ForeignKey(Language, verbose_name='Язык', related_name='+', db_column='DES_LNG_ID')

    description = models.ForeignKey(Description, verbose_name='Описание', db_column='DES_TEX_ID')

    def __lt__(self, other):
        return self.description.text.upper() <= other.description.text.upper()

    class Meta(DesignationBase.Meta):
        db_table = tdsettings.DB_PREFIX + 'designations'


class CountryDesignation(DesignationBase):
    # XXX not a key
    id = models.AutoField('Ид', primary_key=True, db_column='CDS_ID')

    lang = models.ForeignKey(Language, verbose_name='Язык', db_column='CDS_LNG_ID')

    description = models.ForeignKey(Description, verbose_name='Описание', db_column='CDS_TEX_ID')

    class Meta(DesignationBase.Meta):
        db_table = tdsettings.DB_PREFIX + 'country_designations'
