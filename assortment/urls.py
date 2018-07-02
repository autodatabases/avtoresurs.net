from django.conf.urls import url

# from .views import (
#     news_list
# )

from .views import (
    AssortmentList,
)

urlpatterns = [
    url(r'^$', AssortmentList.as_view(), name='assortment_page'),
]
