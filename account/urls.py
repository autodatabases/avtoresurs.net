from django.conf.urls import url

from account.views import AccountView, AccountImport

urlpatterns = [
    url(r'^$', AccountView.as_view(), name='account_main'),
    url(r'^load/$', AccountImport.as_view(), name='account_importer'),
]