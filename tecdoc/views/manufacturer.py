from django.views.generic import ListView, DetailView

from tecdoc.models.manufacturer import Manufacturer

class ManufacturerList(ListView):
    queryset = Manufacturer.objects.manufacturers().distinct()


class ManufacturerView(DetailView):
    model = Manufacturer
    pk_url_kwarg = 'mnf_id'

    queryset = Manufacturer.objects.manufacturers().distinct()



    # def get_context_data(self, **kwargs):
    #     context = super(ManufacturerView, self).get_context_data(**kwargs)
    #     return context
