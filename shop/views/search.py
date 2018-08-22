from distutils.command.clean import clean

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

from shop.models.product import Product, clean_number, get_analogs, get_products, ProductTypes
from tecdoc.models import Part, Q, PartAnalog, PartCross, Supplier, PartProduct
import urllib.parse


class SearchView(TemplateView):
    template_name = 'shop/search_page.html'
    model = Part

    # def get_queryset(self):
    #     q = self.request.GET['q']
    #     query = q
    #     clean_query = clean_number(query)
    #     parts = Part.objects.filter(clean_part_number=clean_query)
    #     return parts

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        q = self.request.GET['q']
        clean_query = clean_number(q)
        parts = Part.objects.filter(clean_part_number=clean_query)
        batteries = Product.get_products(product_type=ProductTypes.Battery).filter(sku=clean_query)
        context.update({
            'q': q,
            'parts': parts,
            'batteries': batteries
        })
        return context


class SearchDetailView(ListView):
    template_name = 'shop/search_detail_page.html'
    context_object_name = 'partproduct_list'

    def get_queryset(self):
        part_number = self.request.GET['part']
        clean_part_number = clean_number(part_number)

        brand = self.request.GET['brand']
        supplier = Supplier.objects.get(title=brand)

        analogs = get_analogs(clean_part_number=clean_part_number, supplier=supplier, user=self.request.user)
        if analogs:
            return analogs

        # if we are here, than we have not analogs, try to search directly in productss
        return get_products(supplier=supplier, clean_part_number=clean_part_number)

    def get_context_data(self, **kwargs):
        context = super(SearchDetailView, self).get_context_data()
        part_number = self.request.GET['part']
        brand = self.request.GET['brand']
        context['part_number'] = part_number
        context['brand'] = brand
        return context
