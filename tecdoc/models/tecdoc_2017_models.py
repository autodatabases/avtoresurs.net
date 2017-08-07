# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AllArticles(models.Model):
    supplierid = models.BigIntegerField()
    datasupplierarticlenumber = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'all_articles'


class AllArticlesCsv(models.Model):
    id = models.BigAutoField(primary_key=True)
    supplierid = models.BigIntegerField()
    datasupplierarticlenumber = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_articles_csv'


class ArticleAcc(models.Model):
    supplierid = models.BigIntegerField(db_column='supplierId')  # Field name made lowercase.
    datasupplierarticlenumber = models.CharField(db_column='DataSupplierArticleNumber', max_length=128)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=128)  # Field name made lowercase.
    accsupplierid = models.BigIntegerField(db_column='AccSupplierId')  # Field name made lowercase.
    accdatasupplierarticlenumber = models.CharField(db_column='AccDataSupplierArticleNumber', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_acc'


class ArticleAttributes(models.Model):
    supplierid = models.BigIntegerField()
    datasupplierarticlenumber = models.CharField(max_length=128)
    id = models.BigIntegerField()
    attributeinformationtype = models.CharField(max_length=512)
    description = models.CharField(max_length=512, blank=True, null=True)
    displaytitle = models.CharField(max_length=512, blank=True, null=True)
    displayvalue = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'article_attributes'


class ArticleCross(models.Model):
    manufacturerid = models.BigIntegerField(db_column='manufacturerId')  # Field name made lowercase.
    oenbr = models.CharField(db_column='OENbr', max_length=128)  # Field name made lowercase.
    supplierid = models.BigIntegerField(db_column='SupplierId')  # Field name made lowercase.
    partsdatasupplierarticlenumber = models.CharField(db_column='PartsDataSupplierArticleNumber', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_cross'


class ArticleImages(models.Model):
    supplierid = models.BigIntegerField(db_column='supplierId')  # Field name made lowercase.
    datasupplierarticlenumber = models.CharField(db_column='DataSupplierArticleNumber', max_length=128)  # Field name made lowercase.
    additionaldescription = models.CharField(db_column='AdditionalDescription', max_length=128)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=128)  # Field name made lowercase.
    documentname = models.CharField(db_column='DocumentName', max_length=128)  # Field name made lowercase.
    documenttype = models.CharField(db_column='DocumentType', max_length=128)  # Field name made lowercase.
    normeddescriptionid = models.CharField(db_column='NormedDescriptionID', max_length=128)  # Field name made lowercase.
    picturename = models.CharField(db_column='PictureName', max_length=128)  # Field name made lowercase.
    showimmediately = models.CharField(db_column='ShowImmediately', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_images'


class ArticleInf(models.Model):
    supplierid = models.BigIntegerField(db_column='supplierId')  # Field name made lowercase.
    datasupplierarticlenumber = models.CharField(db_column='DataSupplierArticleNumber', max_length=128)  # Field name made lowercase.
    informationtext = models.TextField(db_column='InformationText')  # Field name made lowercase.
    informationtype = models.CharField(db_column='InformationType', max_length=128)  # Field name made lowercase.
    informationtypekey = models.CharField(db_column='InformationTypeKey', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_inf'


class ArticleLi(models.Model):
    supplierid = models.BigIntegerField(db_column='supplierId')  # Field name made lowercase.
    datasupplierarticlenumber = models.CharField(db_column='DataSupplierArticleNumber', max_length=128)  # Field name made lowercase.
    linkagetypeid = models.CharField(db_column='linkageTypeId', max_length=128)  # Field name made lowercase.
    linkageid = models.BigIntegerField(db_column='linkageId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_li'


class ArticleLinks(models.Model):
    supplierid = models.BigIntegerField()
    productid = models.BigIntegerField()
    linkagetypeid = models.BigIntegerField()
    linkageid = models.BigIntegerField()
    datasupplierarticlenumber = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article_links'


class ArticleNn(models.Model):
    supplierid = models.BigIntegerField()
    datasupplierarticlenumber = models.CharField(max_length=128)
    newnbr = models.CharField(max_length=128)
    newsupplierid = models.BigIntegerField()
    newdatasupplierarticlenumber = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'article_nn'


class ArticleOe(models.Model):
    supplierid = models.BigIntegerField()
    datasupplierarticlenumber = models.CharField(max_length=128)
    isadditive = models.CharField(db_column='IsAdditive', max_length=128)  # Field name made lowercase.
    oenbr = models.CharField(db_column='OENbr', max_length=128)  # Field name made lowercase.
    manufacturerid = models.BigIntegerField(db_column='manufacturerId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_oe'


class ArticleParts(models.Model):
    supplierid = models.BigIntegerField(db_column='supplierId')  # Field name made lowercase.
    datasupplierarticlenumber = models.CharField(db_column='DataSupplierArticleNumber', max_length=128)  # Field name made lowercase.
    quantity = models.CharField(db_column='Quantity', max_length=128)  # Field name made lowercase.
    partssupplierid = models.BigIntegerField(db_column='PartsSupplierId')  # Field name made lowercase.
    partsdatasupplierarticlenumber = models.CharField(db_column='PartsDataSupplierArticleNumber', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_parts'


class ArticleRn(models.Model):
    supplierid = models.BigIntegerField()
    datasupplierarticlenumber = models.CharField(max_length=128)
    replacenbr = models.CharField(max_length=128)
    replacedupplierid = models.BigIntegerField()
    replacedatasupplierarticlenumber = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'article_rn'


class ArticleUn(models.Model):
    supplierid = models.BigIntegerField()
    datasupplierarticlenumber = models.CharField(max_length=128)
    utilityno = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'article_un'


class Articles(models.Model):
    supplierid = models.BigIntegerField(db_column='supplierId')  # Field name made lowercase.
    datasupplierarticlenumber = models.CharField(db_column='DataSupplierArticleNumber', max_length=128)  # Field name made lowercase.
    articlestatedisplaytitle = models.CharField(db_column='ArticleStateDisplayTitle', max_length=128)  # Field name made lowercase.
    articlestatedisplayvalue = models.CharField(db_column='ArticleStateDisplayValue', max_length=128)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=128)  # Field name made lowercase.
    flagaccessory = models.CharField(db_column='FlagAccessory', max_length=128)  # Field name made lowercase.
    flagmaterialcertification = models.CharField(db_column='FlagMaterialCertification', max_length=128)  # Field name made lowercase.
    flagremanufactured = models.CharField(db_column='FlagRemanufactured', max_length=128)  # Field name made lowercase.
    flagselfservicepacking = models.CharField(db_column='FlagSelfServicePacking', max_length=128)  # Field name made lowercase.
    foundby = models.CharField(db_column='FoundBy', max_length=128)  # Field name made lowercase.
    foundstring = models.CharField(db_column='FoundString', max_length=128)  # Field name made lowercase.
    hasaxle = models.CharField(db_column='HasAxle', max_length=128)  # Field name made lowercase.
    hascommercialvehicle = models.CharField(db_column='HasCommercialVehicle', max_length=128)  # Field name made lowercase.
    hascvmanuid = models.CharField(db_column='HasCVManuID', max_length=128)  # Field name made lowercase.
    hasengine = models.CharField(db_column='HasEngine', max_length=128)  # Field name made lowercase.
    haslinkitems = models.CharField(db_column='HasLinkitems', max_length=128)  # Field name made lowercase.
    hasmotorbike = models.CharField(db_column='HasMotorbike', max_length=128)  # Field name made lowercase.
    haspassengercar = models.CharField(db_column='HasPassengerCar', max_length=128)  # Field name made lowercase.
    isvalid = models.CharField(db_column='IsValid', max_length=128)  # Field name made lowercase.
    lotsize1 = models.CharField(db_column='LotSize1', max_length=128)  # Field name made lowercase.
    lotsize2 = models.CharField(db_column='LotSize2', max_length=128)  # Field name made lowercase.
    normalizeddescription = models.CharField(db_column='NormalizedDescription', max_length=128)  # Field name made lowercase.
    packingunit = models.CharField(db_column='PackingUnit', max_length=128)  # Field name made lowercase.
    quantityperpackingunit = models.CharField(db_column='QuantityPerPackingUnit', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'articles'


class ArticlesCsv(models.Model):
    id = models.BigAutoField(primary_key=True)
    supplierid = models.BigIntegerField()
    datasupplierarticlenumber = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'articles_csv'


class AxleAttributes(models.Model):
    axleid = models.BigIntegerField()
    attributegroup = models.CharField(max_length=512, blank=True, null=True)
    attributetype = models.CharField(max_length=512, blank=True, null=True)
    displaytitle = models.CharField(max_length=512, blank=True, null=True)
    displayvalue = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'axle_attributes'


class AxlePds(models.Model):
    axleid = models.BigIntegerField()
    nodeid = models.BigIntegerField()
    productid = models.BigIntegerField()
    supplierid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'axle_pds'


class AxlePrd(models.Model):
    id = models.BigIntegerField()
    assemblygroupdescription = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    normalizeddescription = models.CharField(max_length=256)
    usagedescription = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'axle_prd'


class AxleQsi(models.Model):
    axleid = models.BigIntegerField()
    description = models.CharField(max_length=512, blank=True, null=True)
    quickstarttype = models.CharField(max_length=512, blank=True, null=True)
    validstate = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'axle_qsi'


class AxleTrees(models.Model):
    axleid = models.BigIntegerField()
    searchtreeid = models.BigIntegerField()
    id = models.BigIntegerField()
    parentid = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'axle_trees'


class Axles(models.Model):
    id = models.BigIntegerField()
    canbedisplayed = models.CharField(max_length=512, blank=True, null=True)
    constructioninterval = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    fulldescription = models.CharField(max_length=512, blank=True, null=True)
    haslink = models.CharField(max_length=512, blank=True, null=True)
    isaxle = models.CharField(max_length=512, blank=True, null=True)
    iscommercialvehicle = models.CharField(max_length=512, blank=True, null=True)
    iscvmanufacturerid = models.CharField(max_length=512, blank=True, null=True)
    isengine = models.CharField(max_length=512, blank=True, null=True)
    ismotorbike = models.CharField(max_length=512, blank=True, null=True)
    ispassengercar = models.CharField(max_length=512, blank=True, null=True)
    istransporter = models.CharField(max_length=512, blank=True, null=True)
    isvalidforcurrentcountry = models.CharField(max_length=512, blank=True, null=True)
    linkitemtype = models.CharField(max_length=512, blank=True, null=True)
    modelid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'axles'


class CommercialDriverCabs(models.Model):
    id = models.BigIntegerField()
    drivercabid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'commercial_driver_cabs'


class CommercialVehicleAttributes(models.Model):
    commercialvehicleid = models.BigIntegerField()
    attributegroup = models.CharField(max_length=512, blank=True, null=True)
    attributetype = models.CharField(max_length=512, blank=True, null=True)
    displaytitle = models.CharField(max_length=512, blank=True, null=True)
    displayvalue = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commercial_vehicle_attributes'


class CommercialVehicleAxles(models.Model):
    id = models.BigIntegerField()
    axleid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'commercial_vehicle_axles'


class CommercialVehicleEngines(models.Model):
    id = models.BigIntegerField()
    engineid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'commercial_vehicle_engines'


class CommercialVehiclePds(models.Model):
    commertialvehicleid = models.BigIntegerField()
    nodeid = models.BigIntegerField()
    productid = models.BigIntegerField()
    supplierid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'commercial_vehicle_pds'


class CommercialVehiclePrd(models.Model):
    id = models.BigIntegerField()
    assemblygroupdescription = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    normalizeddescription = models.CharField(max_length=256)
    usagedescription = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'commercial_vehicle_prd'


class CommercialVehicleQsi(models.Model):
    commercialvehicleid = models.BigIntegerField()
    description = models.CharField(max_length=512, blank=True, null=True)
    quickstarttype = models.CharField(max_length=512, blank=True, null=True)
    validstate = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commercial_vehicle_qsi'


class CommercialVehicleSubTypes(models.Model):
    id = models.BigIntegerField()
    subtypeid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'commercial_vehicle_sub_types'


class CommercialVehicleTrees(models.Model):
    commercialvehicleid = models.BigIntegerField()
    searchtreeid = models.BigIntegerField()
    id = models.BigIntegerField()
    parentid = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commercial_vehicle_trees'


class CommercialVehicles(models.Model):
    id = models.BigIntegerField()
    canbedisplayed = models.CharField(max_length=512, blank=True, null=True)
    constructioninterval = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    fulldescription = models.CharField(max_length=512, blank=True, null=True)
    haslink = models.CharField(max_length=512, blank=True, null=True)
    isaxle = models.CharField(max_length=512, blank=True, null=True)
    iscommercialvehicle = models.CharField(max_length=512, blank=True, null=True)
    iscvmanufacturerid = models.CharField(max_length=512, blank=True, null=True)
    isengine = models.CharField(max_length=512, blank=True, null=True)
    ismotorbike = models.CharField(max_length=512, blank=True, null=True)
    ispassengercar = models.CharField(max_length=512, blank=True, null=True)
    istransporter = models.CharField(max_length=512, blank=True, null=True)
    isvalidforcurrentcountry = models.CharField(max_length=512, blank=True, null=True)
    linkitemtype = models.CharField(max_length=512, blank=True, null=True)
    modelid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commercial_vehicles'


class Countries(models.Model):
    countrycode = models.CharField(max_length=512, blank=True, null=True)
    currencycode = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    isgroup = models.CharField(max_length=512, blank=True, null=True)
    isocode2 = models.CharField(max_length=512, blank=True, null=True)
    isocode3 = models.CharField(max_length=512, blank=True, null=True)
    isocodeno = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class CountryGroups(models.Model):
    countrycode = models.CharField(max_length=512, blank=True, null=True)
    currencycode = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    isgroup = models.CharField(max_length=512, blank=True, null=True)
    isocode2 = models.CharField(max_length=512, blank=True, null=True)
    isocode3 = models.CharField(max_length=512, blank=True, null=True)
    isocodeno = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country_groups'


class EngineAttributes(models.Model):
    engineid = models.BigIntegerField()
    attributegroup = models.CharField(max_length=512, blank=True, null=True)
    attributetype = models.CharField(max_length=512, blank=True, null=True)
    displaytitle = models.CharField(max_length=512, blank=True, null=True)
    displayvalue = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engine_attributes'


class EnginePds(models.Model):
    engineid = models.BigIntegerField()
    nodeid = models.BigIntegerField()
    productid = models.BigIntegerField()
    supplierid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'engine_pds'


class EnginePrd(models.Model):
    id = models.BigIntegerField()
    assemblygroupdescription = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    normalizeddescription = models.CharField(max_length=256)
    usagedescription = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'engine_prd'


class EngineQsi(models.Model):
    engineid = models.BigIntegerField()
    description = models.CharField(max_length=512, blank=True, null=True)
    quickstarttype = models.CharField(max_length=512, blank=True, null=True)
    validstate = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engine_qsi'


class EngineTrees(models.Model):
    engineid = models.BigIntegerField()
    searchtreeid = models.BigIntegerField()
    id = models.BigIntegerField()
    parentid = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engine_trees'


class Engines(models.Model):
    id = models.BigIntegerField()
    canbedisplayed = models.CharField(max_length=512, blank=True, null=True)
    constructioninterval = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    fulldescription = models.CharField(max_length=512, blank=True, null=True)
    haslink = models.CharField(max_length=512, blank=True, null=True)
    haslinkitem = models.CharField(max_length=512, blank=True, null=True)
    isaxle = models.CharField(max_length=512, blank=True, null=True)
    iscommercialvehicle = models.CharField(max_length=512, blank=True, null=True)
    iscvmanufacturerid = models.CharField(max_length=512, blank=True, null=True)
    isengine = models.CharField(max_length=512, blank=True, null=True)
    ismotorbike = models.CharField(max_length=512, blank=True, null=True)
    ispassengercar = models.CharField(max_length=512, blank=True, null=True)
    istransporter = models.CharField(max_length=512, blank=True, null=True)
    isvalidforcurrentcountry = models.CharField(max_length=512, blank=True, null=True)
    linkitemtype = models.CharField(max_length=512, blank=True, null=True)
    manufacturerid = models.BigIntegerField(blank=True, null=True)
    salesdescription = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engines'


class Languages(models.Model):
    id = models.BigIntegerField()
    codepage = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    isocode2 = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'languages'


class Manufacturers(models.Model):
    id = models.BigIntegerField()
    canbedisplayed = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    fulldescription = models.CharField(max_length=512, blank=True, null=True)
    haslink = models.CharField(max_length=512, blank=True, null=True)
    isaxle = models.CharField(max_length=512, blank=True, null=True)
    iscommercialvehicle = models.CharField(max_length=512, blank=True, null=True)
    iscvmanufacturerid = models.CharField(max_length=512, blank=True, null=True)
    isengine = models.CharField(max_length=512, blank=True, null=True)
    ismotorbike = models.CharField(max_length=512, blank=True, null=True)
    ispassengercar = models.CharField(max_length=512, blank=True, null=True)
    istransporter = models.CharField(max_length=512, blank=True, null=True)
    isvalidforcurrentcountry = models.CharField(max_length=512, blank=True, null=True)
    isvgl = models.CharField(max_length=512, blank=True, null=True)
    linkitemtype = models.CharField(max_length=512, blank=True, null=True)
    matchcode = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manufacturers'


class Models(models.Model):
    id = models.BigIntegerField()
    canbedisplayed = models.CharField(max_length=512, blank=True, null=True)
    constructioninterval = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    fulldescription = models.CharField(max_length=512, blank=True, null=True)
    haslink = models.CharField(max_length=512, blank=True, null=True)
    isaxle = models.CharField(max_length=512, blank=True, null=True)
    iscommercialvehicle = models.CharField(max_length=512, blank=True, null=True)
    iscvmanufacturerid = models.CharField(max_length=512, blank=True, null=True)
    isengine = models.CharField(max_length=512, blank=True, null=True)
    ismotorbike = models.CharField(max_length=512, blank=True, null=True)
    ispassengercar = models.CharField(max_length=512, blank=True, null=True)
    istransporter = models.CharField(max_length=512, blank=True, null=True)
    isvalidforcurrentcountry = models.CharField(max_length=512, blank=True, null=True)
    linkitemtype = models.CharField(max_length=512, blank=True, null=True)
    manufacturerid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'models'


class MotorbikeAttributes(models.Model):
    motorbikeid = models.BigIntegerField()
    attributegroup = models.CharField(max_length=512, blank=True, null=True)
    attributetype = models.CharField(max_length=512, blank=True, null=True)
    displaytitle = models.CharField(max_length=512, blank=True, null=True)
    displayvalue = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motorbike_attributes'


class MotorbikePds(models.Model):
    motorbikeid = models.BigIntegerField()
    nodeid = models.BigIntegerField()
    productid = models.BigIntegerField()
    supplierid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'motorbike_pds'


class MotorbikePrd(models.Model):
    id = models.BigIntegerField()
    assemblygroupdescription = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    normalizeddescription = models.CharField(max_length=256)
    usagedescription = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'motorbike_prd'


class MotorbikeQsi(models.Model):
    motorbikeid = models.BigIntegerField()
    description = models.CharField(max_length=512, blank=True, null=True)
    quickstarttype = models.CharField(max_length=512, blank=True, null=True)
    validstate = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motorbike_qsi'


class MotorbikeTrees(models.Model):
    motorbikeid = models.BigIntegerField()
    searchtreeid = models.BigIntegerField()
    id = models.BigIntegerField()
    parentid = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motorbike_trees'


class Motorbikes(models.Model):
    id = models.BigIntegerField()
    canbedisplayed = models.CharField(max_length=512, blank=True, null=True)
    constructioninterval = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    fulldescription = models.CharField(max_length=512, blank=True, null=True)
    haslink = models.CharField(max_length=512, blank=True, null=True)
    isaxle = models.CharField(max_length=512, blank=True, null=True)
    iscommercialvehicle = models.CharField(max_length=512, blank=True, null=True)
    iscvmanufacturerid = models.CharField(max_length=512, blank=True, null=True)
    isengine = models.CharField(max_length=512, blank=True, null=True)
    ismotorbike = models.CharField(max_length=512, blank=True, null=True)
    ispassengercar = models.CharField(max_length=512, blank=True, null=True)
    istransporter = models.CharField(max_length=512, blank=True, null=True)
    isvalidforcurrentcountry = models.CharField(max_length=512, blank=True, null=True)
    linkitemtype = models.CharField(max_length=512, blank=True, null=True)
    modelid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motorbikes'


class PassangerCarAttributes(models.Model):
    passangercarid = models.BigIntegerField()
    attributegroup = models.CharField(max_length=512, blank=True, null=True)
    attributetype = models.CharField(max_length=512, blank=True, null=True)
    displaytitle = models.CharField(max_length=512, blank=True, null=True)
    displayvalue = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passanger_car_attributes'


class PassangerCarEngines(models.Model):
    id = models.BigIntegerField()
    engineid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'passanger_car_engines'


class PassangerCarPds(models.Model):
    passangercarid = models.BigIntegerField()
    nodeid = models.BigIntegerField()
    productid = models.BigIntegerField()
    supplierid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'passanger_car_pds'


class PassangerCarPrd(models.Model):
    id = models.BigIntegerField()
    assemblygroupdescription = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    normalizeddescription = models.CharField(max_length=256)
    usagedescription = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'passanger_car_prd'


class PassangerCarQsi(models.Model):
    passangercarid = models.BigIntegerField()
    description = models.CharField(max_length=512, blank=True, null=True)
    quickstarttype = models.CharField(max_length=512, blank=True, null=True)
    validstate = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passanger_car_qsi'


class PassangerCarTrees(models.Model):
    passangercarid = models.BigIntegerField()
    searchtreeid = models.BigIntegerField()
    id = models.BigIntegerField()
    parentid = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passanger_car_trees'


class PassangerCars(models.Model):
    id = models.BigIntegerField()
    canbedisplayed = models.CharField(max_length=512, blank=True, null=True)
    constructioninterval = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    fulldescription = models.CharField(max_length=512, blank=True, null=True)
    haslink = models.CharField(max_length=512, blank=True, null=True)
    isaxle = models.CharField(max_length=512, blank=True, null=True)
    iscommercialvehicle = models.CharField(max_length=512, blank=True, null=True)
    iscvmanufacturerid = models.CharField(max_length=512, blank=True, null=True)
    isengine = models.CharField(max_length=512, blank=True, null=True)
    ismotorbike = models.CharField(max_length=512, blank=True, null=True)
    ispassengercar = models.CharField(max_length=512, blank=True, null=True)
    istransporter = models.CharField(max_length=512, blank=True, null=True)
    isvalidforcurrentcountry = models.CharField(max_length=512, blank=True, null=True)
    linkitemtype = models.CharField(max_length=512, blank=True, null=True)
    modelid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passanger_cars'


class Prd(models.Model):
    id = models.BigIntegerField()
    assemblygroupdescription = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    normalizeddescription = models.CharField(max_length=256)
    usagedescription = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'prd'


class SupplierDetails(models.Model):
    supplierid = models.BigIntegerField()
    addresstype = models.CharField(max_length=512, blank=True, null=True)
    addresstypeid = models.CharField(max_length=512, blank=True, null=True)
    city1 = models.CharField(max_length=512, blank=True, null=True)
    city2 = models.CharField(max_length=512, blank=True, null=True)
    countrycode = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(max_length=512, blank=True, null=True)
    fax = models.CharField(max_length=512, blank=True, null=True)
    homepage = models.CharField(max_length=512, blank=True, null=True)
    name1 = models.CharField(max_length=512, blank=True, null=True)
    name2 = models.CharField(max_length=512, blank=True, null=True)
    postalcodecity = models.CharField(max_length=512, blank=True, null=True)
    postalcodepob = models.CharField(max_length=512, blank=True, null=True)
    postalcodewholesaler = models.CharField(max_length=512, blank=True, null=True)
    postalcountrycode = models.CharField(max_length=512, blank=True, null=True)
    postofficebox = models.CharField(max_length=512, blank=True, null=True)
    street1 = models.CharField(max_length=512, blank=True, null=True)
    street2 = models.CharField(max_length=512, blank=True, null=True)
    telephone = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier_details'


class Suppliers(models.Model):
    id = models.BigIntegerField()
    dataversion = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    matchcode = models.CharField(max_length=512, blank=True, null=True)
    nbrofarticles = models.CharField(max_length=512, blank=True, null=True)
    hasnewversionarticles = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers'


class SuppliersWithNvArticles(models.Model):
    id = models.BigIntegerField()
    dataversion = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    matchcode = models.CharField(max_length=512, blank=True, null=True)
    nbrofarticles = models.CharField(max_length=512, blank=True, null=True)
    hasnewversionarticles = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers_with_nv_articles'


class SuppliersWithNvLinkages(models.Model):
    id = models.BigIntegerField()
    dataversion = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    matchcode = models.CharField(max_length=512, blank=True, null=True)
    nbrofarticles = models.CharField(max_length=512, blank=True, null=True)
    hasnewversionarticles = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers_with_nv_linkages'
