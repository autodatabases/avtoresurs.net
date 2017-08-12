import os
import re
from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings
from tecdoc.models import Section, Designation, CarType, Supplier, TecdocLanguageDesManager, Manufacturer


class PartSection(models.Model):
    class Meta:
        db_table = 'article_links'

    supplier = models.ForeignKey('Supplier', db_column='supplierid', primary_key=True)
    part_description = models.ForeignKey('PartDescription', db_column='productid')
    linkage_type = models.BigIntegerField(db_column='linkagetypeid')
    car_type = models.ForeignKey('CarType', db_column='linkageid')
    part_number = models.CharField(db_column='datasupplierarticlenumber', max_length=128, blank=True,
                                   null=True)


class Part(models.Model):
    class Meta:
        managed = False
        db_table = 'articles'
        unique_together = ('supplier', 'part_number')

    supplier = models.ForeignKey(Supplier, db_column='supplierId', primary_key=True)  # Field name made lowercase.
    part_number = models.CharField(db_column='DataSupplierArticleNumber',
                                   max_length=128, primary_key=True)  # Field name made lowercase.
    clean_part_number = models.CharField(db_column='FoundString', max_length=128)  # Field name made lowercase.
    title = models.CharField(db_column='NormalizedDescription',
                             max_length=128)  # Field name made lowercase.

    state = models.CharField(db_column='ArticleStateDisplayTitle',
                             max_length=128)  # Field name made lowercase.
    state_title = models.CharField(db_column='ArticleStateDisplayValue',
                                   max_length=128)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=128)  # Field name made lowercase.
    flagaccessory = models.CharField(db_column='FlagAccessory', max_length=128)  # Field name made lowercase.
    flagmaterialcertification = models.CharField(db_column='FlagMaterialCertification',
                                                 max_length=128)  # Field name made lowercase.
    flagremanufactured = models.CharField(db_column='FlagRemanufactured',
                                          max_length=128)  # Field name made lowercase.
    flagselfservicepacking = models.CharField(db_column='FlagSelfServicePacking',
                                              max_length=128)  # Field name made lowercase.
    foundby = models.CharField(db_column='FoundBy', max_length=128)  # Field name made lowercase.

    hasaxle = models.CharField(db_column='HasAxle', max_length=128)  # Field name made lowercase.
    hascommercialvehicle = models.CharField(db_column='HasCommercialVehicle',
                                            max_length=128)  # Field name made lowercase.
    hascvmanuid = models.CharField(db_column='HasCVManuID', max_length=128)  # Field name made lowercase.
    hasengine = models.CharField(db_column='HasEngine', max_length=128)  # Field name made lowercase.
    haslinkitems = models.CharField(db_column='HasLinkitems', max_length=128)  # Field name made lowercase.
    hasmotorbike = models.CharField(db_column='HasMotorbike', max_length=128)  # Field name made lowercase.
    haspassengercar = models.CharField(db_column='HasPassengerCar', max_length=128)  # Field name made lowercase.
    isvalid = models.CharField(db_column='IsValid', max_length=128)  # Field name made lowercase.
    lotsize1 = models.CharField(db_column='LotSize1', max_length=128)  # Field name made lowercase.
    lotsize2 = models.CharField(db_column='LotSize2', max_length=128)  # Field name made lowercase.

    packingunit = models.CharField(db_column='PackingUnit', max_length=128)  # Field name made lowercase.
    quantityperpackingunit = models.CharField(db_column='QuantityPerPackingUnit',
                                              max_length=128)  # Field name made lowercase.

    def image(self):
        tecdoc_image_path = '/static/main/images/tecdoc/'
        image = Image.objects.filter(supplier=self.supplier, part_number=self.part_number).first()
        try:
            base, ext = os.path.splitext(image.picture)
            if ext == '.BMP':
                ext = ext.replace('BMP', 'jpg')
            return '%s%s%s' % (tecdoc_image_path, base, ext.lower())
        except Exception as exc:
            return '/static/main/images/no-image.png'


class PartAnalog(models.Model):
    supplier = models.ForeignKey(Supplier, db_column='supplierid')
    part_number = models.CharField(db_column='datasupplierarticlenumber', max_length=128, primary_key=True)
    isadditive = models.CharField(db_column='IsAdditive', max_length=128)  # Field name made lowercase.
    oenbr = models.CharField(db_column='OENbr', max_length=128)  # Field name made lowercase.
    manufacturer = models.ForeignKey(Manufacturer, db_column='manufacturerId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_oe'

    def __eq__(self, other):
        return self.supplier.title == other.supplier.title and self.part_number == other.part_number

    def __hash__(self):
        return hash(('part_number', self.part_number,
                     'supplier', self.supplier.title))


class PartCross(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, db_column='manufacturerId')  # Field name made lowercase.
    oenbr = models.CharField(primary_key=True, db_column='OENbr', max_length=128)  # Field name made lowercase.
    supplier = models.ForeignKey(Supplier, db_column='SupplierId')  # Field name made lowercase.
    part_number = models.CharField(db_column='PartsDataSupplierArticleNumber',
                                   max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_cross'


class PartTypeGroupSupplier(models.Model):
    car_type = models.ForeignKey(CarType, db_column='passangercarid')
    section = models.ForeignKey(Section, db_column='nodeid')
    part_description = models.ForeignKey('PartDescription', db_column='productid', primary_key=True)
    supplier = models.ForeignKey('Supplier', db_column='supplierid')

    class Meta:
        db_table = 'passanger_car_pds'
        unique_together = ('car_type', 'section', 'part_description', 'supplier')


class PartDescription(models.Model):
    id = models.BigIntegerField(db_column='id', primary_key=True)
    assemblygroupdescription = models.CharField(db_column='assemblygroupdescription', max_length=256)
    title = models.CharField(db_column='description', max_length=256)
    normalizeddescription = models.CharField(db_column='normalizeddescription', max_length=256)
    usagedescription = models.CharField(db_column='usagedescription', max_length=256)

    class Meta:
        db_table = 'passanger_car_prd'


class Image(models.Model):
    supplier = models.ForeignKey(Supplier, db_column='supplierId')  # Field name made lowercase.
    part_number = models.CharField(db_column='DataSupplierArticleNumber',
                                   max_length=128)  # Field name made lowercase.
    additionaldescription = models.CharField(db_column='AdditionalDescription',
                                             max_length=128)  # Field name made lowercase.
    title = models.CharField(db_column='Description', max_length=128, primary_key=True)  # Field name made lowercase.
    documentname = models.CharField(db_column='DocumentName', max_length=128)  # Field name made lowercase.
    documenttype = models.CharField(db_column='DocumentType', max_length=128)  # Field name made lowercase.
    normeddescriptionid = models.CharField(db_column='NormedDescriptionID',
                                           max_length=128)  # Field name made lowercase.
    picture = models.CharField(db_column='PictureName', max_length=128)  # Field name made lowercase.
    showimmediately = models.CharField(db_column='ShowImmediately', max_length=128)  # Field name made lowercase.

    class Meta:
        db_table = 'article_images'


class PartApplicability(models.Model):
    supplier = models.ForeignKey(Supplier, db_column='supplierId', primary_key=True)  # Field name made lowercase.
    part_number = models.CharField(db_column='DataSupplierArticleNumber',
                                   max_length=128)  # Field name made lowercase.
    linkage_type = models.CharField(db_column='linkageTypeId', max_length=128)  # Field name made lowercase.
    car_type = models.ForeignKey(CarType, db_column='linkageId')  # Field name made lowercase.

    class Meta:
        db_table = 'article_li'


class PartAttribute(models.Model):
    supplier = models.ForeignKey(Supplier, db_column='supplierid')
    part_number = models.CharField(db_column='datasupplierarticlenumber', max_length=128)
    id = models.BigIntegerField(db_column='id', primary_key=True)
    attributeinformationtype = models.CharField(db_column='attributeinformationtype', max_length=512)
    description = models.CharField(db_column='description', max_length=512, blank=True, null=True)
    displaytitle = models.CharField(db_column='displaytitle', max_length=512, blank=True, null=True)
    displayvalue = models.CharField(db_column='displayvalue', max_length=4096)

    class Meta:
        managed = False
        db_table = 'article_attributes'

class PartProduct:
    part_number = 0
    supplier = 0
    price = 0
    product_id = 0
    quatity = 0

    def __init__(self, supplier, part_number, price, quantity, product_id, title):
        self.supplier = supplier
        self.part_number = part_number
        self.price = price
        self.quantity = quantity
        self.product_id = product_id
        self.title = title

    def __gt__(self, other):
        return self.price > other.price




    # class PartManager(TecdocLanguageDesManager):
    #     use_for_related_fields = True
    #
    #     def get_queryset(self, *args, **kwargs):
    #         query = super(PartManager, self).get_queryset(*args, **kwargs)
    #         query = query.select_related('designation__description',
    #                                      'supplier')
    #
    #         query = query.prefetch_related('analogs', 'images', )
    #         # query = query.prefetch_related('analogs')
    #         return query


    # class Part(models.Model):
    #     id = models.AutoField(db_column='ART_ID', primary_key=True)
    #     sku = models.CharField(db_column='ART_ARTICLE_NR', max_length=66)
    #     supplier = models.ForeignKey(Supplier, db_column='ART_SUP_ID', blank=True, null=True)
    #     art_des_id = models.IntegerField(db_column='ART_DES_ID', blank=True, null=True)
    #     designation = models.ForeignKey(Designation, db_column='ART_COMPLETE_DES_ID', blank=True,
    #                                     null=True)
    #     # groups = models.ManyToManyField('tecdoc.Group', through='tecdoc.PartGroup', related_name='parts')
    #
    #     art_pack_selfservice = models.SmallIntegerField(db_column='ART_PACK_SELFSERVICE', blank=True,
    #                                                     null=True)
    #     art_material_mark = models.SmallIntegerField(db_column='ART_MATERIAL_MARK', blank=True,
    #                                                  null=True)
    #     art_replacement = models.SmallIntegerField(db_column='ART_REPLACEMENT', blank=True,
    #                                                null=True)
    #     art_accessory = models.SmallIntegerField(db_column='ART_ACCESSORY', blank=True,
    #                                              null=True)
    #     art_batch_size1 = models.IntegerField(db_column='ART_BATCH_SIZE1', blank=True,
    #                                           null=True)
    #     art_batch_size2 = models.IntegerField(db_column='ART_BATCH_SIZE2', blank=True,
    #                                           null=True)
    #     # car_type = models.ManyToManyField(CarType, through='tecdoc.PartTypeGroupSupplier')
    #     group = models.ManyToManyField('tecdoc.Group', through='tecdoc.PartGroup', verbose_name='Группа запчастей')
    #
    #     images = models.ManyToManyField('tecdoc.Image', verbose_name=u'Изображения', through='tecdoc.PartImage',
    #                                     related_name='parts')
    #
    #     # criteries = models.ManyToManyField('tecdoc.Criteria',
    #     #                                    verbose_name=u'Оговорки',
    #     #                                    through='tecdoc.PartCriteria',
    #     #                                    related_name='parts')
    #
    #     # pdfs = models.ManyToManyField(PdfFile, verbose_name=u'Инструкция', through=PartPdf, related_name='parts')
    #
    #     objects = PartManager()
    #
    #     def __str__(self):
    #         return "%s %s %s" % (self.designation.description.text, self.supplier, self.sku)
    #
    #     class Meta:
    #         managed = False
    #         db_table = tdsettings.DB_PREFIX + 'articles'


    # class Group(models.Model):
    #     id = models.AutoField(db_column='ga_id', primary_key=True, verbose_name='Ид')
    #     ga_nr = models.SmallIntegerField(db_column='ga_nr', blank='True', null='True')
    #     designation = models.ForeignKey(Designation, db_column='ga_des_id', verbose_name='Описание', related_name='+')
    #     standart = models.ForeignKey(Designation, db_column='ga_des_id_standard', verbose_name='Стандарт', related_name='+')
    #     assembly = models.ForeignKey(Designation, db_column='ga_des_id_assembly', verbose_name='Где устанавливается',
    #                                  related_name='+')
    #     intended = models.ForeignKey(Designation, db_column='ga_des_id_intended', verbose_name='Во что входит',
    #                                  related_name='+')
    #     ga_universal = models.SmallIntegerField(db_column='ga_universal')
    #     section = models.ManyToManyField(Section, through='tecdoc.SectionGroup', verbose_name='Категории')
    #
    #     #
    #     class Meta:
    #         db_table = tdsettings.DB_PREFIX + 'generic_articles'
    #
    #
    # class SectionGroup(models.Model):
    #     car_section = models.OneToOneField(Section, db_column='lgs_str_id', primary_key=True)
    #     group = models.OneToOneField(Group, db_column='lgs_ga_id', primary_key=True)
    #
    #     class Meta:
    #         db_table = tdsettings.DB_PREFIX + 'link_ga_str'
    # unique_together = (("car_section", "group"),)

# class PartGroup(models.Model):
#     id = models.AutoField(db_column='la_id', primary_key=True, verbose_name='Ид')
#     part = models.ForeignKey(Part, db_column='la_art_id', verbose_name='Запчасть')
#     group = models.ForeignKey(Group, db_column='la_ga_id', verbose_name='Группа запчастей')
#     sorting = models.IntegerField(db_column='la_sort', verbose_name='Порядок')
#     car_type = models.ManyToManyField(CarType, through='tecdoc.PartTypeGroupSupplier', verbose_name='')
#
#     class Meta:
#         db_table = tdsettings.DB_PREFIX + 'link_art'


# class PartTypeGroupSupplier(models.Model):
#     car_type = models.OneToOneField(CarType, db_column='lat_typ_id', primary_key=True)
#     group = models.OneToOneField(Group, db_column='lat_ga_id', primary_key=True)
#     part_group = models.OneToOneField(PartGroup, db_column='lat_la_id', primary_key=True)
#     supplier = models.OneToOneField(Supplier, db_column='lat_sup_id')
#     sorting = models.IntegerField(db_column='lat_sort', verbose_name='Порядок', primary_key=True)
#
#     class Meta:
#         db_table = tdsettings.DB_PREFIX + 'link_la_typ'
#
#
# class PartAnalogManager(models.Manager):
#     # use_for_related_fields = True
#
#     def get_queryset(self):
#         return super(PartAnalogManager, self). \
#             get_queryset(). \
#             filter(part__designation__language=tdsettings.LANG_ID). \
#             select_related('part', 'part__designation__description', 'brand', ).prefetch_related('part__group')


# class PartAnalog(models.Model):
#     KIND = ((1, u'не оригинал'),
#             (2, u'торговый'),
#             (3, u'оригинал'),
#             (4, u'номер замен'),
#             (5, u'штрих-код'),
#             )
#
#     part = models.OneToOneField(Part, db_column='ARL_ART_ID', primary_key=True, verbose_name='Запчасть',
#                                 related_name='analogs')
#     number = models.CharField(db_column='ARL_DISPLAY_NR', max_length=105, verbose_name='Номер')
#     search_number = models.CharField(db_column='ARL_SEARCH_NUMBER', max_length=105, verbose_name='Номер для поиска')
#     kind = models.CharField(db_column='ARL_KIND', max_length=1, verbose_name='Тип')
#     brand = models.ForeignKey('tecdoc.Brand', db_column='ARL_BRA_ID', null=True, blank=True,
#                               verbose_name=u'Производитель', )
#     sorting = models.IntegerField(db_column='ARL_SORT', verbose_name='Порядок')
#
#     objects = PartAnalogManager()
#
#     def __str__(self):
#         return u'%s %s %s' % (self.kind, self.get_manufacturer(), self.get_sku())
#
#     class Meta:
#         db_table = tdsettings.DB_PREFIX + 'art_lookup'
#
#     def get_manufacturer(self):
#         if self.kind in ['3', '4']:
#             return self.brand
#         else:
#             return self.part.supplier
#
#     def get_sku(self):
#         # return self.search_number
#         if self.kind in ['2', '3']:
#             return self.number
#         else:
#             return self.part.sku

#
# class Brand(models.Model):
#     id = models.AutoField(db_column='BRA_ID', primary_key=True, verbose_name='Ид')
#     title = models.CharField(db_column='BRA_BRAND', max_length=60, verbose_name='Название', blank=True, null=True)
#     code = models.CharField(db_column='BRA_MFC_CODE', max_length=30, blank=True, null=True, verbose_name='Название')
#
#     class Meta:
#         db_table = tdsettings.DB_PREFIX + 'brands'
#         ordering = ['title']
#         verbose_name = u'Бренд'
#         verbose_name_plural = u'Бренды'
#
#     def __str__(self):
#         return self.title.upper()
#
#         # return self.title.capitalize()
#
#
# # TODO
# class PartListCriteria(models.Model):
#     class Meta:
#         db_table = tdsettings.DB_PREFIX + 'ARTICLE_LIST_CRITERIA'
