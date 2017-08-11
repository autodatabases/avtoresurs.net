from distutils.command.clean import clean

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

from shop.models.product import Product, clean_number
from tecdoc.models import Part, Q


def search_parts(q, user):
    query = q
    clean_query = clean_number(query)
    parts = Part.objects.filter(Q(clean_part_number__iexact=clean_query) | Q(part_number__iexact=query))

    # products = Product.objects.filter(Q(sku__iexact=clean_query) | Q(sku__iexact=query))
    # print(query)
    # print(clean_query)
    # print(products)
    # print(parts)

    # no_product = True
    #
    # for part in parts:
    #     brand_name = part.supplier.title
    #
    #     for product in products:
    #         if clean_number(part.part_number) == clean_number(product.sku) and brand_name == product.brand:
    #             part.price = product.get_price(user=user)
    #             part.product_id = product.id
    #             part.quantity = product.get_quantity()
    #             no_product = False
    #         pg = PartGroup.objects.filter(supplier__title=brand_name, part_number=part.part_number).first()
    #         if pg:
    #             title = pg.part.title
    #             part.title = title
    #         if clean_number(part.part_number) == clean_number(product.sku) and brand_name == product.brand:
    #             part.price = product.get_price(user=user)
    #             part.product_id = product.id
    #             part.quantity = product.get_quantity()
    #             no_product = False
    #     if not hasattr(part, 'price'):
    #         part.price = -1
    #
    # part_analogs = sorted(parts, key=lambda part: part.price, reverse=True)
    #
    # if not no_product:
    #     return part_analogs


class SearchView(TemplateView, MultipleObjectMixin):
    template_name = 'shop/search_page.html'
    model = Part

    def get_queryset(self):
        q = self.request.GET['q']
        query = q
        clean_query = clean_number(query)
        print('%s %s', query, clean_query)
        parts = Part.objects.filter(Q(part_number=query) | Q(clean_part_number=clean_query))
        print(parts)
        print(Part.objects.filter(Q(part_number=query) | Q(clean_part_number=clean_query)).query)
        return parts

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        q = self.request.GET['q']
        context['q'] = q
        return context

class SearchDetailView(TemplateView, MultipleObjectMixin):
       template_name = 'shop/search_detail_page.html'

       def 
