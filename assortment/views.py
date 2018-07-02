from django.shortcuts import render

from django.views.generic import ListView

# Create your views here.
from assortment.models import AssortmentItem


class AssortmentList(ListView):
    paginate_by = 9
    model = AssortmentItem
    template_name = 'assortment/assortment_list.html'
