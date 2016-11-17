from django.views.generic import DetailView

from shop.models.product import Product
# from tecdoc.models import Part
# from tecdoc.models import PartAnalog
# from tecdoc.models import PartGroup
# from tecdoc.models import clean_number


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = context['product']
        # part = Part.objects.filter(supplier__title=product.manufacturer, sku=product.sku)

        # part = Part.objects.filter(sku=product.sku, supplier__title__iexact=product.manufacturer)
        # if part:
        #     print(part)
        #     part_group = PartGroup.objects.filter(part=part)
        #
        # else:
        #     print('no')

        parts = []

        context['part_analogs'] = parts
        return context
