import MySQLdb
import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.contrib.auth.models import User

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

# Create your views here.
from django.views.generic.edit import FormMixin

from account.forms import UploadFileForm
from account.models import Account, Point
from avtoresurs_new.settings import BASE_DIR

import urllib.parse

from service.parser.klients import parse_klients


class AccountView(TemplateView):
    template_name = 'account/account_view.html'

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data()
        account = Account.objects.all().filter(user=self.request.user).first()
        context['account'] = account
        return context


def user_import(row):
    username = row[3]
    password = row[4]
    fullname = row[5]
    vip_code = row[2]
    points = row[6]

    user = User(username=username)
    user.set_password(password)
    user.save()

    account = Account(user=user, fullname=fullname, vip_code=vip_code)
    account.save()

    point = Point(account=account, point=points)
    point.save()
    print("Пользователь %s %s добавлен" % (username, password))


class AccountImport(TemplateView):
    template_name = 'account/account_view.html'

    def get_context_data(self, **kwargs):
        context = super(AccountImport, self).get_context_data()
        host = '85.25.45.121'
        login = ''
        password = ''
        database = 'main'

        con = MySQLdb.connect(host=host, user=login, passwd=password, db=database, charset='utf8')
        cur = con.cursor()

        sql = "select * from x17f_catalog_users"
        cur.execute(sql)
        rows = cur.fetchall()

        for row in rows:
            user_import(row)

        return context


class PointLoader(TemplateView):
    template_name = 'account/point_file_upload.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/account/point_load/')

        date = datetime.datetime.now()
        filename = os.path.join('csv', 'klients', date.strftime('%Y'), date.strftime('%m'),
                                self.request.FILES['file'].name)

        path = default_storage.save(filename, ContentFile(file.read()))
        file.close()

        with open('media/' + path, 'r', encoding='cp1251') as fin:
            data = fin.read().splitlines(True)

        protocol = parse_klients(data)
        print('Загружено - %s, не загружено - %s' % (protocol[1], protocol[2]))
        for p in protocol[0]:
            print(p)
        return HttpResponse('OK')
