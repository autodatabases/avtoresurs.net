import datetime
import threading
import collections

from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.db import connection
from filer.models.foldermodels import Folder
from filer.models import File
from avtoresurs_new.settings import DIR, EMAIL_NOREPLY, EMAIL_TO, EMAIL_BCC, EMAIL_NOREPLY_LIST
from shop.models import Storage, Part, Product, ProductPrice, clean_number, os, ProductTypes, ProductCategory
from django.core.files.storage import default_storage


def sort_reports(reports):
    sorted_reports = {}
    for category_key, category_report in reports.items():
        sorted_reports.update({category_key: collections.OrderedDict(sorted(category_report.items()))})
    return sorted_reports


class ProductLoader:
    """ class for parsing and loading NewsAuto.csv file from 1C """

    # number of threads that will be adding information in DB
    THREADS = 40
    report = {}
    bad = 0
    good = 0
    report_text = ''
    # one more index for lice
    ONE_MORE = 1

    def __init__(self, file_path, storage_id, filename):
        self.filename = filename
        self.product_categories = ProductCategory.as_list()
        self.report = {}
        for pc in self.product_categories:
            self.report.update({pc.lower(): {}})
        self.storage = Storage.objects.get(id=storage_id)
        self.date = self.get_date()

        all_products = self.parse_file(file_path)
        parsed_products = self.parse_products(all_products)
        for product_category, products in parsed_products.items():
            self.product_load(products=products, product_category=product_category)

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

    def get_intervals(self, products):
        """ method for generating intervals depending of the value SELF.THREADS """
        end_idx = len(products)
        interval = end_idx // self.THREADS
        intervals = list()
        for idx in range(0, self.THREADS):
            start = (interval * idx + idx)
            end = interval * (idx + 1) + idx
            if end >= end_idx:
                intervals.append([start, end_idx])
                break
            intervals.append([start, end])

        return intervals

    def product_load(self, products, product_category):
        """ method for splitting DATA in threads"""
        intervals = self.get_intervals(products)
        threads = list()

        for interval in intervals:
            thread = threading.Thread(target=self.add_product, args=(products, interval, product_category))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def add_product(self, data, interval, product_category):
        """ main logic of searching and inserting product and product price """
        start_idx = interval[0]
        end_idx = interval[1] + self.ONE_MORE
        for idx, line in enumerate(data[start_idx:end_idx]):
            line = line.strip()
            line_number = interval[0] + idx
            try:
                row = line.split(';')
                sku = row[0]
                clear_sku = clean_number(sku)
                brand = row[1]
                quantity = row[2]

                prices = self.get_prices(row)

                if product_category in self.product_categories:
                    part_tecdoc = True
                elif product_category == ProductCategory.Tecdoc:
                    part_tecdoc = Part.objects.filter(clean_part_number=clear_sku, supplier__title=brand)
                else:
                    part_tecdoc = False

                if part_tecdoc:
                    product, created = Product.objects.get_or_create(sku=clear_sku, brand=brand)
                    product.product_category = product_category
                    product.save()

                    product_price, created = ProductPrice.objects.get_or_create(storage=self.storage, product=product)
                    product_price.quantity = quantity
                    product_price.retail_price = prices.get(0)
                    product_price.price_1 = prices.get(1)
                    product_price.price_2 = prices.get(2)
                    product_price.price_3 = prices.get(3)
                    product_price.price_4 = prices.get(4)
                    product_price.price_5 = prices.get(5)
                    product_price.price_6 = prices.get(6)
                    product_price.save()

                    self.report[product_category][line_number] = 'Успешно добавлен. %s' % line
                    self.good = self.good + 1
                else:
                    self.report[product_category][line_number] = 'Ошибка! не найдено соответсвие в TECDOC. %s' % line
                    self.bad = self.bad + 1

                if not prices[0]:
                    self.report[product_category][
                        line_number] = 'Ошибка! Товар добавлен без указании цены товара в рознице. %s' % line
                    self.bad = self.bad + 1

            except Exception as e:
                self.report[product_category][line_number] = "Проверьте корректность строки (Exception: %s) [%s]" % (
                    e, line)
                self.bad = self.bad + 1
        connection.close()

    def get_report(self):
        """ method for generating report """
        sorted_reports = sort_reports(self.report)

        report = ('Прококол загрузки файла товаров %s от %s.%s.%s %s:%s\r\n' % (
            self.filename,
            self.date['day'],
            self.date['month'],
            self.date['year'],
            self.date['hour'],
            self.date['minute'],
        ))

        total_products = 0
        for key, category_report in sorted_reports.items():
            total_products += len(category_report)

        bad = self.bad
        good = self.good
        report += 'Всего обработано - %s, из них принято - %s, с ошибкой - %s\r\n' % (total_products, good, bad)

        for category_key, category_report in sorted_reports.items():
            for key, item in category_report.items():
                report += '%s. %s\n' % (key, item)
        return report

    def save_report(self):
        """ method for saving report to server, to DB and sending to admins email"""
        filename, file_extension = os.path.splitext(self.filename)
        print('filename: %s, new_filename: %s, file_ext: %s' % (self.filename, filename, file_extension))
        report_filename = '%s_%s_%s_%s_%s%s.txt' % (
            filename,
            self.date['year'],
            self.date['month'],
            self.date['day'],
            self.date['hour'],
            self.date['minute']
        )
        print(report_filename)
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
        subject = 'Протокол загрузки файла %s из 1С от %s.%s.%s %s:%s' % (
            self.filename,
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

    def truncate_products(self, storage_id):
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM shop_productstorageprice where storage_id=%s" % storage_id)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    def get_prices(self, row):
        prices = {}
        for x in range(7):
            try:
                column = x + 3
                prices[x] = row[column]
                if ',' in row[column]:
                    prices[x] = row[column].replace(',', '.')
                else:
                    prices[x] = float(row[column])
            except:
                prices[x] = 0
        return prices

    def parse_products(self, all_products):
        product_categories = ProductCategory.get_all_categories()
        brands = make_brands(product_categories)
        products = make_products_template_with_category(product_categories)

        for product in all_products:
            row = product.split(';')
            try:
                brand = row[1].lower()
            except (AttributeError, IndexError):
                brand = 'UNKNOWN'
            if brand in brands:
                products[brands.get(brand)].append(product)
            else:
                products[ProductCategory.Tecdoc].append(product)
        return products


def make_brands(product_categories):
    brands = {}
    for product_category in product_categories:
        for brand in product_category.brands_as_list():
            brands.update({brand.lower(): product_category.name.lower()})
    return brands


def make_products_template_with_category(product_categories):
    products = {}
    for product_category in product_categories:
        products.update({product_category.name.lower(): []})
    return products
