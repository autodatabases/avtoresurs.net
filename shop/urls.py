from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from shop.views.product import ProductDetailView
from shop.views.search import SearchView, SearchDetailView
from shop.views.shop import ShopIndexView
from shop.views.api import PPList, PPDetail

urlpatterns = [
    url(r'^$', ShopIndexView.as_view(), name='shop_index'),
    url(r'^product/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^search/$', SearchView.as_view(), name='search_page'),
    url(r'^search/analogs/$', SearchDetailView.as_view(), name='search_detail'),
    url(r'^api/$', PPList.as_view(), name='psp_list'),
    url(r'^api/(?P<pk>[0-9]+)/$', PPDetail.as_view(), name='psp_list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
