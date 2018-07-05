from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from main.models import GoodItemModelPlugin, ProposalModelPlugin


class GoodItemPlugin(CMSPluginBase):
    model = GoodItemModelPlugin
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


plugin_pool.register_plugin(GoodItemPlugin)
plugin_pool.register_plugin(ProposalPlugin)
