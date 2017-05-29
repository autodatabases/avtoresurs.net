import datetime
from io import BytesIO
import os
import threading
from ftplib import FTP

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError

from avtoresurs_new.settings import MEDIA_ROOT
from service.views import point_load, get_filename, price_load

# REAL FTP
HOST = '195.190.127.74'
USER = 'oleg'
PASSWD = 'KoxlabiruX'

# TEST FTP
# HOST = '46.101.123.237'
# USER = 'ftpuser'
# PASSWD = 'Ufdhbrb31337'

# filenames = ('Klients.csv', )
filenames = ('Klients.csv', 'NewsAuto.csv')


class FtpFile:
    def __init__(self, host, user, passwd):
        self.ftp = FTP(host=host)
        self.ftp.set_pasv(True)
        self.ftp.login(user=user, passwd=passwd)

    def get_file(self, filename):
        new_file = get_filename(filename)
        file = BytesIO()
        self.ftp.retrbinary('RETR %s' % filename, file.write)
        file.seek(0)
        default_storage.save(new_file, ContentFile(file.read()))
        if filename == 'Klients.csv':
            point_load(new_file)
        elif filename == 'NewsAuto.csv':
            price_load(new_file)


class Command(BaseCommand):
    help = 'Download files from FTP'

    def handle(self, *args, **options):
        ftp = FtpFile(host=HOST, user=USER, passwd=PASSWD)
        for filename in filenames:
            ftp.get_file(filename)
        ftp.ftp.close()

        self.stdout.write(self.style.SUCCESS('Successfully'))
