from django.db import models
from django.conf import settings
from cart.models import Cart
from django.db.models.signals import pre_save
from decimal import Decimal


# Create your models here.

class UserCheckout(models.Model):
    # email = models.EmailField(unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout)
    shipping_total_price = models.DecimalField(decimal_places=2, max_digits=50, default=5.99)
    order_total = models.DecimalField(decimal_places=2, max_digits=50)

    def __str__(self):
        return str(self.cart.id)


def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.subtotal
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total


pre_save.connect(order_pre_save, sender=Order)
# class Order(models.Model):
#     #cart
#     #user checkout --> required
#     #shipping address
#     #billing address
#     #shipping total
#     #order total
#     #order_id --> custom id
