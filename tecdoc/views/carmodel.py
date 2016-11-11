from django.views.generic import DetailView

from tecdoc.models import CarModel


class CarModelView(DetailView):
    model = CarModel
    pk_url_kwarg = 'model_id'
