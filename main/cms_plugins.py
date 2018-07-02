from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from main.models import GoodItemModelPlugin


class GoodItemPlugin(CMSPluginBase):
    model = GoodItemModelPlugin
    module = ('Контент')
    name = ('Поступление товара')
    render_template = 'main/includes/goods_receipt.html'

    def render(self, context, instance, placeholder):
        goods = instance.get_goods()
        context.update({
            'instace': instance,
            'goods': goods
        })
        return context

plugin_pool.register_plugin(GoodItemPlugin)

