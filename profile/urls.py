from django.conf.urls import url

from profile.views import ProfileView, ProfileImport, PointLoader

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile_main'),
    url(r'^load/$', ProfileImport.as_view(), name='profile_importer'),
    url(r'^point_load/$', PointLoader.as_view(), name='point_importer'),
]