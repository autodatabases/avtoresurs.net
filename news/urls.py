from django.conf import settings
from django.conf.urls import include, url
from main.views import resend_activation_email

# from .views import (
#     news_list
# )

from .views import (
    NewsList,
)

urlpatterns = [
    url(r'^.*$', NewsList.as_view(), name='news_list'),
]
