from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import PostPluginModel, Post


class PostPlugin(CMSPluginBase):
    model = PostPluginModel
    module = ("Контент")
    name = ("Новости")
    render_template = 'news/main_news_list.html'

    def render(self, context, instance, placeholder):
        posts = Post.objects.all()[:6]
        context.update({
            'instance': instance,
            'posts': posts,
        })
        return context


plugin_pool.register_plugin(PostPlugin)
