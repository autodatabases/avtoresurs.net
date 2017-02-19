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


class AccountView(TemplateView):
    template_name = 'account/account_view.html'

    # model = Account

    # def get_object(self, queryset=None):
    #     """ Hook to ensure object is owned by request.user"""
    #     obj = super(AccountView, self).get_object()
    #     account = Account.objects.all().filter(user=self.request.user).first()
    #     # if not obj in massmedia.reporter_set.all():
    #     #     raise Http404
    #     return obj

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data()
        account = Account.objects.all().filter(user=self.request.user).first()
        context['account'] = account
        return context
        # account = User.objects.g


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

        # cur.execute("SELECT VERSION()")
        # ver = cur.fetchone()
        # print("Database version : %s " % ver)

        sql = "select * from x17f_catalog_users"
        cur.execute(sql)
        rows = cur.fetchall()

        for row in rows:
            user_import(row)

        return context


class PointLoader(TemplateView):
    template_name = 'account/point_file_upload.html'

    # form_class = UploadFileForm

    # def get(self, request):
    #     return HttpResponseRedirect('/account/point_load/')

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except:
            return HttpResponseRedirect('/account/point_load/')

        # filename, file_extension = os.path.splitext(self.request.FILES['file'].name)
        date = datetime.datetime.now()
        now = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
        filename = str(date.date()) + '_' + self.request.FILES['file'].name
        filename = 'points/' + str(date.year) + '/' + str(date.month) + '/' + filename
        # print(filename)
        path = default_storage.save(filename, ContentFile(file.read()))

        with open('media/' + path, 'r', encoding='cp1251') as fin:
            data = fin.read().splitlines(True)
        with open('media/' + path, 'w') as fout:
            fout.writelines(data[1:])

        for line in data[1:]:
            row = line.split(';')
            login = row[0].replace('ЦБ', 'cl')
            account = Account.objects.get(user__username=login)
            account.fullname = row[1]
            account.vip_code = row[2].strip()
            point = account.get_point()
            point.point = float(row[3].replace(',', '.'))
            account.save()
            point.save()

        return HttpResponse('ok')
