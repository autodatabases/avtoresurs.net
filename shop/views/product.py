import os
from collections import Set
from django.views.generic import DetailView

from profile.models import Profile
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
        part_number = product.sku

        context['part_analogs'] = get_analogs(part_number=part_number, supplier=supplier, user=self.request.user)

        return context
