#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Author  : LiQingLei
# @File    : utils.py
# @Time    : 2017/8/11 15:52
# @Last Modified by:   LiQingLei
# @Last Modified time: 2017/8/11 15:52
# @Site    : 
# @desc    :
'''


# 引入云API入口模块
from QcloudApi.qcloudapi import QcloudApi
import traceback
import time
import pytz
import datetime
from requests import request


'''
module 设置需要加载的模块
已有的模块列表：
cvm      对应   cvm.api.qcloud.com
cdb      对应   cdb.api.qcloud.com
lb       对应   lb.api.qcloud.com
trade    对应   trade.api.qcloud.com
sec      对应   csec.api.qcloud.com
image    对应   image.api.qcloud.com
monitor  对应   monitor.api.qcloud.com
cdn      对应   cdn.api.qcloud.com
wenzhi   对应   wenzhi.api.qcloud.com
'''

def getInstances(module,action,secretId,secretKey,Version,Offset,Limit):
    print 'module : %s ' %module
    print 'action : %s ' %action
    print 'secretId : %s ' %secretId
    print 'secretKey : %s ' %secretKey
    print 'Version : %s ' %Version
    print 'Offset : %s ' %Offset
    print 'Limit : %s ' %Limit
    module = module
    '''
    action 对应接口的接口名，请参考产品文档上对应接口的接口名
    '''
    action = action
    config = {
        'Region': 'ap-beijing',
        'secretId': secretId,
        'secretKey': secretKey,
        'method': 'get'
    }
    '''
    params 请求参数，请参考产品文档上对应接口的说明
    '''
    params = {
        'Version': "2017-03-12",
    }
    if Offset is not None:
        params['Offset'] = Offset
    if Limit is not None:
        params['Limit'] = Limit
    try:
        print 'config : %s ' % config
        service = QcloudApi(module, config)
        # 生成请求的URL，不发起请求
        print 'service : %s ' % service
        print 'params : %s ' % params
        service.generateUrl(action, params)
        # print service.generateUrl(action, params)
        # 调用接口，发起请求
        print params
        result = service.call(action, params)
        print service.call(action, params)
        return result
    except Exception, e:
        traceback.print_exc()
        print 'exception:', e




def requestQcloud(module,action,secretId,secretKey,params):
    module = module
    '''
    action 对应接口的接口名，请参考产品文档上对应接口的接口名
    '''
    action = action
    config = {
        'Region': 'ap-beijing',
        'secretId': secretId,
        'secretKey': secretKey,
        'method': 'get'
    }
    '''
    params 请求参数，请参考产品文档上对应接口的说明
    '''
    params = {
        'Version': "2017-03-12",
    }
    # if Offset is not None:
    #     params['Offset'] = Offset
    # if Limit is not None:
    #     params['Limit'] = Limit
    try:
        service = QcloudApi(module, config)
        # 生成请求的URL，不发起请求
        service.generateUrl(action, params)
        print service.generateUrl(action, params)
        # 调用接口，发起请求
        print params
        result = service.call(action, params)
        print service.call(action, params)
        return result
    except Exception, e:
        traceback.print_exc()
        print 'exception:', e


def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    local_tz = pytz.timezone('Asia/Shanghai')
    local_format = "%Y-%m-%d %H:%M:%S"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return datetime.datetime.strptime(time_str, local_format)
