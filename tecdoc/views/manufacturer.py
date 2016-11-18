from django.views.generic import ListView, DetailView

from tecdoc.models.manufacturer import Manufacturer
from tecdoc.models.carmodel import CarModel
from django.db import connection

class ManufacturerList(ListView):
    queryset = Manufacturer.objects.all().distinct()


class ManufacturerView(DetailView):
    model = Manufacturer
    pk_url_kwarg = 'mnf_id'

    def get_context_data(self, **kwargs):
        context = super(ManufacturerView, self).get_context_data(**kwargs)
        return context
