"""avtoresurs_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView
from registration.backends.hmac.views import RegistrationView
from filebrowser.sites import site
from avtoresurs_new import settings

from main.forms import RegistrationFormTOSAndEmail
from shop.views.cart import CartView, ItemCountView
from shop.views.checkout import CheckoutView

urlpatterns = [
                  url(r'^admin/filebrowser/', include(site.urls)),
                  # url(r'^grappelli/', include('grappelli.urls')),
                  url(r'^admin/', include(admin.site.urls)),

                  url(r'^', include('cms.urls')),
                  url(r'^', include('main.urls', namespace='main')),
                  url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormTOSAndEmail),
                      name='registration_register'),
                  url(r'^accounts/', include('registration.backends.hmac.urls')),

                  url(r'^accounts/profile/$', RedirectView.as_view(url='/profile/', permanent=False),
                      name='ProfilePage'),
                  url(r'^profile/', include('profile.urls', namespace='profile')),
                  url(r'^news/', include('news.urls', namespace='news')),
                  url(r'shop/', include('shop.urls', namespace='shop')),
                  url(r'parts/', include('tecdoc.urls', namespace='tecdoc')),
                  url(r'^cart/$', CartView.as_view(), name='cart'),
                  url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
                  url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
                  url(r'^service/', include('service.urls', namespace='service')),
                  url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
