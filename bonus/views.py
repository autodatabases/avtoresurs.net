import json
import traceback

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView

from bonus.models import Bonus, UserBonus
from profile.models import Profile

UNREGISTERED_USER_POINTS = 0
PROTECTED_KEY = 'GsdfklGsdn6305cHdshy'


class BonusPageView(ListView):
    """ This view response for bonus items page and return page with all items """
    template_name = 'bonus/bonus_items.html'
    model = Bonus
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(BonusPageView, self).get_context_data()
        try:
            profile = Profile.objects.get(user=self.request.user)
            context['points'] = profile.points
        except TypeError:
            # 'AnonymousUser' have no profile and points
            context['points'] = UNREGISTERED_USER_POINTS
        return context


class BonusObtainView(View):
    """ view for post request to add user bonuses """

    def post(self, *args, **kwargs):
        error_redirect = HttpResponse("Во время получения бонуса произошла ошибка!", status=503)
        try:
            bonus_id = self.request.GET.get('bonus_id')
            print(self.request.body)
            encoded_data = json.loads(self.request.body.decode('utf8'))
            user_id = encoded_data['id']
            key = encoded_data['key']
            bonus = Bonus.objects.get(pk=bonus_id)
            user = User.objects.get(pk=user_id)
            if key == PROTECTED_KEY:
                profile = Profile.objects.get(user=user)
                print(profile.points)
                print(bonus.price)
                if profile.points >= bonus.price:
                    profile.points -= bonus.price
                    profile.save()
                    UserBonus.objects.create(user=user, bonus=bonus)
                else:
                    return error_redirect
            else:
                return error_redirect
        except Exception as e:
            traceback.print_tb(e)
            return error_redirect
        return HttpResponse("Вы успешно получили '%s'!" % bonus.title, status=200)
