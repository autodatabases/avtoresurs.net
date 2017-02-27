from django.db import models

# Create your models here.
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class ProductQuerySet(models.query.QuerySet):
    """ класс-фильтр queryset - возвращает только продукты со статусом Active """

    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    """ кастомный менеджер товаров"""

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

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
        self.retail_price = prices[0]
        self.price_1 = prices[1]
        self.price_2 = prices[2]
        self.price_3 = prices[3]
        # self.price_4 = prices[4]
        self.save()

    def get_price(self):
        # print(self.request.user)
        return self.retail_price

    def get_retail_price(self):
        return self.retail_price

    def get_whosale_price(self):
        return self.whosale_price

    def get_quantity(self):
        if self.quantity == None:
            self.quantity = 0
            print(self.quantity)
        return self.quantity

    def __str__(self):
        return "%s %s" % (self.brand, self.sku)

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={'pk': self.id})
        # return "/shop/products/" + str(self.id)

    def add_to_cart(self):
        return "%s?item=%s&qty=1" % (reverse("cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&delete=true" % (reverse("cart"), self.id)


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
