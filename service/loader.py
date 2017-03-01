from ftplib import FTP

import datetime

import sys, os, django

os.environ["DJANGO_SETTINGS_MODULE"] = "avtoresurs_new.settings"
django.setup()

from profile.models import Account

HOST = '195.190.127.74'
USER = 'Oleg'
PASSWD = 'KoxlabiruX'

# HOST = '46.101.123.237'
# USER = 'ftpuser'
# PASSWD = 'Ufdhbrb31337'

filenames = ('Klients.csv', 'Priz.csv',)
date = datetime.datetime.now()
path = os.path.join('media', 'csv', 'klients', str(date.date().year))


class FtpFile:
    def __init__(self, host, user, passwd):
        self.ftp = FTP(host=host)
        self.ftp.set_pasv(False)
        self.ftp.login(user=user, passwd=passwd)


    def get_file(self, filename):
        new_filename = os.path.join(path, str(date.date()) + '_' + filename)
        file = open(new_filename, 'wb')
        self.ftp.retrbinary('RETR %s' % filename, file.write)


ftp = FtpFile(host=HOST, user=USER, passwd=PASSWD)
for filename in filenames:
    ftp.get_file(filename)
ftp.ftp.close()




# path = 'media/points/' + str(date.date().year) + '/'
# with open(path + str(date.date()) + '_' + 'Klients.cs', 'r', encoding='cp1251') as fin:
#     data = fin.read().splitlines(True)

# for line in data[1:]:
#     print(line)
# row = line.split(';')
# login = row[0].replace('ЦБ', 'cl')
# account = Account.objects.get(user__username=login)
# account.fullname = row[1]
# account.vip_code = row[2].strip()
