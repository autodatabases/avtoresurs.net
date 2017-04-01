from django.core.paginator import Paginator
from django.shortcuts import render_to_response

from django.views.generic import ListView

from bonus.models import Bonus


class BonusPageView(ListView):
    """ This view response for bonus items page and return page with all items """
    template_name = 'bonus/bonus_items.html'
    model = Bonus
    paginate_by = 4

    # def __init__(self, **kwargs):
    #     super(BonusPageView, self).__init__(**kwargs)
    #     self.object_list = self.get_queryset()

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data()
    #     bonuses = Bonus.objects.all()
    #     paginator = Paginator(bonuses, int(self.paginate_by))
    #     context['bonuses'] = paginator.page(1)
    #     return render_to_response(self.template_name, context=context)
