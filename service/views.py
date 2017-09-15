from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from shop.models.storage import Storage
from service.parser.custom_cross import CustomCross
from service.parser.parser import get_filename, bonus_load, parse_clients, point_load, ProductLoader


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

    def get_context_data(self, **kwargs):
        context = super(ProductLoad, self).get_context_data()
        storages = Storage.objects.filter(active=True)
        context['storages'] = storages

        return context

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/product_load/')

        storage_id = self.request.POST.get('storage')
        filename = self.request.FILES['file'].name
        new_filename = get_filename(self.request.FILES['file'].name)
        file_path = default_storage.save(new_filename, ContentFile(file.read()))
        file.close()
        ProductLoader(file_path, storage_id, filename)

        return HttpResponseRedirect('/service/product_load/')


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


class CustomCrossView(TemplateView):
    template_name = 'service/custom_cross.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/custom_cross/')

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        cc = CustomCross(filename)
        cc.parse_file()
        cc.make_suppliers()
        cc.make_products()
        return HttpResponseRedirect('/service/custom_cross/')
