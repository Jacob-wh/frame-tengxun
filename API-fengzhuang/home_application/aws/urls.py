# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'home_application.aws.views',
    url(r'^$', 'aws'),
)