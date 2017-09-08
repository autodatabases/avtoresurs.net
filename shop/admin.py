from django.contrib import admin

# Register your models here.
from shop.models.cart import Cart
from shop.models.order import Order
from shop.models.product import Product
from shop.models.storage import Storage

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Storage)
