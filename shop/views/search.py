from distutils.command.clean import clean

from django.views.generic import TemplateView

from shop.models.product import Product, clean_number
from tecdoc.models import PartAnalog, PartGroup


def search_parts(q, user):
    pa = PartAnalog.objects.filter(part_number__iexact=q)
    parts = set()

    for p in pa:
        parts.add(p)


    products = Product.objects.filter(sku__iexact=q)

    for part in parts:
        brand_name = part.supplier.title

        for product in products:
            pg = PartGroup.objects.filter(supplier__title=brand_name, part_number=part.part_number).first()
            title = pg.part.title
            part.title = title
            if clean_number(part.part_number) == clean_number(product.sku) and brand_name == product.brand:
                part.price = product.get_price(user=user)
                part.product_id = product.id
                part.quantity = product.get_quantity()
        if not hasattr(part, 'price'):
            part.price = -1

    part_analogs = sorted(parts, key=lambda part: part.price, reverse=True)
    return part_analogs


class SearchView(TemplateView):
    template_name = 'shop/search_page.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        q = self.request.GET['q']
        context['q'] = q
        context['part_analogs'] = search_parts(q=q, user=self.request.user)
        return context
