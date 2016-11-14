from django.views.generic import DetailView

from shop.models.product import Product


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = context['product']
        # part = Part.objects.filter(supplier__title=product.manufacturer, sku=product.sku)
        # print(part)
        return context
