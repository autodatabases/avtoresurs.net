import csv

import datetime
import os
import threading

from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
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
from shop.models.product import Product, ProductPrice, clean_number

# Create your views here.
# from tecdoc.models import Part
from tecdoc.models import Part, PartAnalog


def add(data, interval, report_product, report_price):
    for idx, line in enumerate(data[interval[0]:interval[1]]):
        try:
            row = line.split(';')
            part_analog = None
            brand = row[1]
            sku = row[0]
            quantity = row[2]
            prices = [row[3], row[4], row[5], row[6], row[7]]
            if not prices[4]:
                prices[4] = 0
            # print(prices)
            clean_sku = clean_number(sku)
            part_analog = PartAnalog.objects.filter(search_number=clean_sku)
            product, created = Product.objects.get_or_create(sku=sku, brand=brand)
            product.quantity = quantity
            product.save()

            # product_price = ProductPrice(
            #     product=product,
            #     retail_price=prices[0],
            #     price_1=prices[1],
            #     price_2=prices[2],
            #     price_3=prices[3],
            #     price_4=prices[4]
            # )
            product_price, created = ProductPrice.objects.get_or_create(product=product)
            product_price.retail_price = prices[0]
            product_price.price_1 = prices[1]
            product_price.price_2 = prices[2]
            product_price.price_3 = prices[3]
            product_price.price_4 = prices[4]
            # print(product_price)
            product_price.save()
            if not prices[0]:
                report_price.append('Строка № %s не указана цена товара. [%s]' % (idx, line))
            if not part_analog:
                report_product.append('Строка № %s не найдено соответсвие в TECDOC. [%s]' % (idx, line))
        except:
            report_product.append('Строка № %s КРИТИЧЕСКАЯ ОШИБКА. [%s]' % (idx, line))


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


def get_intervals(interval, THREADS, end_idx):
    intervals = list()
    intervals.append([1, interval])
    for idx in range(1, THREADS + 1):
        intervals.append([interval * idx, interval * (idx + 1)])
    intervals[0][0] = 1
    intervals[THREADS - 1][1] = end_idx
    return intervals

    # [
    #     [1, interval],
    #     [interval, interval * 2],
    #     [interval * 2, interval * 3],
    #     [interval * 3, interval * 4],
    #     [interval * 4, interval * 5],
    #     [interval * 5, interval * 6],
    #     [interval * 6, interval * 7],
    #     [interval * 7, interval * 8],
    #     [interval * 8, interval * 9],
    #     [interval * 9, len(data)]
    # ]


class ProductLoader(TemplateView):
    template_name = 'load.html'

    # def get(self, request):
    #     pass

    def post(self, request):
        # file = 'NewsAuto2.csv'
        # with open(file, 'r', encoding='cp1251') as fin:
        #     data = fin.read().splitlines(True)
        # date = datetime.datetime.now()

        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/profile/point_load/')

        date = datetime.datetime.now()
        filename = os.path.join('csv', 'auto', date.strftime('%Y'), date.strftime('%m'),
                                self.request.FILES['file'].name)

        path = default_storage.save(filename, ContentFile(file.read()))
        file.close()

        with open('media/' + path, 'r', encoding='cp1251') as fin:
            data = fin.read().splitlines(True)

        report_product = ['Прококол загрузки файла товаров от %s' % date]
        report_price = ['Прококол загрузки цен от %s' % date]

        # print(data[0:50])
        # exit()

        THREADS = 40
        list_len = len(data)
        interval = list_len // THREADS
        intervals = get_intervals(interval, THREADS, list_len)

        # print(intervals[0])
        # add(data, intervals[0], report_product, report_price)


        threads = list()
        for interval in intervals:
            thread = threading.Thread(target=add, args=(data, interval, report_product, report_price))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        error_file_path = 'error.log'
        with open(error_file_path, 'w+') as error_file:
            for item in report_product:
                error_file.write('\r\n%s' % item)

        error_file_price_path = 'error_price.log'
        with open(error_file_price_path, 'w+') as error_file_price:
            for item in report_price:
                error_file_price.write('\r\n%s' % item)

        return HttpResponse('OK')


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
