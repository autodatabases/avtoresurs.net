import csv

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
from shop.models.product import Product

# Create your views here.
# from tecdoc.models import Part


class MainPageView(TemplateView):
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data()
        news = Post.objects.all()
        context['news'] = news
        slides = Slider.objects.all()
        context['slides'] = slides
        return context


# class ProductLoader(TemplateView):
#     template_name = 'load.html'
#
#     def get(self, request):
#         get_data = super(ProductLoader, self).get(request)
#         get_data = 0
#         path = '/home/auto/avtoresurs_new/avtoresurs_new/NewsAuto.csv'
#         pass_first_line = True
#
#         report = []
#
#         with open(path) as f:
#             if pass_first_line:
#                 pass_first_line = False
#                 pass
#             reader = csv.reader(f, delimiter=';')
#             for idx, row in enumerate(reader):
#                 created = ''
#                 try:
#                     # print('sku - %s, brand - %s, title - %s, cross - %s , quantity - %s, active - True, price - %s' %
#                     #       (row[0], row[1], row[2], row[3], row[4], row[5]))
#
#                     created = Product.objects.get_or_create(
#                         sku=row[0].lower().replace(" ", ""),
#                         manufacturer=row[1].lower(),
#                         title=row[2].lower(),
#                         cross_sku=row[3].lower(),
#                         quantity=row[4],
#                         # quantity=10,
#                         active=True,
#                         price=row[5],
#                         # price=455.12,
#                     )
#                     # print(created)
#                     part = Part.objects.filter(sku__iexact=created.sku, supplier__title__iexact=created.manufacturer)
#                     if not part:
#                         error_string = "%s %s %s %s %s" % (
#                             idx,
#                             created.sku,
#                             created.manufacturer,
#                             created.title,
#                             created.cross_sku
#                         )
#                         report.append(error_string)
#                 except:
#                     pass
#
#         if report:
#             error_file_path = '/home/auto/avtoresurs_new/avtoresurs_new/error.log'
#             report_log = ''
#             for error_line in report:
#                 error_line += '\n'
#                 report_log += error_line
#             with open(error_file_path, 'w+') as error_file:
#                 print(report)
#                 error_file.write(report_log)
#
#         return get_data


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