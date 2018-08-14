# -*- coding: utf-8 -*-
import json
import traceback

import datetime
from django.http import HttpResponse, HttpResponseRedirect

from common.log import logger
from common.mymako import render_mako_context, render_json, render_json_custom
from home_application.models import VcenterAccount, UcloudInstance
from hybirdsdk.ucloud.sdk import UcloudApiClient
from hybirdsdk.ucloud.config import base_url


import json
from django.core.serializers.json import DjangoJSONEncoder

def ucloud(request):
    # 这里开始触发缓存数据，确保后续页面访问流畅。
    return render_mako_context(
        request, '/home_application/ucloud/ucloud.html'
    )


def syncUcloudAccount(request):
    accountId = None
    if request.method == 'POST':
        accountId = request.POST['id']
        logger.info( "accountId is %s" % accountId)
        if accountId is None or accountId < 0:
            res = {
                'result': True,
                'message': "该账号不存在",
            }
            return render_json(res)

        accountModel = VcenterAccount.objects.get(id=accountId)
        public_key = accountModel.cloud_public_key
        private_key = accountModel.cloud_private_key
        ApiClient = UcloudApiClient(base_url, public_key, private_key)
        Parameters={
            "Action":"DescribeUHostInstance",
            "Region":"cn-sh2",
        }
        response = ApiClient.get("/", Parameters)
        print response

"""
根据账号来同步
{
    u'Zone': u'cn-sh2-01',
    u'OsName': u'CentOS6.564\u4f4d',
    u'HostType': u'N1',
    u'State': u'Running',
    u'Memory': 4096,
    u'NetCapability': u'Normal',
    u'BootDiskState': u'Normal',
    u'CPU': 2,
    u'BasicImageName': u'CentOS6.564\u4f4d',
    u'IPSet': [
        {
            u'SubnetId': u'subnet-54zkvr',
            u'IP': u'10.23.35.12',
            u'VPCId': u'uvnet-fghges',
            u'Type': u'Private'
        },
        {
            u'IPId': u'eip-yb0b1g',
            u'IP': u'120.132.7.240',
            u'Bandwidth': 2,
            u'Type': u'Bgp',
            u'Weight': 50
        }
    ],
    u'NetCapFeature': True,
    u'ImageId': u'bsi-l4bd2p',
    u'AutoRenew': u'Yes',
    u'IsExpire': u'No',
    u'TotalDiskSpace': 20,
    u'OsType': u'Linux',
    u'DiskSet': [
        {
            u'Encrypted': u'No',
            u'Drive': u'/dev/vda',
            u'BackupType': u'BASIC_SNAPSHOT',
            u'Type': u'Boot',
            u'DiskId': u'bsi-l4bd2p',
            u'Size': 20
        },
        {
            u'Name': u'\u6570\u636e\u76d8_cmp',
            u'Encrypted': u'No',
            u'Drive': u'/dev/vdb',
            u'BackupType': u'BASIC_SNAPSHOT',
            u'Type': u'Udisk',
            u'DiskId': u'bs-ps5pca',
            u'Size': 20
        }
    ],
    u'SubnetType': u'Default',
    u'Remark': u'',
    u'Name': u'cmp',
    u'UHostId': u'uhost-kltgdo',
    u'GPU': 0,
    u'StorageType': u'UDisk',
    u'HotplugFeature': False,
    u'UHostType': u'Normal',
    u'BasicImageId': u'uimage-5sr2eq',
    u'ExpireTime': 1502876007,
    u'Tag': u'web',
    u'NetworkState': u'Connected',
    u'ChargeType': u'Dynamic',
    u'CreateTime': 1502872404,
    u'TimemachineFeature': u'no'
}
"""
def syncUcloud(accountModel):
    if accountModel is None:
        res = {
            'result': False,
            'message': "同步失败",
        }
        return render_json(res)

    public_key = accountModel.cloud_public_key
    private_key = accountModel.cloud_private_key
    cloud_region = accountModel.cloud_region
    print cloud_region
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    if cloud_region is not None:
        Parameters={
            "Action":"DescribeUHostInstance",
            "Region":cloud_region,
        }
    else:
        Parameters={
            "Action":"DescribeUHostInstance",
            "Region":"cn-sh2",
        }

    print Parameters
    response = ApiClient.get("/", Parameters)

    totalCount = response['TotalCount']
    uHostSet = response['UHostSet']

    try:
        #判断主机是否为空
        if uHostSet is not None and totalCount>0:
            for host in uHostSet:
               print "host ....."
               ucloudHost = UcloudInstance()
               ucloudHost.zone = host['Zone']
               ucloudHost.osName = host['OsName']
               ucloudHost.hostType = host['HostType']
               ucloudHost.state = host['State']
               ucloudHost.memory = host['Memory']
               ucloudHost.netCapability = host['NetCapability']
               ucloudHost.bootDiskState = host['BootDiskState']
               ucloudHost.autoRenew = host['AutoRenew']
               ucloudHost.basicImageId = host['BasicImageId']
               ucloudHost.basicImageName = host['BasicImageName']
               ucloudHost.cpu = host['CPU']
               ucloudHost.chargeType = host['ChargeType']

               createTime = datetime.datetime.fromtimestamp(float(host['CreateTime']))
               expireTime = datetime.datetime.fromtimestamp(float(host['ExpireTime']))
               print createTime
               print expireTime
               ucloudHost.createTime = createTime
               ucloudHost.expireTime = expireTime
               ucloudHost.gpu = host['GPU']
               ucloudHost.hotplugFeature = host['HotplugFeature']
               ucloudHost.imageId = host['ImageId']
               ucloudHost.isExpire = host['IsExpire']
               ucloudHost.name = host['Name']
               ucloudHost.netCapFeature = host['NetCapFeature']
               ucloudHost.memory = host['Memory']
               ucloudHost.networkState = host['NetworkState']
               ucloudHost.osType = host['OsType']
               ucloudHost.remark = host['Remark']
               ucloudHost.storageType = host['StorageType']
               ucloudHost.subnetType = host['SubnetType']
               ucloudHost.tag = host['Tag']
               ucloudHost.timemachineFeature = host['TimemachineFeature']
               ucloudHost.totalDiskSpace = host['TotalDiskSpace']
               ucloudHost.uHostId = host['UHostId']
               ucloudHost.uHostType = host['UHostType']
               ucloudHost.save()
    except Exception as e:
        print str(e)
        traceback.print_exc()
        res = {
            'result': False,
            'message': "同步失败",
        }
        return render_json(res)

    print "res ....."
    res = {
        'result': True,
        'message': "同步成功",
    }
    return render_json(res)




#获取ucloud虚拟机列表
def getUcloudInstanceList(request):
    logger.info("查询ucloud虚拟机列表")
    instanceList = UcloudInstance.objects.all()
    vmJsonList = []

    from django.forms.models import model_to_dict
    for vm in instanceList:
        tempvm = model_to_dict(vm)
        vmJsonList.append(tempvm)

    res = {
        "recordsTotal": len(instanceList),
        'data': vmJsonList
    }
    return render_json_custom(res)