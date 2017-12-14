import os
from collections import Set
from django.views.generic import DetailView

from profile.models import Profile
from shop.models import Storage, ProductPrice
from shop.models.product import Product, clean_number, get_analogs
from tecdoc.models import PartAnalog, Part, PartCriteria, CarType, Image, Supplier, PartApplicability, \
    PartAttribute, Q, PartCross


def check_availability(storage, product_storages):
    for product_storage in product_storages:
        if storage == product_storage.storage:
            return True
    return False


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = context['product']
        product.whosale_price = product.get_price(user=self.request.user)
        product.retail_price = product.get_price()

        supplier = Supplier.objects.get(title=product.brand)
        clean_part_number = product.sku

        context['part_analogs'] = get_analogs(clean_part_number=clean_part_number, supplier=supplier,
                                              user=self.request.user)

        storages = Storage.objects.filter(active=True)
        product_prices = ProductPrice.objects.filter(storage__in=storages, product=product)

        for storage in storages:
            storage.available = check_availability(storage, product_prices)
            storage.product_price = ProductPrice.objects.filter(storage=storage, product=product).first()
            try:
                quantity = range(storage.product_price.quantity)
            except AttributeError:
                quantity = 0
            storage.quantity = quantity

            # print(storage.product_price)

        context['storages'] = storages
        # for storage_price in storage_prices:
        #     print(storage_price)

        return context
