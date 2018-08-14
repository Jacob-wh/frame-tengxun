# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'home_application.qcloud.views',
    url(r'^$', 'qcloud'),
    #查询腾讯云账号列表
    url(r'api/getQcloudAccountList$', 'getQcloudAccountList'),
    #同步腾讯云虚拟机信息
    url(r'api/syncDescribeInstances$', 'syncDescribeInstances'),
    #同步腾讯云虚拟机信息
    url(r'api/syncImages$', 'syncImages'),
    #查询腾讯云实例列表
    url(r'api/getQcloudVmList$', 'getQcloudVmList'),
    #开启腾讯云实例
    url(r'api/startQcloudVm$', 'startQcloudVm'),
    #关闭腾讯云实例
    url(r'api/stopQcloudVm$', 'stopQcloudVm'),
)