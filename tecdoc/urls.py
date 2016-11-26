from django.conf.urls import url

from tecdoc.views.carmodel import CarModelView
from tecdoc.views.parts import PartList
from tecdoc.views.section import SectionList, SectionDetail
from tecdoc.views.manufacturer import ManufacturerList, ManufacturerView

urlpatterns = [
    url(r'^$', ManufacturerList.as_view(), name='manufacturers'),
    url(r'^(?P<mnf_id>\d+)/$', ManufacturerView.as_view(), name='manufacturer'),
    url(r'^(?P<mnf_id>\d+)/(?P<model_id>\d+)/$', CarModelView.as_view(), name='model'),
    url(r'^(?P<mnf_id>\d+)/(?P<model_id>\d+)/(?P<type_id>\d+)/$', SectionList.as_view(), name='section_list'),
    url(r'^(?P<mnf_id>\d+)/(?P<model_id>\d+)/(?P<type_id>\d+)/(?P<section_id>\d+)/$', SectionDetail.as_view(), name='section_detail'),
    #     name='parts-catalog'),
]
