from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
# Create your views here.
from django.views.generic.edit import FormView

from profile.forms import ProfileForm
from profile.models import Profile
from shop.models.order import Order


class ProfileView(TemplateView):
    template_name = 'profile/profile_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        profile = Profile.objects.all().filter(user=self.request.user).first()
        context['profile'] = profile
        orders_count = Order.objects.filter(user=self.request.user).count()
        context['orders_count'] = orders_count
        return context


class ProfileEdit(FormView):
    form_class = ProfileForm
    model = Profile
    template_name = 'profile/profile_edit.html'

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(ProfileEdit, self).get_context_data()
        profile = get_object_or_404(Profile, user=self.request.user)
        fullname = profile.fullname
        form = ProfileForm({'fullname': fullname})
        if self.request.POST:
            # print("post")
            form = self.get_form()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            profile = Profile.objects.get(user=self.request.user)
            profile.fullname = form.cleaned_data['fullname']
            user = self.request.user
            user.set_password(form.cleaned_data['password1'])
            print(form.cleaned_data['password1'])
            profile.save()
            user.save()

        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect('/profile/')


class OrderList(ListView):
    template_name = 'profile/order_list.html'
    paginate_by = 20
    model = Order

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(user=user).order_by('-added')
        return orders


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

# def user_import(row):
#     username = row[3]
#     password = row[4]
#     fullname = row[5]
#     vip_code = row[2]
#     points = row[6]
#
#     user, created = User.objects.get_or_create(username=username)
#     if created:
#         user.set_password(password)
#         user.save()
#
#     profile = Profile(user=user, fullname=fullname, vip_code=vip_code)
#     profile.save()
#
#     point = Point(profile=profile, point=points)
#     point.save()
#     print("Пользователь %s %s добавлен" % (username, password))


# class ProfileImport(TemplateView):
#     template_name = 'profile/profile_view.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProfileImport, self).get_context_data()
#         host = '85.25.45.121'
#         login = 'root'
#         password = '11235813zZ!'
#         database = 'main'
#
#         con = MySQLdb.connect(host=host, user=login, passwd=password, db=database, charset='utf8')
#         cur = con.cursor()
#
#         sql = "select * from x17f_catalog_users"
#         cur.execute(sql)
#         rows = cur.fetchall()
#
#         for row in rows:
#             user_import(row)
#
#         return context
