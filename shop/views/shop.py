from django.views.generic import TemplateView


class ShopIndexView(TemplateView):
    template_name = 'shop/shop_index.html'
