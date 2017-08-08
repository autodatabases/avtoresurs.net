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
from tecdoc.models import PartAnalog, PartGroup, Q


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

    subject = 'Протокол загрузки файла Klients.csv от %s.%s.%s %s:%s' % (year, month, day, hour, minute)
    body = 'Протокол загрузки клиентских бонусов Klients.csv в приложении'
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

    protocol = 'Протокол приема файла Priz.csv от %s.%s.%s %s:%s\n' % (day, month, year, hour, minute)
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

    subject = 'Протокол загрузки файла Priz.csv от %s.%s.%s %s:%s' % (year, month, day, hour, minute)
    body = 'Протокол загрузки бонусного каталога Priz.csv в приложении'
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


class ProductLoader:
    """ class for parsing and loading NewsAuto.csv file from 1C """

    # number of threads that will be adding information in DB
    THREADS = 60
    report = list()
    report_text = ''

    def __init__(self, filename):
        self.date = self.get_date()
        self.data = self.parse_file(filename)
        self.product_load()
        self.report_text = self.get_report()
        self.save_report()

    def get_date(self):
        """ get date and formatting string"""
        date = datetime.datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
        date = {
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute
        }
        return date

    def parse_file(self, filename):
        """ parsing NewsAuto.csv and returning list """
        with open(filename, 'r', encoding='cp1251') as file_price:
            data = file_price.read().splitlines(True)
        file_price.close()
        return data[1:]

    def get_intervals(self):
        """ method for generating intervals depending of the value SELF.THREADS """
        end_idx = len(self.data)
        interval = end_idx // self.THREADS
        # print(interval)
        # print(end_idx)
        intervals = list()
        # intervals.append([0, interval])
        for idx in range(0, self.THREADS):
            start = (interval * idx + idx)
            end = interval * (idx + 1) + idx
            if end >= end_idx:
                intervals.append([start, end_idx])
                break
            intervals.append([start, end])

        # last_interval_start = 0
        # intervals.append([last_interval_start, end_idx])
        print(intervals)
        return intervals

    def product_load(self):
        """ method for splitting DATA in threads"""
        intervals = self.get_intervals()
        threads = list()

        # self.add_product([0, len(self.data)])

        for interval in intervals:
            thread = threading.Thread(target=self.add_product, args=(self.data, interval))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def add_product(self, data, interval, offset=2):
        """ main logic of searching and inserting product and product price """
        for idx, line in enumerate(data[interval[0]:(interval[1])]):
            range = interval[1] - interval[0]
            # print(range)
            line_number = interval[0] + offset + idx
            # line_number = (range * idx) + idx
            try:
                # try:
                row = line.split(';')
                sku = row[0]
                brand = row[1]
                quantity = row[2]
                prices = [
                    row[3].replace(',', '.'),
                    row[4].replace(',', '.'),
                    row[5].replace(',', '.'),
                    row[6].replace(',', '.'),
                    row[7].replace(',', '.'),
                    # row[8].replace(',', '.'),
                ]
                try:
                    prices[1]
                except:
                    prices.append(0)
                try:
                    prices[2]
                except:
                    prices.append(0)
                try:
                    prices[3]
                except:
                    prices.append(0)
                try:
                    prices[4]
                except:
                    prices.append(0)
                # try:
                #     prices[5]
                # except:
                #     prices.append(0)
                # print(prices)
                clean_sku = clean_number(sku)
                part_analog = PartGroup.objects.filter(Q(part_number=clean_sku) | Q(part_number=sku))
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
                    # price_5=prices[5]
                )
                product_price.save()

                if not prices[0]:
                    self.report.append('%s. не указана цена товара в рознице. %s' % (line_number, line))
                if not part_analog:
                    self.report.append(
                        '%s. не найдено соответсвие в TECDOC. %s' % (line_number, line))
            except Exception as e:
                # print("%s. Проверьте корректность строки [%s]" % (line_number, line))
                self.report.append("%s. Проверьте корректность строки [%s]" % (line_number, line))

    def get_report(self):
        """ method for generating report """
        self.report = sorted(self.report)
        report = ('Прококол загрузки файла товаров от %s.%s.%s %s:%s\r\n' % (
            self.date['day'],
            self.date['month'],
            self.date['year'],
            self.date['hour'],
            self.date['minute'],
        ))
        total_products = len(self.data)
        bad = len(self.report)
        good = total_products - bad
        report += 'Всего обработано - %s, из них принято - %s, с ошибкой - %s\r\n' % (total_products, good, bad)
        for item in self.report:
            report += item
        return report

    def save_report(self):
        """ method for saving report to server, to DB and sending to admins email"""
        report_filename = '%s_%s_%s_%s_%s_NewsAuto.txt' % (
            self.date['year'],
            self.date['month'],
            self.date['day'],
            self.date['hour'],
            self.date['minute'])
        report_file = os.path.join(
            DIR['CSV'],
            DIR['PRICE'],
            DIR['LOG'],
            self.date['year'],
            self.date['month'],
            self.date['day'],
            report_filename)
        report_file_path = default_storage.save(report_file, ContentFile(self.report_text))

        folder, created = Folder.objects.get_or_create(name='NewsAuto')
        subfolder_year, created = Folder.objects.get_or_create(name=self.date['year'], parent=folder)
        subfolder_month, created = Folder.objects.get_or_create(name=self.date['month'], parent=subfolder_year)
        report_file = File(file=report_file_path)
        report_file.name = report_filename
        report_file.folder = subfolder_month
        report_file.save()
        self.send_email(report_filename)

    def send_email(self, report_filename):
        subject = 'Протокол загрузки файла NewsAuto.csv из 1С от %s.%s.%s %s:%s' % (
            self.date['year'],
            self.date['month'],
            self.date['day'],
            self.date['hour'],
            self.date['minute']
        )
        body = 'Протокол в приложении'
        email = EmailMessage(
            subject,
            body,
            EMAIL_NOREPLY,
            EMAIL_TO,
            EMAIL_BCC,
            reply_to=EMAIL_NOREPLY_LIST,
            headers={'Message-ID': 'foo'},
        )

        email.attach(report_filename, self.report_text, 'text/plain')
        email.send()
