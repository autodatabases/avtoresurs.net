from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from shop.models.cart import Cart
from shop.models.product import Product


class UserCheckout(models.Model):
    # email = models.EmailField(unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    # cart = models.ForeignKey(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    products = models.ManyToManyField(Product)
    shipping_total_price = models.DecimalField(decimal_places=2, max_digits=50, default=5.99)
    order_total = models.DecimalField(decimal_places=2, max_digits=50)

    def __str__(self):
        return str(self.cart.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.subtotal
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total


pre_save.connect(order_pre_save, sender=Order)
