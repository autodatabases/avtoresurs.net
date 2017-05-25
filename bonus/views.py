from django.views.generic import ListView

from bonus.models import Bonus


class BonusPageView(ListView):
    """ This view response for bonus items page and return page with all items """
    template_name = 'bonus/bonus_items.html'
    model = Bonus
    paginate_by = 4

