# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'home_application.overview.views',
    url(r'^$', 'overview'),
    url(r'^getAnalysisDataRequest$', 'getAnalysisDataRequest'),
)