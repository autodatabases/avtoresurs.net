import os
from cms.models import CMSPlugin
from enum import Enum
import re
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from user_profile.models import UserProfile

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


class ProductTypes(Enum):
    Tecdoc = 'Tecdoc'
    Battery = 'Battery'
    Oil = 'Oil'

    @classmethod
    def as_choices(cls):
        return tuple((x.name, x.value) for x in cls)

    def __str__(self):
        return self.value


class ProductCategoryQuerySet(models.query.QuerySet):
    """ класс-фильтр queryset - возвращает только категории со статусом Active """

    def get_queryset(self):
        return self.filter(active=True)


class ProductCategoryManager(models.Manager):
    """ кастомный менеджер категорий"""

    def all(self, *args, **kwargs):
        return self.filter(active=True)


class ProductCategory(models.Model):
    Tecdoc = 'tecdoc'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class Admin:
        manager = ProductCategoryManager()

    name = models.CharField(max_length=255, verbose_name='Название (на английском)')
    russian_name = models.CharField(max_length=255, verbose_name='Название (на русском)')
    description = models.CharField(max_length=255, verbose_name='Описание')
    brands = models.CharField(max_length=255, blank=True, null=True, verbose_name='Брэнды (через запятую)')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    active = models.BooleanField(default=True, verbose_name='Активен')

    objects = ProductCategoryManager()

    def __str__(self):
        return self.russian_name

    def brands_as_list(self):
        if self.brands:
            return self.brands.split(",")
        else:
            return {}

    @classmethod
    def get_all_categories(cls):
        product_categories = cls.objects.all()
        return product_categories

    @classmethod
    def as_choices(cls):
        product_categories = cls.get_all_categories()
        return tuple((x.name.lower(), x.russian_name) for x in product_categories if x.active == True)

    @classmethod
    def as_list(cls):
        product_categories = cls.get_all_categories()
        return [x.name.lower() for x in product_categories]


class Product(models.Model):
    """ реализует класс Товар """
    brand = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    product_category = models.CharField(choices=ProductCategory.as_choices(), max_length=10,
                                        verbose_name='Тип продукта',
                                        null=True)
    _description = models.CharField(max_length=300, null=True, verbose_name='Описание', db_column='description')

    _image = models.ImageField(null=True, blank=True, verbose_name='Картинка', db_column='image')

    @property
    def description(self):
        return self._description or ''

    # slug
    objects = ProductManager()

    def get_sku(self):
        part = Part.objects.filter(clean_part_number=self.sku, supplier__title=self.brand).first()
        return getattr(part, 'part_number', self.sku)

    def update(self, quantity, prices):
        self.quantity = quantity
        self.save()
        ProductPrice(product=self, retail_price=prices[0], price_1=prices[1], price_2=prices[2],
                     price_3=prices[3]).save()

    def get_quantity(self):
        try:
            product_prices = ProductPrice.objects.filter(product=self)
            quantity = 0
            for product_price in product_prices:
                quantity += product_price.quantity
            return quantity
        except Exception as exp:
            return 0

    @property
    def total_quantity(self):
        return self.get_quantity()

    @property
    def title(self):
        part = Part.objects.filter(clean_part_number=self.sku, supplier__title=self.brand).first()
        title = getattr(part, 'title', self._default_title)
        return title

    @property
    def _default_title(self):
        product_category = ProductCategory.objects.filter(name=self.product_category).first()
        if product_category:
            return product_category.description
        else:
            return 'Запчасть'

    def get_part_attributes(self):
        part = Part.objects.filter(supplier__title=self.brand, clean_part_number=self.sku).first()
        part_number = getattr(part, 'part_number', None)
        part_attributes = PartAttribute.objects.filter(part_number=part_number, supplier__title=self.brand)
        if part_attributes:
            return part_attributes
        return False

    def get_part_applicability(self):
        part = Part.objects.filter(supplier__title=self.brand, clean_part_number=self.sku).first()
        part_number = getattr(part, 'part_number', None)
        part_applicability = PartApplicability.objects.filter(part_number=part_number, supplier__title=self.brand)
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

    def get_price(self, user=None, storage=None):

        pp = ProductPrice.objects.filter(product=self, storage__id=1).first()
        if storage is not None:
            pp = ProductPrice.objects.filter(product=self, storage=storage).first()
        if not pp:
            pp = ProductPrice(product=self, price_1=0, price_2=0, price_3=0, price_4=0)

        if not user:
            try:
                return pp.retail_price
            except:
                return pp.retail_price

        try:
            discount = UserProfile.objects.get(user=user).discount.discount
            price = pp.retail_price - round((pp.retail_price * discount / 100), 2)
            return price
        except Exception:
            pass

        try:
            group = UserProfile.objects.get(user=user).group
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

    @property
    def image(self):
        if self._image:
            return self._image.url
        else:
            tecdoc_image_path = '/static/main/images/tecdoc/'
            part = Part.objects.filter(clean_part_number=self.sku, supplier__title=self.brand).first()
            part_number = getattr(part, 'part_number', None)
            image = Image.objects.filter(supplier__title=self.brand, part_number=part_number).first()
            try:
                base, ext = os.path.splitext(image.picture)
                if ext == '.BMP':
                    ext = ext.replace('BMP', 'jpg')
                return '%s%s%s' % (tecdoc_image_path, base, ext.lower())
            except Exception as exc:
                return '/static/main/images/no-image.png'

    @classmethod
    def get_products(cls, product_category=ProductCategory.Tecdoc):
        products = cls.objects.filter(product_category=product_category)
        return products

    @classmethod
    def get_additional_products(cls, sku):
        pc_query = ProductCategory.get_all_categories()
        additional_products = {}
        for product_category in pc_query:
            products = Product.search_by_sku_category(sku=sku, category=product_category.name)
            if products:
                additional_products.update({product_category: products})
        return additional_products

    @classmethod
    def search_by_sku_category(cls, sku, category):
        products_query = cls.objects.filter(sku__icontains=sku, product_category=category).prefetch_related()
        products = sorted(products_query, reverse=True)
        return products

    def __gt__(self, other):
        return self.total_quantity > other.total_quantity

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
    OPT6 = 7


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
    storage = models.ForeignKey('Storage', null=True, blank=True)
    quantity = models.IntegerField(blank=True, null=True, default=0)
    retail_price = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_1 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_2 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_3 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_4 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_5 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    price_6 = models.DecimalField(decimal_places=2, max_digits=20, default=0, blank=True, null=True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return "%s" % self.price_1

    def get_price(self, user):
        retail_price = self.retail_price
        whosale_price = self.get_whosale_price(user)
        prices = {'retail_price': retail_price, 'whosale_price': whosale_price}
        return prices

    def get_whosale_price(self, user):
        if not user:
            return None
        try:
            group = UserProfile.objects.get(user=user).group
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
            elif group == PriceGroup.OPT6.value:
                return self.price_6
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
    part_number = getattr(part, 'part_number', None)
    part_analogs = PartAnalog.objects.filter(part_number=part_number, supplier=supplier)
    crosses = list()
    for part_analog in part_analogs:
        crosses.append(part_analog.oenbr)
    analogs = PartCross.objects.values('supplier', 'part_number').filter(oenbr__in=crosses).distinct()
    for analog in analogs:
        analog['clean_part_number'] = clean_number(analog['part_number'])
    analogs = get_prices(analogs, user)
    result = {}
    if analogs:
        result = sorted(analogs, reverse=True)
    return result


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


class ProductTypeModelPlugin(CMSPlugin):
    product_category = models.CharField(choices=ProductCategory.as_choices(), max_length=10,
                                        verbose_name='Тип продукта',
                                        null=True)

    @property
    def products(self):
        product_query = Product.get_products(product_category=self.product_category).order_by('sku')
        return product_query
