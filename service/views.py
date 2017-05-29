from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from service.parser.parser import get_filename, price_load, bonus_load, parse_clients, point_load


class ServiceMainViev(TemplateView):
    template_name = 'service/service_main.html'


class PointLoad(TemplateView):
    template_name = 'service/point_load.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/point_load/')

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        url = point_load(filename)
        return HttpResponseRedirect(url)


class ProductLoad(TemplateView):
    template_name = 'service/product_load.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/product_load/')

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        url = price_load(filename)
        return HttpResponseRedirect(url)


class BonusLoad(TemplateView):
    template_name = 'service/bonus_load.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/bonus_load/')

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        url = bonus_load(filename)
        return HttpResponseRedirect(url)
