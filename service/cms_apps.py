from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class ServiceApphook(CMSApp):
    app_name = 'service'
    name = _("Service Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ['service.urls']


apphook_pool.register(ServiceApphook)
