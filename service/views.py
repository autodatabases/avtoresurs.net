import datetime
import os
import threading
from django.core.mail import EmailMessage

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
# Create your views here.
from django.views.generic import TemplateView
from filer.models import Folder, File
from io import BytesIO

from avtoresurs_new.settings import MEDIA_ROOT, DIR, MEDIA_URL, EMAIL_NOREPLY, EMAIL_TO, EMAIL_BCC, EMAIL_NOREPLY_LIST
from service.parser.clients import parse_clients
from shop.models.product import clean_number, Product, ProductPrice
from tecdoc.models import PartAnalog


class ServiceMainViev(TemplateView):
    template_name = 'service/service_main.html'


def add(data, interval, report_product, report_price):
    for idx, line in enumerate(data[interval[0]:interval[1]]):
        line_number = idx + interval[0] + 1
        row = line.split(';')
        part_analog = None

        sku = row[0]
        brand = row[1]
        quantity = row[2]
        prices = [row[3], row[4], row[5], row[6], row[7], row[8]]
        if not prices[4]:
            prices[4] = 0
        if not prices[5]:
            prices[5] = 0
        # print(prices)
        clean_sku = clean_number(sku)
        part_analog = PartAnalog.objects.filter(search_number=clean_sku)
        product, created = Product.objects.get_or_create(sku=sku, brand=brand)
        product.quantity = quantity
        product.save()

        product_price = ProductPrice(
            product=product,
            retail_price=prices[0],
            price_1=prices[1],
            price_2=prices[2],
            price_3=prices[3],
            price_4=prices[4],
            price_5=prices[5]
        )
        # product_price, created = ProductPrice.objects.get_or_create(product=product)
        # product_price.retail_price = prices[0]
        # product_price.price_1 = prices[1]
        # product_price.price_2 = prices[2]
        # product_price.price_3 = prices[3]
        # product_price.price_4 = prices[4]
        # print(product_price)
        product_price.save()

        if not prices[0]:
            report_price.append('Строка № %s не указана цена товара. [%s]' % (line_number, line))
        if not part_analog:
            report_product.append(
                'Строка № %s не найдено соответсвие в TECDOC. [%s]' % (line_number, line.split()))
            # except:
            #     report_product.append('Строка № %s КРИТИЧЕСКАЯ ОШИБКА. [%s]' % (line_number, line.split()))


def get_intervals(interval, THREADS, end_idx):
    intervals = list()
    intervals.append([1, interval])
    for idx in range(1, THREADS + 1):
        intervals.append([interval * idx, interval * (idx + 1)])
    intervals[0][0] = 1
    intervals[THREADS - 1][1] = end_idx
    return intervals


def price_load(filename):
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    hour = date.strftime('%H')
    minute = date.strftime('%M')

    with open(filename, 'r', encoding='cp1251') as file_price:
        data = file_price.read().splitlines(True)
    file_price.close()

    report_product_str = ''

    report_product_str += ('Прококол загрузки файла товаров от %s\r\n' % date)
    report_product = list()
    report_price_str = 'Прококол загрузки цен от %s\r\n' % date
    report_price = list()

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

    error_file = 'error_%s_%s_%s_%s_%s.txt' % (year, month, day, hour, minute)
    error_file = os.path.join(DIR['CSV'], DIR['PRICE'], DIR['LOG'], year, month, day, error_file)
    for item in report_product:
        report_product_str += '\r\n%s' % item
    error_file_path = default_storage.save(error_file, ContentFile(report_product_str))

    error_price_file = 'error_price_%s_%s_%s_%s_%s.txt' % (year, month, day, hour, minute)
    error_price_file = os.path.join(DIR['CSV'], DIR['PRICE'], DIR['LOG'], year, month, day, error_price_file)
    for item in report_price:
        report_price_str += '\r\n%s' % item
    error_price_file_path = default_storage.save(error_price_file, ContentFile(report_price_str))

    folder, created = Folder.objects.get_or_create(name='NewsAuto')
    subfolder_year, created = Folder.objects.get_or_create(name=year, parent=folder)
    subfolder_month, created = Folder.objects.get_or_create(name=month, parent=subfolder_year)

    error_file = File(file=error_file_path)
    error_file.name = 'error_%s_%s_%s_%s_%s.txt' % (year, month, day, hour, minute)
    error_file.folder = subfolder_month
    error_file.save()

    error_price = File(file=error_price_file_path)
    error_price.name = 'error_price_%s_%s_%s_%s_%s.txt' % (year, month, day, hour, minute)
    error_price.folder = subfolder_month
    error_price.save()

    subject = 'Протокол загрузки файлов с ценами от %s.%s.%s %s:%s' % (year, month, day, hour, minute)
    body = 'Протоколы в приложении'
    email = EmailMessage(
        subject,
        body,
        EMAIL_NOREPLY,
        EMAIL_TO,
        EMAIL_BCC,
        reply_to=EMAIL_NOREPLY_LIST,
        headers={'Message-ID': 'foo'},
    )

    email.attach('error.txt', report_product_str, 'text/plain')
    email.attach('error_price.txt', report_price_str, 'text/plain')
    email.send()

    return MEDIA_URL + error_file_path


class ProductLoad(TemplateView):
    template_name = 'service/product_load.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/product_load/')

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        url = price_load(filename)
        return HttpResponseRedirect(url)


def point_load(filename):
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    hour = date.strftime('%H')
    minute = date.strftime('%M')

    with open(filename, 'r', encoding='cp1251') as fin:
        data = fin.read().splitlines(True)

    protocol = parse_clients(data)

    protocol_filename = 'protokol_%s_%s_%s_%s_%s.txt' % (year, month, day, hour, minute)
    protocol_path = os.path.join(DIR['CSV'], DIR['KLIENTS'], DIR['LOG'], year, month, protocol_filename)

    protocol_string = 'Загружено - %s, не загружено - %s\n\n' % (protocol[1], protocol[2])
    protocol_string += "\n".join(str(x) for x in protocol[0])
    protocol_bytes = protocol_string.encode('utf-8')
    protocol_path = default_storage.save(protocol_path, ContentFile(protocol_bytes))
    # print(protocol_path)

    folder, created = Folder.objects.get_or_create(name='Klients')
    subfolder_year, created = Folder.objects.get_or_create(name=date.strftime('%Y'), parent=folder)
    subfolder_month, created = Folder.objects.get_or_create(name=date.strftime('%m'), parent=subfolder_year)

    protocol_file = File(file=protocol_path)
    protocol_file.name = protocol_filename
    protocol_file.folder = subfolder_month

    protocol_file.save()

    subject = 'Протокол загрузки клиентских бонусов от %s.%s.%s %s:%s' % (year, month, day, hour, minute)
    body = 'Протокол загрузки клиентских бонусов в приложении'
    email = EmailMessage(
        subject,
        body,
        EMAIL_NOREPLY,
        EMAIL_TO,
        EMAIL_BCC,
        reply_to=EMAIL_NOREPLY_LIST,
        headers={'Message-ID': 'foo'},
    )

    email.attach('Klients.txt', protocol_string, 'text/plain')
    email.send()

    return MEDIA_URL + protocol_path


def get_filename(filename):
    dir = 'default'
    if filename == 'Klients.csv':
        dir = DIR['KLIENTS']
    elif filename == 'NewsAuto.csv':
        dir = DIR['PRICE']
    elif filename == 'Priz.csv':
        dir = DIR['BONUS']
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    clients_filename = os.path.join(MEDIA_ROOT, DIR['CSV'], dir, year, month, day, filename)
    return clients_filename


class PointLoad(TemplateView):
    template_name = 'service/point_load.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/point_load/')

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        url = point_load(filename)
        return HttpResponseRedirect(url)
