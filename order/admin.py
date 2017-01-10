from django.contrib import admin

from .models import UserCheckout, Order

admin.site.register(UserCheckout)
# admin.site.register(UserAddress)
admin.site.register(Order)