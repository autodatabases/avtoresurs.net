from django.views.generic import DetailView

from tecdoc.models import CarType, CarTypeAttributes
from tecdoc.models.carmodel import CarModel
from tecdoc.models.tree import CarTree


class CarModelView(DetailView):
    model = CarModel
    pk_url_kwarg = 'model_id'


    def get_context_data(self, **kwargs):
        context = super(CarModelView, self).get_context_data()
        carmodel = context.get('carmodel')
        print(carmodel)
        car_types = CarType.objects.all().filter(model=carmodel)
        for car_type in car_types:
            car_type.car_specs = car_type.car_specs()
            print(car_type.car_specs)
        return context
