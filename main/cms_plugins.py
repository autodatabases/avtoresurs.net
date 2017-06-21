from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import SliderPlugin, PhonePlugin


class SliderPlugin(CMSPluginBase):
    model = SliderPlugin
    module = ('Контент')
    name = ('Слайдер')
    render_template = 'main/includes/slider.html'

    def render(self, context, instance, placeholder):
        slides = instance.get_slides()
        context.update({
            'instance': instance,
            'slides': slides,
        })
        return context

class PhonePlugin(CMSPluginBase):
    model = PhonePlugin
    module = ('Контент')
    name = ('Телефоны')
    render_template = 'main/includes/phones.html'

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
        })
        return context


plugin_pool.register_plugin(SliderPlugin)
plugin_pool.register_plugin(PhonePlugin)
