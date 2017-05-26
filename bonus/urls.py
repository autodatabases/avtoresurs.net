#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from bonus.views import BonusObtainView
from . import views

urlpatterns = [
    url(r'^$', views.BonusPageView.as_view(), name='BonusPage'),
    url(r'^obtain/$', csrf_exempt(BonusObtainView.as_view()), name='BonusObtain'),
]
