from django.views.generic import DetailView

from tecdoc.models.carmodel import CarModel


class CarModelView(DetailView):
    model = CarModel
    pk_url_kwarg = 'model_id'

    # def get_queryset(self, *args, **kwargs):
    #     print(kwargs)
    #     qs = super(CarModelView, self).get_queryset()
    #     # print(len(qs))
    #     return qs
