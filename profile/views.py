import MySQLdb
import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.models import User

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

# Create your views here.
from django.views.generic.edit import FormMixin, UpdateView, FormView
from django.views.generic.list import MultipleObjectMixin

from profile.forms import UploadFileForm, ProfileForm
from profile.models import Profile, Point
from avtoresurs_new.settings import BASE_DIR

import urllib.parse

from service.parser.klients import parse_klients
from shop.models.order import Order


class ProfileView(TemplateView):
    template_name = 'profile/profile_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        profile = Profile.objects.all().filter(user=self.request.user).first()
        context['profile'] = profile
        return context


class ProfileEdit(FormView):
    form_class = ProfileForm
    model = User
    template_name = 'profile/profile_edit.html'
    success_url = '/profile/'


def user_import(row):
    username = row[3]
    password = row[4]
    fullname = row[5]
    vip_code = row[2]
    points = row[6]

    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()

    profile = Profile(user=user, fullname=fullname, vip_code=vip_code)
    profile.save()

    point = Point(profile=profile, point=points)
    point.save()
    print("Пользователь %s %s добавлен" % (username, password))


class ProfileImport(TemplateView):
    template_name = 'profile/profile_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileImport, self).get_context_data()
        host = '85.25.45.121'
        login = 'root'
        password = '11235813zZ!'
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
    template_name = 'profile/point_file_upload.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/profile/point_load/')

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


class OrderList(ListView):
    template_name = 'profile/order_list.html'
    paginate_by = 20
    model = Order

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(user=user).order_by('-added')
        return orders

        # def get_context_data(self, **kwargs):
        #     context = super(OrderList, self).get_context_data()
        #     user = self.request.user
        # orders = Order.objects.filter(user=user)
        # context['orders'] = orders
        # return context


class OrderDetail(DetailView):
    template_name = 'profile/order_detail.html'
    model = Order

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user"""
        obj = super(OrderDetail, self).get_object()
        user = self.request.user
        if not obj.user == user:
            raise Http404
        return obj
