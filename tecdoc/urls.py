from django.conf.urls import url

from .views.manufacturer import ManufacturerList, ManufacturerView

urlpatterns = [
    url(r'^$', ManufacturerList.as_view(), name='manufacturers'),
    url(r'^(?P<mnf_id>\d+)/$', ManufacturerView.as_view(), name='manufacturer'),
]
