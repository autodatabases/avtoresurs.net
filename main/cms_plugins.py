from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from main.models import ArrivalItemModelPlugin, ProposalModelPlugin, StoreAddressModelPlugin, StockModelPlugin, \
    PostPlugin




@plugin_pool.register_plugin
class PostPlugin(CMSPluginBase):
    module = ("Контент")
    name = ("Новости")
    render_template = 'main/includes/right_news_list.html'
    model = PostPlugin

    def render(self, context, instance, placeholder):
        posts = instance.get_posts()
        context.update({
            'instance': instance,
            'posts': posts,
        })
        return context


@plugin_pool.register_plugin
class ProposalPlugin(CMSPluginBase):
    model = ProposalModelPlugin
    module = ('Контент')
    name = ('Лучшее предложение')
    render_template = 'main/includes/proposal.html'


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
class StockPlugin(CMSPluginBase):
    model = StockModelPlugin
    module = ('Контент')
    name = ('Акция на главной странице')
    render_template = 'main/includes/stock.html'
