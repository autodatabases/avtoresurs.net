from enum import Enum

import re
from django.db import models

# Create your models here.
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from profile.models import Profile
from tecdoc.models.part import Part, PartGroup


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
    # title = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    # cross_sku = models.CharField(max_length=255)
    quantity = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    retail_price = models.DecimalField(decimal_places=2, max_digits=20, default=False)
    price_1 = models.DecimalField(decimal_places=2, max_digits=20, default=False)
    price_2 = models.DecimalField(decimal_places=2, max_digits=20, default=False)
    price_3 = models.DecimalField(decimal_places=2, max_digits=20, default=False)
    price_4 = models.DecimalField(decimal_places=2, max_digits=20, default=False)
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')

    # slug
    objects = ProductManager()

    def update(self, quantity, prices):
        self.quantity = quantity
        self.save()
        ProductPrice(product=self, retail_price=prices[0], price_1=prices[1], price_2=prices[2],
                     price_3=prices[3]).save()

    def get_retail_price(self):
        return self.retail_price

    def get_whosale_price(self):
        return self.whosale_price

    def get_quantity(self):
        if self.quantity == None:
            self.quantity = 0
        return self.quantity

    def get_title(self):
        pg = PartGroup.objects.filter(part_number=self.sku, supplier__title=self.brand).first()
        product_title = pg.part.title
        return product_title

    def __str__(self):
        return "%s %s" % (self.brand, self.sku)

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


# def get_price(product, user=None):
#     pp = ProductPrice.objects.filter(product=product).first()
#
#     if not user:
#         try:
#             return pp.retail_price
#         except:
#             return -1
#
#     try:
#         discount = Profile.objects.get(user=user).discount.discount
#         price = pp.retail_price - round((pp.retail_price * discount / 100), 2)
#         return price
#     except Exception:
#         pass
#
#     try:
#         group = user.groups.all()[0]
#         group = group.pk
#         if group == PriceGroup.RETAIL.value:
#             return pp.retail_price
#         elif group == PriceGroup.OPT1.value:
#             return pp.price_1
#         elif group == PriceGroup.OPT2.value:
#             return pp.price_2
#         elif group == PriceGroup.OPT3.value:
#             return pp.price_3
#         elif group == PriceGroup.OPT4.value:
#             return pp.price_4
#     except Exception:
#         pass
#
#     return -1


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
                # print(product)
                # print(group_id)
                part.part_group.part.price = product.get_price(user=user)
                part.part_group.part.product_id = product.id
                part.part_group.part.quantity = product.get_quantity()
        if not hasattr(part.part_group.part, 'price'):
            part.part_group.part.price = -1
    part_analog_data = sorted(data, key=lambda x: x.part_group.part.price, reverse=True)
    # for pa in part_analog_data:
    #     print(pa.part_group.part.pk)
    return part_analog_data


number_re = re.compile('[^a-zA-Z0-9]+')


def clean_number(number):
    return number_re.sub('', number)
