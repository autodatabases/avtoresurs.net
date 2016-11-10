from django.conf.urls import url

from .views import (
    ShopIndexView,
)


urlpatterns = [
    url(r'^$', ShopIndexView.as_view(), name='shop_index'),
]