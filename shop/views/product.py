import re

from collections import Set
from django.views.generic import DetailView

from shop.models.product import Product
# from tecdoc.models import Part
# from tecdoc.models import PartAnalog
# from tecdoc.models import PartGroup
# from tecdoc.models import clean_number
from tecdoc.models import PartAnalog, get_part_analogs

number_re = re.compile('[^a-zA-Z0-9]+')


def clean_number(number):
    return number_re.sub('', number)


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        product = context['product']
        part_analogs = PartAnalog.objects.filter(search_number=clean_number(product.cross_sku))
        # print(clean_number(product.sku))

        parts = set()
        sku = []
        # if part_analogs:
        for pa in part_analogs:
            parts.add(pa.part)
            sku.append(pa.part.sku)
        # print(parts)
        products = Product.objects.filter(sku__in=sku)



        for part in parts:
            print(part)
            brand_name_small = part.supplier.title.lower()
            sku_small = part.sku.lower()
            for product in products:
                if sku_small == product.sku and brand_name_small == product.manufacturer:
                    # print(product)
                    part.price = product.get_price()
                    part.product_id = product.id
                    part.quantity = product.get_quantity()
            if not hasattr(part, 'price'):
                part.price = -1

        # print(parts)
        parts = sorted(parts, key=lambda part: part.price, reverse=True)


        # part = Part.objects.filter(supplier__title=product.manufacturer, sku=product.sku)

        # part = Part.objects.filter(sku=product.sku, supplier__title__iexact=product.manufacturer)
        # if part:
        #     print(part)
        #     part_group = PartGroup.objects.filter(part=part)
        #
        # else:
        #     print('no')

        context['part_analogs'] = parts
        return context
