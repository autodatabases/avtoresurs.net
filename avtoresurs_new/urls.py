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
from shop.views.checkout import CheckoutView, CheckoutSuccessView
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [

                  url(r'^admin/filebrowser/', include(site.urls)),
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormTOSAndEmail),
                      name='registration_register'),
                  url(r'^accounts/', include('registration.backends.hmac.urls')),
                  url(r'^accounts/profile/$', RedirectView.as_view(url='/profile/', permanent=False),
                      name='ProfilePage'),
                  url(r'^profile/', include('profile.urls', namespace='profile')),
                  url(r'^cart/$', CartView.as_view(), name='cart'),
                  url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
                  url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
                  url(r'^checkout/success/$', CheckoutSuccessView.as_view(), name='checkout_success'),
                  url(r'^service/', include('service.urls', namespace='service')),
                  url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
                  # url(r'^api/', include(router.urls)),
                  # url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  # url(r'^', include('main.urls', namespace='main')),
                  # ALL URLS AFTER 'cms.ursl' WILL NOT WORK!!!
                  url(r'^', include('cms.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
