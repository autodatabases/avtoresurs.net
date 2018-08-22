from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse, NoReverseMatch

from avtoresurs_new.support_utils import get_brands_images_list
from shop.models import StoragePlugin, BatteryModelPlugin


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
class BatteryPlugin(CMSPluginBase):
    module = ('Магазин')
    name = ('Аккумуляторы')
    render_template = 'shop/includes/battery.html'
    model = BatteryModelPlugin

    def render(self, context, instance, placeholder):
        batteries = instance.batteries
        context.update({
            'batteries': batteries
        })
        return context
