from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import AssortmentItemPlugin
from django.core.urlresolvers import reverse, NoReverseMatch


@plugin_pool.register_plugin
class AssortmentPlugin(CMSPluginBase):
    module = ("Контент")
    name = ("Ассортимент")
    render_template = 'assortment/base_assortment.html'
    model = AssortmentItemPlugin

    def render(self, context, instance, placeholder):
        items = instance.get_items()
        context.update({
            'instance': instance,
            'items': items,
        })
        return context
