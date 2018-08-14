# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'home_application.ucloud.views',
    url(r'^$', 'ucloud'),
    url(r'api/syncUcloudAccount', 'syncUcloudAccount'),
    url(r'api/getUcloudInstanceList', 'getUcloudInstanceList'),
)