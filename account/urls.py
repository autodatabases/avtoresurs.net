from django.conf.urls import url

from account.views import AccountView, AccountImport, PointLoader

urlpatterns = [
    url(r'^$', AccountView.as_view(), name='account_main'),
    url(r'^load/$', AccountImport.as_view(), name='account_importer'),
    url(r'^point_load/$', PointLoader.as_view(), name='point_importer'),
]