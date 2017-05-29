import datetime
import os
import threading

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from djangocms_file.models import Folder, File

from avtoresurs_new.settings import DIR, EMAIL_NOREPLY, EMAIL_TO, EMAIL_BCC, EMAIL_NOREPLY_LIST, MEDIA_URL, MEDIA_ROOT
from bonus.bonus_importer import csv_worker
from bonus.models import Bonus
from profile.models import Profile
from shop.models.product import clean_number, Product, ProductPrice
from tecdoc.models import PartAnalog


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


def parse_clients(data):
    """ parse file from media and update profile info
     :arg data is splitted lines from file """
    protocol = []
    good = 0
    bad = 0
    for line in data[1:]:
        try:
            row = line.split(';')
            login = row[0].replace('ЦБ', 'cl')
            profile = Profile.objects.get(user__username=login)
            profile.fullname = row[1]
            profile.vip_code = row[2].strip()
            profile.points = float(row[3].replace(',', '.'))
            profile.save()

            protocol.append('%s - %s' % ('OK', line.strip()))
            good += 1
        except Exception as e:
            protocol.append('%s - %s, %s' % ('ERROR', line, e))
            bad += 1
    return protocol, good, bad


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


def add_product(data, interval, report_product, report_price):
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
        thread = threading.Thread(target=add_product, args=(data, interval, report_product, report_price))
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


def bonus_load(filename):
    """ import bonuses from csv file """
    rows = csv_worker.get_rows_list_from_csv(csv_file_path=filename, encoding='cp1251', delimiter=';')
    error_rows = []
    data = None
    with open(filename, 'r', encoding='cp1251') as fin:
        data = fin.read().splitlines(True)
    for row in data[1:]:
        print('%s' % row)
    exit()
    for row in data[1:]:
        # print(row)
        try:
            # try to get data from row
            item_code = row[0]
            item_name = row[1]
            item_bonus_price = row[2]
            print('item_bonus_price: %s' % item_bonus_price)
            # try:
            int(item_bonus_price)
            print(item_code, item_name, item_bonus_price)
            # TODO write code below:
            # next we should create an object from this fields (django model) and save it, or return dict
            bonus, created = Bonus.objects.get_or_create(id_1c=item_code)
            bonus.model = item_name
            bonus.price = item_bonus_price
            bonus.save()
            # except ValueError:
            #     print("Wrong format in bonus row. This will be reported.")
            #     error_rows.append(row)

        except IndexError:
            error_rows.append(row)
            print("File '%s': wrong columns markup. This will be reported.\nrow=%s" % (filename, row))
    return HttpResponseRedirect('/service/bonus_load/')
