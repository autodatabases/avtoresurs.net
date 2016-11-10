from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

class ShopIndexView(TemplateView):
    template_name = 'shop.html'