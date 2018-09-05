from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from avtoresurs_new.support_utils import get_brands_images_list
from main.models import ProposalModelPlugin, StoreAddressModelPlugin, StockModelPlugin, PostPluginModel


@plugin_pool.register_plugin
class PostPlugin(CMSPluginBase):
    module = ("Контент")
    name = ("Новости")
    model = PostPluginModel

    def render(self, context, instance, placeholder):
        posts = instance.get_posts()
        context.update({
            'instance': instance,
            'posts': posts,
        })
        return context

    def get_render_template(self, context, instance, placeholder):
        return instance.render_template


@plugin_pool.register_plugin
class StoreAddressPlugin(CMSPluginBase):
    model = StoreAddressModelPlugin
    module = ('Контент')
    name = ('Адреса и телефоны')
    render_template = 'main/includes/store_address.html'

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'stores': instance.stores
        })
        return context


@plugin_pool.register_plugin
class ProposalPlugin(CMSPluginBase):
    model = ProposalModelPlugin
    module = ('Контент')
    name = ('Лучшее предложение')
    render_template = 'main/includes/proposal.html'


@plugin_pool.register_plugin
class StockPlugin(CMSPluginBase):
    model = StockModelPlugin
    module = ('Контент')
    name = ('Акция на главной странице')
    render_template = 'main/includes/stock.html'


@plugin_pool.register_plugin
class BrandList(CMSPluginBase):
    module = ('Контент')
    name = ('Лента с брэндами')
    render_template = 'main/plugins/brands_lent.html'
    cache = None

    def render(self, context, instance, placeholder):
        brands = get_brands_images_list()
        context.update({
            'brands': brands
        })
        return context