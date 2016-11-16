from django.views.generic import DetailView

from shop.models.product import Product
from tecdoc.models import Part
from tecdoc.models import PartAnalog
from tecdoc.models import clean_number


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = context['product']
        # part = Part.objects.filter(supplier__title=product.manufacturer, sku=product.sku)

        parts = Part

        cross_sku = clean_number(product.cross_sku)
        part_analog = PartAnalog.objects.filter(search_number=cross_sku)
        # print(cross_sku)
        # part_analog = Part.objects.lookup(number=cross_sku)
        part_analog_art_id = set()
        part_analog_sku = set()
        for pa in part_analog:
            try:
                part_analog_art_id.add(pa.part.id)
                part_analog_sku.add(pa.part.sku)
            except:
                pass

        part_analog = PartAnalog.objects.filter(search_number__in=part_analog_sku)
        for pa in part_analog:
            try:
                part_analog_art_id.add(pa.part.id)
                part_analog_sku.add(pa.part.sku)
            except:
                pass

        # part_analog_art_id = list(part_analog_art_id)
        # print(part_analog_art_id)
        # part_analog_sku = list(part_analog_sku)
        # print(part_analog_sku)

        parts = Part.objects.filter(id__in=part_analog_art_id)

        products = Product.objects.filter(sku__in=part_analog_sku)
        for part in parts:
            for product in products:
                if part.sku == product.sku:
                    part.product = product

        context['part_analogs'] = parts
        return context
