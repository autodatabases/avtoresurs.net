from django.conf.urls import url

from profile.views import ProfileView, ProfileEdit, ProfileImport, PointLoader

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile_main'),
    url(r'^edit/(?P<pk>[0-9]+)/$', ProfileEdit.as_view(), name='profile_edit'),
    url(r'^load/$', ProfileImport.as_view(), name='profile_importer'),
    url(r'^point_load/$', PointLoader.as_view(), name='point_importer'),
]