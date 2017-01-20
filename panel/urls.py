from django.conf.urls import url

from panel.views import PanelMainView

urlpatterns = [
    url(r'^$', PanelMainView.as_view(), name='account_main'),
    # url(r'^load/$', AccountImport.as_view(), name='account_importer'),
]