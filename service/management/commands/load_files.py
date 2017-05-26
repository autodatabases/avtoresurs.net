import datetime
import os
import threading
from ftplib import FTP

from django.core.management.base import BaseCommand, CommandError

from avtoresurs_new.settings import MEDIA_ROOT
from service.views import point_load, get_clients_filename

# HOST = '195.190.127.74'
# USER = 'oleg'
# PASSWD = 'KoxlabiruX'

HOST = '46.101.123.237'
USER = 'ftpuser'
PASSWD = 'Ufdhbrb31337'

filenames = ('Klients.csv',)


class FtpFile:
    def __init__(self, host, user, passwd):
        self.ftp = FTP(host=host)
        self.ftp.set_pasv(True)
        self.ftp.login(user=user, passwd=passwd)

    def get_file(self, filename):
        new_filename = get_clients_filename(filename)
        file = open(new_filename, 'wb')
        self.ftp.retrbinary('RETR %s' % filename, file.write)
        file.close()
        point_load(new_filename)


class Command(BaseCommand):
    help = 'Download files from FTP'

    def handle(self, *args, **options):
        ftp = FtpFile(host=HOST, user=USER, passwd=PASSWD)
        for filename in filenames:
            ftp.get_file(filename)
        ftp.ftp.close()

        self.stdout.write(self.style.SUCCESS('Successfully'))
