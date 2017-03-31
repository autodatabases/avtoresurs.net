from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from avtoresurs_new import settings
from main.forms import ResendActivationEmailForm
from main.models import Slider
from news.models import Post
from registration.forms import User


# Create your views here.

class MainPageView(TemplateView):
    template_name = 'main/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data()
        news = Post.objects.all()[:6]
        context['news'] = news
        slides = Slider.objects.all()
        context['slides'] = slides
        return context


class AboutView(TemplateView):
    template_name = 'main/about_view.html'


class BrandsView(TemplateView):
    template_name = 'brands_view.html'


class AssortmentView(TemplateView):
    template_name = 'assortment_view.html'


class TrucksView(TemplateView):
    template_name = 'trucks_view.html'


class FAQView(TemplateView):
    template_name = 'faq_view.html'


class ServiceStationView(TemplateView):
    template_name = 'service_station_view.html'


class ContactsView(TemplateView):
    template_name = 'contacts_view.html'


class YandexDnsView(TemplateView):
    template_name = 'yandex_dns_view.html'


# todo make CBV
def resend_activation_email(request):
    email_body_template = 'registration/activation_email.txt'
    email_subject_template = 'registration/activation_email_subject.txt'

    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')

    context = Context()

    form = None
    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email, is_active=0)

            if not users.count():
                form._errors["email"] = 'Учетная запись на таком e-mail не найдена или уже зарегистрирована.'

            REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT', 'registration')
            print(REGISTRATION_SALT)
            for user in users:
                activation_key = signing.dumps(
                    obj=getattr(user, user.USERNAME_FIELD),
                    salt=REGISTRATION_SALT,
                )
                context = {}
                context['activation_key'] = activation_key
                context['expiration_days'] = settings.ACCOUNT_ACTIVATION_DAYS
                context['site'] = get_current_site(request)

                subject = render_to_string(email_subject_template,
                                           context)
                # Force subject to a single line to avoid header-injection
                # issues.
                subject = ''.join(subject.splitlines())
                message = render_to_string(email_body_template,
                                           context)
                user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
                context['email'] = form.cleaned_data["email"]
                return render(request, 'registration/resend_activation_email_done.html', context)

    if not form:
        form = ResendActivationEmailForm()

    context.update({"form": form})
    return render(request, 'registration/resend_activation_email_form.html', context)
