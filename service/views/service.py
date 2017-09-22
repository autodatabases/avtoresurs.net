from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(staff_member_required, name='dispatch')
class ServiceView(TemplateView):
    template_name = 'service/service_main.html'
