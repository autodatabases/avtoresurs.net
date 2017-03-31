from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class BonusApphook(CMSApp):
    app_name = 'bonus'
    name = _("bonus")

    def get_urls(self, page=None, language=None, **kwargs):
        return ['bonus.urls']


apphook_pool.register(BonusApphook)
