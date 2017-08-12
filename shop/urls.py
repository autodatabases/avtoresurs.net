from django.conf.urls import url

from shop.views.product import ProductDetailView
from shop.views.search import SearchView, SearchDetailView
from shop.views.shop import ShopIndexView



urlpatterns = [
    url(r'^$', ShopIndexView.as_view(), name='shop_index'),
    url(r'^product/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^search/$', SearchView.as_view(), name='search_page'),
    url(r'^search/analogs/$', SearchDetailView.as_view(), name='search_detail'),
]