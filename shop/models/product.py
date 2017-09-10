import os
from enum import Enum
import re
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from profile.models import Profile
from tecdoc.models import Supplier, Image, PartAttribute, PartApplicability
from tecdoc.models.part import Part, PartAnalog, PartCross, PartProduct


class ProductQuerySet(models.query.QuerySet):
    """ класс-фильтр queryset - возвращает только продукты со статусом Active """

    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    """ кастомный менеджер товаров"""

    def all(self, *args, **kwargs):
        return self.get_queryset()

    def get_price(self):
        if self.user.request.group == 'розница':
            return self.get_retail_price()
        return self.get_whosale_price()


class Product(models.Model):
    """ реализует класс Товар """
    brand = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')

    # slug
    objects = ProductManager()

    def get_sku(self):
        part = Part.objects.filter(clean_part_number=self.sku, supplier__title=self.brand).first()
        return part.part_number

    def update(self, quantity, prices):
        self.quantity = quantity
        self.save()
        ProductPrice(product=self, retail_price=prices[0], price_1=prices[1], price_2=prices[2],
                     price_3=prices[3]).save()

    def get_quantity(self):
        try:
            pp = ProductPrice.objects.get(product=self)
            return pp.quantity
        except Exception as exp:
            return 0

    def title(self):
        title = Part.objects.filter(clean_part_number=self.sku, supplier__title=self.brand).first().title
        if title:
            return title
        return ''

    def get_part_attributes(self):
        part = Part.objects.filter(supplier__title=self.brand, clean_part_number=self.sku).first()
        part_attributes = PartAttribute.objects.filter(part_number=part.part_number, supplier__title=self.brand)
        if part_attributes:
            return part_attributes
        return False

    def get_part_applicability(self):
        part = Part.objects.filter(supplier__title=self.brand, clean_part_number=self.sku).first()
        part_applicability = PartApplicability.objects.filter(part_number=part.part_number, supplier__title=self.brand)
        if part_applicability:
            return sorted(part_applicability)
        return False

    def __str__(self):
        return "%s %s" % (self.brand, self.get_sku())

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={'pk': self.id})
        # return "/shop/products/" + str(self.id)

    def add_to_cart(self):
        return "%s?item=%s&qty=1" % (reverse("cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&delete=true" % (reverse("cart"), self.id)

    def get_price(self, user=None):

        pp = ProductPrice.objects.filter(product=self).first()

        if not pp:
            pp = ProductPrice(product=self, price_1=0, price_2=0, price_3=0, price_4=0)

        if not user:
            try:
                return pp.retail_price
            except:
                return pp.retail_price

        try:
            discount = Profile.objects.get(user=user).discount.discount
            price = pp.retail_price - round((pp.retail_price * discount / 100), 2)
            return price
        except Exception:
            pass

        try:
            group = Profile.objects.get(user=user).group
            group = group.pk
            if group == PriceGroup.RETAIL.value:
                return pp.retail_price
            elif group == PriceGroup.OPT1.value:
                return pp.price_1
            elif group == PriceGroup.OPT2.value:
                return pp.price_2
            elif group == PriceGroup.OPT3.value:
                return pp.price_3
            elif group == PriceGroup.OPT4.value:
                return pp.price_4
            elif group == PriceGroup.OPT5.value:
                return pp.price_5
        except Exception:
            pass

        return pp.retail_price

    def image(self):
        tecdoc_image_path = '/static/main/images/tecdoc/'
        part = Part.objects.filter(clean_part_number=self.sku, supplier__title=self.brand).first()
        image = Image.objects.filter(supplier__title=self.brand, part_number=part.part_number).first()
        try:
            base, ext = os.path.splitext(image.picture)
            if ext == '.BMP':
                ext = ext.replace('BMP', 'jpg')
            return '%s%s%s' % (tecdoc_image_path, base, ext.lower())
        except Exception as exc:
            return '/static/main/images/no-image.png'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class PriceGroup(Enum):
    RETAIL = 1
    OPT1 = 2
    OPT2 = 3
    OPT3 = 4
    OPT4 = 5
    OPT5 = 6


def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    return "products/%s_%s" % (instance.id, filename)


class ProductImage(models.Model):
    """ фоточки для товаров """
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to, null=True, blank=True)

    def __str__(self):
        return self.product.title


class ProductPrice(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(blank=True, null=True, default=0)
    retail_price = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_1 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_2 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_3 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_4 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_5 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return  "%s" % self.price_1

    def get_price(self, user):
        retail_price = self.retail_price
        whosale_price = self.get_whosale_price(user)
        prices = {'retail_price': retail_price, 'whosale_price': whosale_price}
        return prices

    def get_whosale_price(self, user):
        if not user:
            return None
        try:
            group = Profile.objects.get(user=user).group
            group = group.pk
            if group == PriceGroup.RETAIL.value:
                return self.retail_price
            elif group == PriceGroup.OPT1.value:
                return self.price_1
            elif group == PriceGroup.OPT2.value:
                return self.price_2
            elif group == PriceGroup.OPT3.value:
                return self.price_3
            elif group == PriceGroup.OPT4.value:
                return self.price_4
            elif group == PriceGroup.OPT5.value:
                return self.price_5
        except Exception:
            return None


def get_part_analogs(part_analog, user):
    data = part_analog
    sku = []
    brand = []
    for part in data:
        sku.append(part.part_group.part.sku)
    products = Product.objects.filter(sku__in=sku)

    # adding price data into parttypegroupsupplier_list
    parts_with_price = []
    parts_without_price = []
    for part in data:
        brand_name = part.part_group.part.supplier.title
        sku = part.part_group.part.sku
        for product in products:
            if clean_number(sku) == clean_number(product.sku) and brand_name == product.brand:
                part.part_group.part.price = product.get_price(user=user)
                part.part_group.part.product_id = product.id
                part.part_group.part.quantity = product.get_quantity()
        if not hasattr(part.part_group.part, 'price'):
            part.part_group.part.price = -1
    part_analog_data = sorted(data, key=lambda x: x.part_group.part.price, reverse=True)
    return part_analog_data


number_re = re.compile('[^a-zA-Z0-9]+')


def clean_number(number):
    return number_re.sub('', number)


def get_prices(analogs, user):
    if not analogs:
        return False
    sku_list = list()
    supplier_ids = list()
    for analog in analogs:
        sku_list.append(analog['clean_part_number'])
        supplier_ids.append(analog['supplier'])
    suppliers = Supplier.objects.filter(id__in=supplier_ids)
    products = Product.objects.filter(sku__in=sku_list)
    parts = Part.objects.filter(clean_part_number__in=sku_list, supplier__in=suppliers)

    part_products = list()
    for analog in analogs:
        brand = suppliers.get(id=analog['supplier'])
        part_number = analog['part_number']
        clean_part_number = analog['clean_part_number']
        price = -1
        quantity = -1
        product_id = None
        try:
            title = parts.filter(clean_part_number=clean_part_number, supplier=brand).first().title
        except:
            title = None
        part_product = PartProduct(supplier=brand.title, part_number=part_number, clean_part_number=clean_part_number,
                                   price=price, quantity=quantity, product_id=product_id, title=title)
        for product in products:
            if product.sku == clean_part_number and product.brand.upper() == brand.title.upper():
                part_product.price = product.get_price(user=user)
                part_product.product_id = product.id
                part_product.quantity = product.get_quantity()
        part_products.append(part_product)
    return part_products


def get_analogs(clean_part_number, supplier, user):
    part = Part.objects.filter(clean_part_number=clean_part_number, supplier=supplier).first()
    part_number = part.part_number
    part_analogs = PartAnalog.objects.filter(part_number=part_number, supplier=supplier)
    crosses = list()
    for part_analog in part_analogs:
        crosses.append(part_analog.oenbr)
    analogs = PartCross.objects.values('supplier', 'part_number').filter(oenbr__in=crosses).distinct()
    for analog in analogs:
        analog['clean_part_number'] = clean_number(analog['part_number'])
    analogs = get_prices(analogs, user)
    if analogs:
        return sorted(analogs, reverse=True)
    return {}


def get_products(supplier, clean_part_number):
    products = Product.objects.filter(brand=supplier.title, sku=clean_part_number)
    part_products = list()
    for product in products:
        price = product.get_price()
        quantity = product.get_quantity()
        title = Part.objects.filter(supplier__title=product.brand, clean_part_number=product.sku).first().title
        supplier = product.brand
        part_number = product.sku
        product_id = product.id
        part_product = PartProduct(
            supplier=supplier,
            part_number=part_number,
            clean_part_number=clean_part_number,
            product_id=product_id,
            price=price,
            quantity=quantity,
            title=title

        )
        part_products.append(part_product)
    return sorted(part_products, reverse=True)


