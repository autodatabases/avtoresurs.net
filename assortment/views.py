import os
from django.shortcuts import render

from django.views.generic import ListView

# Create your views here.
from assortment.models import AssortmentItem
from avtoresurs_new import settings
from avtoresurs_new.support_utils import get_brands_images_list


class AssortmentList(ListView):
    paginate_by = 9
    model = AssortmentItem
    template_name = 'assortment/assortment_list.html'

    def get_context_data(self, **kwargs):
        brands = get_brands_images_list()
        return {'brands': brands}
