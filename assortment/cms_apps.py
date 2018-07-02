from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class AssortmentApphook(CMSApp):
    app_name = 'assortment'
    name = _("Assortment application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ['assortment.urls']


apphook_pool.register(AssortmentApphook)
