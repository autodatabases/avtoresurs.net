from django.contrib import admin

# Register your models here.

from .models import Product, ProductImage

admin.site.register(Product)

admin.site.register(ProductImage)