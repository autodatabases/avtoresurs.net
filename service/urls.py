from django.conf import settings
from django.conf.urls import include, url
from main.views import resend_activation_email, AboutView
from service.views.bonus import BonusView
from service.views.custom_cross import CustomCrossView
from service.views.point import PointView
from service.views.product import ProductView
from service.views.service import ServiceView

urlpatterns = [
    url(r'^$', ServiceView.as_view(), name='main'),
    url(r'^product_load/$', ProductView.as_view(), name='product_load'),
    url(r'^point_load/$', PointView.as_view(), name='point_load'),
    url(r'^bonus_load/$', BonusView.as_view(), name='bonus_load'),
    url(r'^custom_cross/$', CustomCrossView.as_view(), name='custom_cross'),

]
