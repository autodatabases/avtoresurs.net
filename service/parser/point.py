import datetime
import os

from django.core.mail import EmailMessage

from avtoresurs_new.settings import DIR, EMAIL_NOREPLY, EMAIL_TO, EMAIL_BCC, EMAIL_NOREPLY_LIST
from user_profile.models import UserProfile
from filer.models.foldermodels import Folder
from filer.models import File, ContentFile
from django.core.files.storage import default_storage


class PointLoader:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.date = datetime.datetime.now()
        self.year = self.date.strftime('%Y')
        self.month = self.date.strftime('%m')
        self.day = self.date.strftime('%d')
        self.hour = self.date.strftime('%H')
        self.minute = self.date.strftime('%M')
        self.report = {'good': list(), 'bad': list()}
        self.report_str = None

    def parse_file(self):
        with open(self.filename, 'r', encoding='cp1251') as fin:
            self.data = fin.read().splitlines(True)
        fin.close()

    def load(self):
        for line in self.data[1:]:
            try:
                row = line.split(';')
                login = row[0].replace('ЦБ', 'cl')
                profile = UserProfile.objects.get(user__username=login)
                profile.fullname = row[1]
                profile.vip_code = row[2].strip()
                profile.points = float(row[3].replace(',', '.'))
                profile.save()
                self.report['good'].append('%s - %s\n' % ('OK', line.strip()))
            except Exception as e:
                self.report['bad'].append('%s - %s, %s\n' % ('ERROR', line.strip(), e))

    def save_report(self):
        report_filename = 'protokol_%s_%s_%s_%s_%s.txt' % (self.year, self.month, self.day, self.hour, self.minute)
        report_path = os.path.join(DIR['CSV'], DIR['KLIENTS'], DIR['LOG'], self.year, self.month, report_filename)

        good = len(self.report['good'])
        bad = len(self.report['bad'])
        self.report_str = 'Всего записей - %s, загружено - %s, не загружено - %s\n\n' % (good + bad, good, bad)
        for line in self.report['good']:
            self.report_str += line
        for line in self.report['bad']:
            self.report_str += line
        report_bytes = self.report_str.encode('utf-8')
        report_path = default_storage.save(report_path, ContentFile(report_bytes))

        folder, created = Folder.objects.get_or_create(name='Klients')
        subfolder_year, created = Folder.objects.get_or_create(name=self.date.strftime('%Y'), parent=folder)
        subfolder_month, created = Folder.objects.get_or_create(name=self.date.strftime('%m'), parent=subfolder_year)

        report_file = File(file=report_path)
        report_file.name = report_filename
        report_file.folder = subfolder_month

        report_file.save()

    def send_email(self):
        subject = 'Протокол загрузки файла Klients.csv от %s.%s.%s %s:%s' % (
            self.year, self.month, self.day, self.hour, self.minute)
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

        email.attach('Klients.txt', self.report_str, 'text/plain')
        email.send()
