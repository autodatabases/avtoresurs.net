from distutils.command.clean import clean

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

from shop.models.product import Product, clean_number
from tecdoc.models import Part, Q, PartAnalog, PartCross, Supplier, PartProduct


class SearchView(ListView):
    template_name = 'shop/search_page.html'
    model = Part

    def get_queryset(self):
        q = self.request.GET['q']
        query = q
        clean_query = clean_number(query)
        parts = Part.objects.filter(clean_part_number=clean_query)
        return parts

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        q = self.request.GET['q']
        context['q'] = q
        return context


def get_prices(analogs, user):
    if not analogs:
        return False
    sku_list = list()
    supplier_ids = list()
    for analog in analogs:
        sku_list.append(analog['part_number'])
        supplier_ids.append(analog['supplier'])
    suppliers = Supplier.objects.filter(id__in=supplier_ids)
    products = Product.objects.filter(sku__in=sku_list)
    parts = Part.objects.filter(part_number__in=sku_list, supplier__in=suppliers)

    part_products = list()
    for analog in analogs:
        brand = suppliers.get(id=analog['supplier'])
        sku = analog['part_number']
        price = -1
        quantity = -1
        product_id = None

        try:
            title = parts.filter(part_number=sku, supplier=brand).first().title
        except:
            title = None
        part_product = PartProduct(supplier=brand.title, sku=sku, price=price, quantity=quantity,
                                   product=product_id, title=title)
        for product in products:
            if product.sku == sku and product.brand == brand.title:
                part_product.price = product.get_price(user=user)
                part_product.product = product.id
                part_product.quantity = product.get_quantity()
        part_products.append(part_product)
    return part_products


class SearchDetailView(ListView):
    template_name = 'shop/search_detail_page.html'
    context_object_name = 'partproduct_list'

    def get_queryset(self):
        part_number = self.request.GET['part']
        brand = self.request.GET['brand']
        part_analogs = PartAnalog.objects.filter(part_number=part_number, supplier__title=brand)
        crosses = list()
        for part_analog in part_analogs:
            crosses.append(part_analog.oenbr)

        analogs = PartCross.objects.values('supplier', 'part_number').filter(oenbr__in=crosses).distinct()

        analogs = get_prices(analogs, self.request.user)

        return sorted(analogs, reverse=True)

    def get_context_data(self, **kwargs):
        context = super(SearchDetailView, self).get_context_data()
        part_number = self.request.GET['part']
        brand = self.request.GET['brand']
        context['part_number'] = part_number
        context['brand'] = brand
        return context
