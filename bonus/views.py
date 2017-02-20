from django.core.paginator import Paginator
from django.shortcuts import render, render_to_response

# Create your views here.

# todo move it to better app; and do not forget to move also template
from django.views.generic import ListView

from bonus.models import Prize


class BonusPageView(ListView):
    """ This view response for bonus items page and return page with all items """
    template_name = 'bonus/bonus_items.html'
    model = Prize
    paginate_by = 3

    def __init__(self, **kwargs):
        super(BonusPageView, self).__init__(**kwargs)
        self.object_list = self.get_queryset()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        bonuses = Prize.objects.all()
        paginator = Paginator(bonuses, int(self.paginate_by))
        context['bonuses'] = paginator.page(1)
        return render_to_response(self.template_name, context=context)

