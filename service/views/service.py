from django.views.generic import TemplateView


class ServiceViev(TemplateView):
    template_name = 'service/service_main.html'
