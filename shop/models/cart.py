from decimal import Decimal
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.conf import settings


from shop.models.product import Product


class CartItem(models.Model):
    """ товар в корзине """
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Product)
    storage = models.ForeignKey('Storage')
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "%s %s" % (self.item.__str__(), self.storage.__str__())

    def remove(self):
        return self.item.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    """ метод реализует суммарную стоимость продукта - цена * количество"""
    qty = Decimal(instance.quantity)
    if qty >= 1:
        user = instance.cart.user
        price = instance.item.get_price(user, instance.storage)
        line_item_total = qty * Decimal(price)
        instance.line_item_total = line_item_total


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    """ метод реализует суммарную стоимость всей корзины (ИТОГО корзины)"""
    instance.cart.update_subtotal()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)
post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
    """
        класс Корзина - реализует логику работы корзины, для каждого кастомера - своя
        содержит Product
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(Product, through=CartItem)
    storages = models.ManyToManyField('Storage', through=CartItem)
    subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')

    def __str__(self):
        return "%s %s" % (str(self.id), self.user)

    def update_subtotal(self):
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = subtotal
        self.save()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
