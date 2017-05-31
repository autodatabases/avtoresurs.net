import datetime
import os
import threading

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from filer.models import File
from filer.models.foldermodels import Folder

from avtoresurs_new.settings import DIR, EMAIL_NOREPLY, EMAIL_TO, EMAIL_BCC, EMAIL_NOREPLY_LIST, MEDIA_URL, MEDIA_ROOT

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
    new_filename = os.path.join(MEDIA_ROOT, DIR['CSV'], dir, year, month, day, filename)
    return new_filename


def save_protocol(folder_name, protocol_path, protocol_filename, protocol_string):
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    hour = date.strftime('%H')
    minute = date.strftime('%M')

    folder, created = Folder.objects.get_or_create(name=folder_name)
    subfolder_year, created = Folder.objects.get_or_create(name=date.strftime('%Y'), parent=folder)
    subfolder_month, created = Folder.objects.get_or_create(name=date.strftime('%m'), parent=subfolder_year)

    protocol_file = File(file=protocol_path)
    protocol_file.name = protocol_filename
    protocol_file.folder = subfolder_month

    subject = 'Протокол загрузки каталога бонусов от %s.%s.%s %s:%s' % (year, month, day, hour, minute)
    body = 'Протокол загрузки каталога бонусов в приложении'
    email = EmailMessage(
        subject,
        body,
        EMAIL_NOREPLY,
        EMAIL_TO,
        EMAIL_BCC,
        reply_to=EMAIL_NOREPLY_LIST,
        headers={},
    )

    email.attach('Priz.txt', protocol_string, 'text/plain')
    email.send()


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

        try:
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
            product_price.save()

            if not prices[0]:
                report_price.append('Строка № %s не указана цена товара. [%s]' % (line_number, line))
            if not part_analog:
                report_product.append(
                    'Строка № %s не найдено соответсвие в TECDOC. [%s]' % (line_number, line.split()))
                # except:
                #     report_product.append('Строка № %s КРИТИЧЕСКАЯ ОШИБКА. [%s]' % (line_number, line.split()))
        except Exception as e:
            report_product.append("Строка № %s. Проверьте корректность строки [%s]" % (line_number, line.split()))


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

    error_filename = '%s_%s_%s_%s_%s_error.txt' % (year, month, day, hour, minute)
    error_file = os.path.join(DIR['CSV'], DIR['PRICE'], DIR['LOG'], year, month, day, error_filename)
    for item in report_product:
        report_product_str += '\r\n%s' % item
    error_file_path = default_storage.save(error_file, ContentFile(report_product_str))

    error_price_filename = '%s_%s_%s_%s_%s_error_price.txt' % (year, month, day, hour, minute)
    error_price_file = os.path.join(DIR['CSV'], DIR['PRICE'], DIR['LOG'], year, month, day, error_price_filename)
    for item in report_price:
        report_price_str += '\r\n%s' % item
    error_price_file_path = default_storage.save(error_price_file, ContentFile(report_price_str))

    folder, created = Folder.objects.get_or_create(name='NewsAuto')
    subfolder_year, created = Folder.objects.get_or_create(name=year, parent=folder)
    subfolder_month, created = Folder.objects.get_or_create(name=month, parent=subfolder_year)

    error_file = File(file=error_file_path)
    error_file.name = error_filename
    error_file.folder = subfolder_month
    error_file.save()

    error_price = File(file=error_price_file_path)
    error_price.name = error_price_filename
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

    email.attach(error_filename, report_product_str, 'text/plain')
    email.attach(error_price_filename, report_price_str, 'text/plain')
    email.send()

    return MEDIA_URL + error_file_path


def import_bonuses(filename):
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    hour = date.strftime('%H')
    minute = date.strftime('%M')

    with open(filename, 'r', encoding='cp1251') as file_price:
        data = file_price.read().splitlines(True)
    file_price.close()

    good = 0
    bad = 0
    protocol_bad = ''
    protocol_good = ''
    for line in data[1:]:
        row = line.split(';')
        try:
            bonus_code = row[0]
            bonus_title = row[1]
            print(bonus_title)
            bonus_price = int(row[2])
            print(bonus_price)
            bonus, created = Bonus.objects.get_or_create(id_1c=bonus_code)
            bonus.title = bonus_title
            bonus.price = bonus_price
            bonus.save()
            good += 1
            protocol_good += '%s %s\n' % (line, 'Принят')
        except Exception as error:
            bad += 1
            protocol_bad += '%s %s (%s)\n' % (line, 'Возникла ошибка', error)

    protocol = 'Протокол приема каталога бонусов от %s.%s.%s %s:%s\n' % (day, month, year, hour, minute)
    protocol += 'Всего обработано - %s, из них принято - %s, с ошибкой - %s\n\n' % (good + bad, good, bad)
    protocol += protocol_good
    protocol += protocol_bad

    protocol_filename = '%s_%s_%s_%s_%s_priz.txt' % (year, month, day, hour, minute)
    protocol_path = os.path.join(DIR['CSV'], DIR['BONUS'], DIR['LOG'], year, month, protocol_filename)
    # print(protocol_path)
    protocol_path = default_storage.save(protocol_path, ContentFile(protocol.encode('utf-8')))

    folder, created = Folder.objects.get_or_create(name='Priz')
    subfolder_year, created = Folder.objects.get_or_create(name=date.strftime('%Y'), parent=folder)
    subfolder_month, created = Folder.objects.get_or_create(name=date.strftime('%m'), parent=subfolder_year)

    protocol_file = File(file=protocol_path)
    protocol_file.name = protocol_filename
    protocol_file.folder = subfolder_month

    protocol_file.save()

    subject = 'Протокол загрузки бонусного каталога от %s.%s.%s %s:%s' % (year, month, day, hour, minute)
    body = 'Протокол загрузки бонусного каталога в приложении'
    email = EmailMessage(
        subject,
        body,
        EMAIL_NOREPLY,
        EMAIL_TO,
        EMAIL_BCC,
        reply_to=EMAIL_NOREPLY_LIST,
        headers={},
    )

    email.attach(protocol_filename, protocol, 'text/plain')
    email.send()

    return protocol


def bonus_load(filename):
    protocol = import_bonuses(filename)

    return '/service/bonus_load/'
