# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'home_application.azure.views',
    url(r'^$', 'azure'),
    url(r'api/getAzureVmList$','getAzureVmList')
)