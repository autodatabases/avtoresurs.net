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

from avtoresurs_new import settings
from cart.views import CartView, ItemCountView, CheckoutView
from main.forms import RegistrationFormTOSAndEmail

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^', include('main.urls', namespace='main')),
                  url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormTOSAndEmail),
                      name='registration_register'),
                  url(r'^accounts/', include('registration.backends.hmac.urls')),

                  url(r'^accounts/profile/$', RedirectView.as_view(url='/account/', permanent=False),
                      name='ProfilePage'),
                  url(r'^account/', include('account.urls', namespace='account')),
                  # url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/successfully_logged_out/'}),
                  # url(r'account/', include('account.urls', namespace='account')),
                  url(r'shop/', include('shop.urls', namespace='shop')),
                  url(r'parts/', include('tecdoc.urls', namespace='tecdoc')),
                  url(r'^cart/$', CartView.as_view(), name='cart'),
                  url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
                  url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
