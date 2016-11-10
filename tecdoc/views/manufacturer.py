from django.views.generic import ListView, DetailView

from tecdoc.models.common import Manufacturer


class ManufacturerList(ListView):
    queryset = Manufacturer.objects.all().distinct()


class ManufacturerView(DetailView):
    model = Manufacturer
    pk_url_kwarg = 'mnf_id'
