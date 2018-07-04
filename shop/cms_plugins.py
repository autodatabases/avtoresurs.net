from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse, NoReverseMatch

from shop.models.shop import ShopPlugin


@plugin_pool.register_plugin
class ShopPlugin(CMSPluginBase):
    module = ("Контент")
    name = ("Магазин")
    render_template = 'shop/base_shop.html'
    model = ShopPlugin

    def render(self, context, instance, placeholder):
        shops = instance.get_shops()
        context.update({
            'instance': instance,
            'shops': shops,
        })
        return context
