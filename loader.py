from ftplib import FTP

import datetime

from account.models import Account

host = '195.190.127.74'
user = 'Oleg'
passwd = 'KoxlabiruX'
filename = 'Klients.csv'
date = datetime.datetime.now()
filename_with_date = str(date.date()) + '_' + filename


class FtpFile:
    def __init__(self, host, user, passwd):
        self.ftp = FTP(host=host)
        self.ftp.set_pasv(False)
        self.ftp.login(user=user, passwd=passwd)
        # self.ftp.dir()

    def get_file(self, filename):

        # path = 'media/points/' + str(date.year()) + '/'
        file = open(filename_with_date, 'wb')
        self.ftp.retrbinary('RETR %s' % filename, file.write)

FtpFile(host=host, user=user, passwd=passwd).get_file(filename)

with open(filename_with_date, 'r', encoding='cp1251') as fin:
    data = fin.read().splitlines(True)

for line in data[1:]:
    row = line.split(';')
    login = row[0].replace('ЦБ', 'cl')
    account = Account.objects.get(user__username=login)
    account.fullname = row[1]
    account.vip_code = row[2].strip()

# with open('media/' + path, 'w') as fout:
#     fout.writelines(data[1:])


# ftp = FTP(host=host)
# ftp.set_pasv(False)
# ftp.login(user=user, passwd=passwd)
# ftp.dir()
#
# date = datetime.datetime.now()
# path = 'media/points/' + str(date.year())
#
# file = open(str(date.date()) + '_' + filename, 'wb')
# ftp.retrbinary('RETR %s' % filename, file.write)

# print(file)
