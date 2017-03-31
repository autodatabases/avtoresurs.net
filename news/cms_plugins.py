from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import PostPlugin
from django.core.urlresolvers import reverse, NoReverseMatch




@plugin_pool.register_plugin
class PostPlugin(CMSPluginBase):
    module = ("Контент")
    name = ("Новости")
    render_template = 'news/main_news_list.html'
    model = PostPlugin

    def render(self, context, instance, placeholder):
        posts = instance.get_posts()
        context.update({
            'instance': instance,
            'posts': posts,
        })
        return context


