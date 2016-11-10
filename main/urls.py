from django.conf import settings
from django.conf.urls import include, url

# from .views import (
#     news_list
# )

from .views import (
    MainPageView
)

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main_page'),

]