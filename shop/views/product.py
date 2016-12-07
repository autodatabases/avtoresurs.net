import re
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

        parts = []
        if part_analogs:
            for pa in part_analogs:
                parts.append(pa.part)

        print(parts)
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
