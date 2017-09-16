import datetime
import os
from django.core.files.storage import default_storage
from avtoresurs_new.settings import DIR, EMAIL_NOREPLY, EMAIL_TO, EMAIL_BCC, EMAIL_NOREPLY_LIST
from bonus.models import Bonus
from filer.models import File, ContentFile
from filer.models.foldermodels import Folder
from django.core.mail import EmailMessage


class BonusLoader:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.report = {'good': list(), 'bad': list()}

        self.date = datetime.datetime.now()
        self.year = self.date.strftime('%Y')
        self.month = self.date.strftime('%m')
        self.day = self.date.strftime('%d')
        self.hour = self.date.strftime('%H')
        self.minute = self.date.strftime('%M')
        self.good = 0
        self.bad = 0
        self.report_filename = None
        self.report_str = None

    def parse_file(self):
        with open(self.filename, 'r', encoding='cp1251') as file_price:
            self.data = file_price.read().splitlines(True)
        file_price.close()

    def load(self):
        for line in self.data[1:]:
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
                self.report['good'].append('%s %s\n' % (line.strip(), 'Принят'))
            except Exception as error:
                self.report['bad'].append('%s %s (%s)\n' % (line.strip(), 'Возникла ошибка', error))
        self.good = len(self.report['good'])
        self.bad = len(self.report['bad'])

    def save_report(self):
        self.report_str = 'Протокол приема файла Priz.csv от %s.%s.%s %s:%s\n' % (
            self.day, self.month, self.year, self.hour, self.minute)
        self.report_str += 'Всего обработано - %s, из них принято - %s, с ошибкой - %s\n\n' % (
            self.good + self.bad, self.good, self.bad)
        for line in self.report['good']:
            self.report_str += line
        for line in self.report['bad']:
            self.report_str += line

        self.report_filename = '%s_%s_%s_%s_%s_priz.txt' % (self.year, self.month, self.day, self.hour, self.minute)
        report_path = os.path.join(DIR['CSV'], DIR['BONUS'], DIR['LOG'], self.year, self.month, self.report_filename)
        report_path = default_storage.save(report_path, ContentFile(self.report_str.encode('utf-8')))

        folder, created = Folder.objects.get_or_create(name='Priz')
        subfolder_year, created = Folder.objects.get_or_create(name=self.date.strftime('%Y'), parent=folder)
        subfolder_month, created = Folder.objects.get_or_create(name=self.date.strftime('%m'), parent=subfolder_year)

        report_file = File(file=report_path)
        report_file.name = self.report_filename
        report_file.folder = subfolder_month

        report_file.save()

    def send_email(self):
        subject = 'Протокол загрузки файла Priz.csv от %s.%s.%s %s:%s' % (
            self.year, self.month, self.day, self.hour, self.minute)
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

        email.attach(self.report_filename, self.report_str, 'text/plain')
        email.send()
