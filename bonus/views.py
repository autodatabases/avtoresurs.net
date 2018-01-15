import json
import traceback

from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView

from bonus.models import Bonus, UserBonus
from postman.models import STATUS_ACCEPTED, Message
from profile.models import Profile

UNREGISTERED_USER_POINTS = 0
PROTECTED_KEY = 'GsdfklGsdn6305cHdshy'


class BonusPageView(ListView):
    """ This view response for bonus items page and return page with all items """
    template_name = 'bonus/bonus_items.html'
    model = Bonus
    paginate_by = 24

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

    @staticmethod
    def _send_email(subject, body):
        email = EmailMessage(
            subject,
            body,
            'no-reply@avtoresurs.net',
            ['avtoresurs@mail.ru'],
            ['oleg_a@outlook.com'],
            reply_to=['no-reply@avtoresurs.net'],
            headers={'Message-ID': 'foo'},
        )
        email.send()

    @staticmethod
    def _send_private_messages_recipient_and_admin(subject, body, recipient):
        status = STATUS_ACCEPTED
        sender = User.objects.filter(username='admin').first()
        message_user = Message(subject=subject, body=body, sender=sender, recipient=recipient, moderation_status=status)
        message_user.save()
        message_admin = Message(subject=subject, body=body, sender=recipient, recipient=sender,
                                moderation_status=status)
        message_admin.save()

    def post(self, *args, **kwargs):
        error_redirect = JsonResponse("Неизвестная ошибка! Пожалуйста, обратитесь к администратору сайта.", status=503,
                                      safe=False)
        try:
            encoded_data = json.loads(self.request.body.decode('utf-8'))
            bonus_id = encoded_data['bonus']
            bonus = Bonus.objects.get(pk=bonus_id)
            user = self.request.user
            profile = Profile.objects.get(user=user)
            if profile.points >= bonus.price:
                profile.points -= bonus.price
                profile.save()
                UserBonus.objects.create(user=user, bonus=bonus)
                subject = 'Получение товаров по бонусной акции'
                body = 'Пользователь %s получил %s по бонусной акции.' % (user.username, bonus.title)
                self._send_email(subject=subject, body=body)
                self._send_private_messages_recipient_and_admin(subject=subject, body=body, recipient=user)
            else:
                miss_points = bonus.price - profile.points
                return JsonResponse("Недостаточно %s баллов!" % miss_points, status=503, safe=False)
        except Exception as e:
            traceback.print_tb(e)
            return error_redirect

        return JsonResponse("Вы успешно получили '%s'!" % bonus.title, status=200, safe=False)

        # return HttpResponse("Вы успешно получили %s" % bonus_id, status=200)
        # error_redirect = HttpResponse("Во время получения бонуса произошла ошибка!", status=503)
        # try:
        #     bonus_id = self.request.GET.get('bonus_id')
        #     encoded_data = json.loads(self.request.body.decode('utf8'))
        #     user_id = encoded_data['id']
        #     key = encoded_data['key']
        #     bonus = Bonus.objects.get(pk=bonus_id)
        #     user = User.objects.get(pk=user_id)
        #     if key == PROTECTED_KEY:
        #         profile = Profile.objects.get(user=user)
        #         if profile.points >= bonus.price:
        #             profile.points -= bonus.price
        #             profile.save()
        #             UserBonus.objects.create(user=user, bonus=bonus)
        #             subject = 'Получение товаров по бонусной акции'
        #             body = 'Пользователь %s получил %s по бонусной акции.' % (user.username, bonus.title)
        #             self._send_email(subject=subject, body=body)
        #             self._send_private_messages_recipient_and_admin(subject=subject, body=body, recipient=user)
        #         else:
        #             return error_redirect
        #     else:
        #         return error_redirect
        # except Exception as e:
        #     traceback.print_tb(e)
        #     return error_redirect
        # return HttpResponse("Вы успешно получили '%s'!" % bonus.title, status=200)
