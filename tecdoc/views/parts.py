# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import DetailView, ListView
from django.template.response import TemplateResponse

# from tecdoc.models import Part
# from products.models import Product
from products.models import Product
from tecdoc.models import SectionGroup, Part, PartTypeGroupSupplier, CarType, SearchTree, Manufacturer
# from tecdoc.conf import TecdocConf as tdsettings
# from tecdoc.models.raw_models import LinkGaStr, Articles


class PartList(ListView):
    model = PartTypeGroupSupplier
    template_name = 'tecdoc/part_list.html'

    def get_queryset(self):
        section_id = self.kwargs['section_id']
        type_id = self.kwargs['type_id']
        qs = super(PartList, self).get_queryset().filter(car_type=type_id, part__group__sections=section_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super(PartList, self).get_context_data(**kwargs)
        sku = []
        brand = []
        for part in context['parttypegroupsupplier_list']:
            sku.append(part.part.part.sku)
        products = Product.objects.filter(sku__in=sku)
        # products = []

        # adding price data into parttypegroupsupplier_list
        parts_with_price = []
        parts_without_price = []
        for part in context['parttypegroupsupplier_list']:
            brand_name_small = part.part.part.supplier.title.lower()
            sku_small = part.part.part.sku.lower()
            for product in products:
                if sku_small == product.sku and brand_name_small == product.manufacturer:
                    # print(product)
                    part.part.part.price = product.get_price()
                    part.part.part.product_id = product.id
                    part.part.part.quantity = product.get_quantity()
            if not hasattr(part.part.part, 'price'):
                part.part.part.price = -1
        context['parttypegroupsupplier_list'] = sorted(context['parttypegroupsupplier_list'],
                                                       key=lambda x: x.part.part.price, reverse=True)

        # parts_with_price.extend(parts_without_price)
        type_id = self.kwargs['type_id']
        car_type = CarType.objects.get(id=type_id)
        context['car_type'] = car_type
        context['section'] = SearchTree.objects.get(id=self.kwargs['section_id'])
        return context


class PartView(DetailView):
    model = Part
    template_name = 'tecdoc/part_detail.html'
    pk_url_kwarg = 'part_id'