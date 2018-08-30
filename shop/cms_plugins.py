from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse, NoReverseMatch

from avtoresurs_new.support_utils import get_brands_images_list
from shop.models import StoragePlugin, ProductTypeModelPlugin


@plugin_pool.register_plugin
class ShopPlugin(CMSPluginBase):
    module = ("Контент")
    name = ("Магазин")
    render_template = 'shop/base_shop.html'
    model = StoragePlugin

    def render(self, context, instance, placeholder):
        shops = instance.get_shops()
        brands = get_brands_images_list()
        context.update({
            'instance': instance,
            'shops': shops,
            'brands': brands
        })
        return context


@plugin_pool.register_plugin
class ProductTypePlugin(CMSPluginBase):
    module = ('Магазин')
    name = ('Продукты по категории')
    render_template = 'shop/includes/product_category.html'
    model = ProductTypeModelPlugin
    cache = False

    def render(self, context, instance, placeholder):
        context.update({
            'products': instance.products
        })
        return context
