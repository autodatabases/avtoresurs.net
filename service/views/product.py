from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.core.files.storage import default_storage
from service.parser.parser import get_filename
from service.parser.product import ProductLoader

from shop.models import Storage


@method_decorator(staff_member_required, name='dispatch')
class ProductView(TemplateView):
    template_name = 'service/product_load.html'

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data()
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
