from django.conf.urls import url
from main.views import resend_activation_email

urlpatterns = [
    url(r'^accounts/reactivate/$', resend_activation_email, name='account_reactivate'),
]
