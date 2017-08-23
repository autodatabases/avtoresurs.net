from django.views.generic import ListView, DetailView

from tecdoc.models.manufacturer import Manufacturer

class ManufacturerList(ListView):
    model = Manufacturer
    pk_url_kwarg = 'mnf_id'

    def get_queryset(self):
        qs = Manufacturer.objects.get_queryset()
        return qs



class ManufacturerView(DetailView):
    model = Manufacturer
    pk_url_kwarg = 'mnf_id'

    # def get_context_data(self, **kwargs):
    #     context = super(ManufacturerView, self).get_context_data(**kwargs)
    #     return context
