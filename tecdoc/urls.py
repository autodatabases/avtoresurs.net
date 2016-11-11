from django.conf.urls import url

from tecdoc.views.carmodel import CarModelView
from tecdoc.views.searchtree import SearchTreeList
from .views.manufacturer import ManufacturerList, ManufacturerView

urlpatterns = [
    url(r'^$', ManufacturerList.as_view(), name='manufacturers'),
    url(r'^(?P<mnf_id>\d+)/$', ManufacturerView.as_view(), name='manufacturer'),
    url(r'^(?P<mnf_id>\d+)/(?P<model_id>\d+)/$', CarModelView.as_view(), name='models'),
    url(r'^(?P<mnf_id>\d+)/(?P<model_id>\d+)/(?P<type_id>\d+)/$', SearchTreeList.as_view(), name='tree'),
]
