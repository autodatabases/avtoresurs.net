import csv

from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.http import HttpResponse
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
from tecdoc.models import Part


class MainPageView(TemplateView):
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data()
        news = Post.objects.all()[:6]
        context['news'] = news
        slides = Slider.objects.all()
        context['slides'] = slides
        return context


class AboutView(TemplateView):
    template_name = 'about_view.html'


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


class ProductLoader(TemplateView):
    template_name = 'load.html'

    def get(self, request):
        path = 'NewsAuto.csv'
        report = []

        with open(path, 'r', encoding='cp1251') as f:
            data = f.read().splitlines(True)

        for idx, line in enumerate(data[1:]):
            row = line.split(';')
            created = ''
            try:
                brand = row[1]
                sku = row[0].replace(' ', '')
                quantity = row[2]
                retail_price = row[3]
                price_1 = row[4]
                price_2 = row[5]
                price_3 = row[6]
                price_4 = row[7]
                print('%s %s %s %s %s %s %s %s' % (sku, brand, quantity, retail_price, price_1, price_2, price_3, price_4))
            except:
                pass
        #     try:
        #         created = Product.objects.get_or_create(
        #             sku=row[0].lower().replace(" ", ""),
        #             manufacturer=row[1].lower(),
        #         )
        #         product = created[0]
        #         # print(product)
        #         product.title = row[2].lower()
        #         product.cross_sku = row[3].lower()
        #         product.quantity = row[4].lower()
        #         product.active = True
        #         product.retail_price = row[5].lower()
        #         product.whosale_price = row[6].lower()
        #         product.save()
        #
        #         part = Part.objects.filter(sku__iexact=product.sku, supplier__title__iexact=product.manufacturer)
        #         if not part:
        #             error_string = "product - %s %s %s %s %s - not in TECDOC DB" % (
        #                 idx,
        #                 created.sku,
        #                 created.manufacturer,
        #                 created.title,
        #                 created.cross_sku
        #             )
        #             report.append(error_string)
        #     except:
        #         pass
        #
        # report.append("File load succesfully")
        # if report:
        #     error_file_path = 'error.log'
        #     report_log = ''
        #     for error_line in report:
        #         error_line += '\n'
        #         report_log += error_line
        #     with open(error_file_path, 'w+') as error_file:
        #         # print(report)
        #         error_file.write(report_log)

        return HttpResponse('OK')

        # for idx, row in enumerate(reader):
        #     created = ''
        #     try:
        #         # print('sku - %s, brand - %s, title - %s, cross - %s , quantity - %s, active - True, price - %s' %
        #         #       (row[0], row[1], row[2], row[3], row[4], row[5]))
        #
        #         created = Product.objects.get_or_create(
        #             sku=row[0].lower().replace(" ", ""),
        #             manufacturer=row[1].lower(),
        #             title=row[2].lower(),
        #             cross_sku=row[3].lower(),
        #             quantity=row[4],
        #             # quantity=10,
        #             active=True,
        #             price=row[5],
        #             # price=455.12,
        #         )
        #         # print(created)
        #         part = Part.objects.filter(sku__iexact=created.sku, supplier__title__iexact=created.manufacturer)
        #         if not part:
        #             error_string = "%s %s %s %s %s" % (
        #                 idx,
        #                 created.sku,
        #                 created.manufacturer,
        #                 created.title,
        #                 created.cross_sku
        #             )
        #             report.append(error_string)
        #     except:
        #         pass
        #
        # if report:
        #     error_file_path = '/home/avto/avto/error.log'
        #     report_log = ''
        #     for error_line in report:
        #         error_line += '\n'
        #         report_log += error_line
        #     with open(error_file_path, 'w+') as error_file:
        #         # print(report)
        #         error_file.write(report_log)


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
