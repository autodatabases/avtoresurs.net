from django.conf import settings
from django.conf.urls import include, url
from main.views import resend_activation_email

# from .views import (
#     news_list
# )

from .views import (
    MainPageView,
)

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main_page'),
    # url(r'^load/$', ProductLoader.as_view(), name='loader'),
    url(r'^accounts/reactivate/$', resend_activation_email, name='account_reactivate'),
]
