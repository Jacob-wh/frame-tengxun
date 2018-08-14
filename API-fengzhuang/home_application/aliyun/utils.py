# -*- coding: utf-8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
import traceback
import time
import pytz
import datetime


def getInstances(module,action,secretId,secretKey,region,Version,PageNumber,PageSize):
    module = module
    '''
    action 对应接口的接口名，请参考产品文档上对应接口的接口名
    '''
    action = action
    # 创建 AcsClient 实例
    client = AcsClient(
        secretId,
        secretKey,
        region
    );
    try:
        request = CommonRequest()
        request.set_domain(module)
        request.set_version(Version)
        request.set_action_name(action)
        request.add_query_param('PageNumber', PageNumber)
        request.add_query_param('PageSize', PageSize)
        response = client.do_action_with_exception(request)
        return response
    except Exception, e:
        traceback.print_exc()
        print 'exception:', e



def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%M:%SZ'):
    local_tz = pytz.timezone('Asia/Shanghai')
    local_format = "%Y-%m-%d %M:%S"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return datetime.datetime.strptime(time_str, local_format)