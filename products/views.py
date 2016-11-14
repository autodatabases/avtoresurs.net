from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q

from tecdoc.models import Part
from tecdoc.models import PartAnalog, PartGroup
from tecdoc.models import PartTypeGroupSupplier
from .models import Product


# Create your views here.


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = context['product']
        part = Part.objects.filter(supplier__title=product.manufacturer, sku=product.sku)
        print(part)


        return context


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        # context['now'] = timezone.now()
        context["query"] = self.request.GET.get("q")
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(manufacturer__icontains=query) |
                Q(sku__icontains=query)
                # Q(sku_icontains=query)
            )
        return qs

# def product_detail_view_func(request, id=1):
#     product_instance = get_object_or_404(Product, id=id)
#     template = 'products/product_detail.html'
#     context = {
#         'object': product_instance
#     }
#     return render(request, template, context)
