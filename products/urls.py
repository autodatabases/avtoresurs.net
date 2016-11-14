from django.conf import settings
from django.conf.urls import include, url

# from .views import (
#     news_list
# )

from .views import (
    ProductDetailView,
    ProductListView,
    # product_detail_view_func
)

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='products'),
    url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
    # url(r'^(?P<id>\d+)', product_detail_view_func, name='shop_detail'),
]