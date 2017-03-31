from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import Slide, Slider, SliderPluginModel


class SliderPlugin(CMSPluginBase):
    model = SliderPluginModel
    module = ('Контент')
    name = ('Слайдер')
    render_template = 'main/includes/slider.html'

    def render(self, context, instance, placeholder):
        slides = instance.slider.slide_set.all()
        context.update({
            'instance': instance,
            'slides': slides,
        })
        return context


plugin_pool.register_plugin(SliderPlugin)
