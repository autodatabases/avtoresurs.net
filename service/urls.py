from django.conf import settings
from django.conf.urls import include, url
from main.views import resend_activation_email, AboutView

# from .views import (
#     news_list
# )

from .views import (
    ProductLoader,
)

urlpatterns = [
    url(r'^load/$', ProductLoader.as_view(), name='product_loader'),
]
