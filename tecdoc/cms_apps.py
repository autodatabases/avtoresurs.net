from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class TecdocApphook(CMSApp):
    app_name = 'tecdoc'
    name = _("TECDOC catalogue")

    def get_urls(self, page=None, language=None, **kwargs):
        return ['tecdoc.urls']


apphook_pool.register(TecdocApphook)
