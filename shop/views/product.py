import os
from collections import Set
from django.views.generic import DetailView

from profile.models import Profile
from shop.models import Storage, ProductStoragePrice
from shop.models.product import Product, clean_number, get_analogs
from tecdoc.models import PartAnalog, Part, PartCriteria, CarType, Image, Supplier, PartApplicability, \
    PartAttribute, Q, PartCross





class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = context['product']
        product.price = product.get_price(user=self.request.user)
        product.default_price = product.get_price()

        supplier = Supplier.objects.get(title=product.brand)
        clean_part_number = product.sku

        context['part_analogs'] = get_analogs(clean_part_number=clean_part_number, supplier=supplier, user=self.request.user)

        storages = Storage.objects.filter(active=True)
        storage_prices = ProductStoragePrice.objects.filter(storage__in=storages, product=product)
        context['storages'] = storage_prices
        # for storage_price in storage_prices:
        #     print(storage_price)

        return context
