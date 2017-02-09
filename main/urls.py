from django.conf import settings
from django.conf.urls import include, url
from main.views import resend_activation_email, AboutView

# from .views import (
#     news_list
# )

from .views import (
    MainPageView,
)

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main_page'),
    url(r'^about/$', AboutView.as_view(), name='about_view'),
    # url(r'^load/$', ProductLoader.as_view(), name='loader'),
    url(r'^accounts/reactivate/$', resend_activation_email, name='account_reactivate'),
]
