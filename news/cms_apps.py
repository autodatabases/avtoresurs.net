from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class PostApphook(CMSApp):
    app_name = 'posts'
    name = _("Posts Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ['news.urls']


apphook_pool.register(PostApphook)
