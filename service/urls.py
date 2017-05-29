from django.conf import settings
from django.conf.urls import include, url
from main.views import resend_activation_email, AboutView

from .views import (
    ProductLoad,
    PointLoad,
    ServiceMainViev,
    BonusLoad)

urlpatterns = [
    url(r'^$', ServiceMainViev.as_view(), name='main'),
    url(r'^product_load/$', ProductLoad.as_view(), name='product_load'),
    url(r'^point_load/$', PointLoad.as_view(), name='point_load'),
    url(r'^bonus_load/$', BonusLoad.as_view(), name='bonus_load'),
]
