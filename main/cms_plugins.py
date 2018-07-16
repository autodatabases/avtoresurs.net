from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from main.models import ArrivalItemModelPlugin, ProposalModelPlugin, StoreAddressModelPlugin, StockModelPlugin


class ArrivalItemPlugin(CMSPluginBase):
    model = ArrivalItemModelPlugin
    module = ('Контент')
    name = ('Поступление товара')
    render_template = 'main/includes/goods_receipt.html'

    def render(self, context, instance, placeholder):
        goods = instance.get_goods()
        context.update({
            'instance': instance,
            'goods': goods
        })
        return context


class ProposalPlugin(CMSPluginBase):
    model = ProposalModelPlugin
    module = ('Контент')
    name = ('Лучшее предложение')
    render_template = 'main/includes/proposal.html'


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


class StockPlugin(CMSPluginBase):
    model = StockModelPlugin
    module = ('Контент')
    name = ('Акция на главной странице')
    render_template = 'main/includes/stock.html'


plugin_pool.register_plugin(ArrivalItemPlugin)
plugin_pool.register_plugin(ProposalPlugin)
plugin_pool.register_plugin(StoreAddressPlugin)
plugin_pool.register_plugin(StockPlugin)
