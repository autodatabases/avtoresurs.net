from django.conf import settings
from django.conf.urls import include, url
from main.views import resend_activation_email, AboutView

# from .views import (
#     news_list
# )

from .views import (
    MainPageView, BrandsView, AssortmentView, TrucksView, FAQView, ServiceStationView, ContactsView
)

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main_page'),
    url(r'^about/$', AboutView.as_view(), name='about_view'),
    url(r'^brands/$', BrandsView.as_view(), name='brands_view'),
    url(r'^assortment/$', AssortmentView.as_view(), name='assortment_view'),
    url(r'^trucks/$', TrucksView.as_view(), name='trucks_view'),
    url(r'^faq/$', FAQView.as_view(), name='faq_view'),
    url(r'^service_stations/$', ServiceStationView.as_view(), name='service_stations_view'),
    url(r'^contacts/$', ContactsView.as_view(), name='contacts_view'),
    # url(r'^load/$', ProductLoader.as_view(), name='loader'),
    url(r'^accounts/reactivate/$', resend_activation_email, name='account_reactivate'),
]
