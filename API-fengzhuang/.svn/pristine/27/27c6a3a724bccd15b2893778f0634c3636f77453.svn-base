# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect

from common.mymako import render_mako_context
from QcloudApi.qcloudapi import QcloudApi
import traceback
from common.mymako import render_mako_context, render_json
from home_application.models import *
import utils
import json
import time
import pytz
import datetime
import math
from common.log import logger

# AKIDuzyiMrVHE4uo7QQVM7i8XsmVs585nTtC
# MXlPuIUVM51rZ9aqz87ukPuENK6kHetA
def qcloud(request):
    # 这里开始触发缓存数据，确保后续页面访问流畅。
    return render_mako_context(request, '/home_application/qcloud/qcloud.html')


'''
查询腾讯云的账号信息
'''
def getQcloudAccountList(request):
    try:
        accountObjectList = VcenterAccount.objects.filter(cloud_provider='qcloud')
        accountJsonList = []
        from django.forms.models import model_to_dict
        for account in accountObjectList:
            tempAccount = model_to_dict(account)
            accountJsonList.append(tempAccount)
        res = {
            "recordsTotal": len(accountObjectList),
            'data': accountJsonList
        }
        return render_json(res)
    except Exception, e:
        traceback.print_exc()
        logger.error('getQcloudAccountList is error :', e)




'''
同步腾讯云的虚拟机实例信息
'''
def syncDescribeInstances(request):
    try:
        accountObjectList = VcenterAccount.objects.filter(cloud_provider='qcloud')
        if accountObjectList is None or len(accountObjectList) <= 0:
            '''腾讯云账号不存在或者没有取到，此时无法进行api的正常调用，直接返回错误'''
            pass
        else:
            qcloudAccount = accountObjectList[0]
            account_name = str(qcloudAccount.account_name)
            account_password = str(qcloudAccount.account_password)
            version = str(qcloudAccount.vcenter_version)
            # print 'account_name : %s' % account_name
            # print 'account_password : %s' % account_password
            # print 'version : %s' % version
            module = 'cvm'
            '''
            action 对应接口的接口名，请参考产品文档上对应接口的接口名
            '''
            action = 'DescribeInstances'
            Offset = 0
            Limit = 100
            params = {}
            '''调用腾讯云api根据需要查询的条件进行服务器列表实例查询'''
            result = utils.getInstances(module, action, account_name, account_password, version, Offset, Limit)
            result = json.loads(result)
            '''判断返回的结果中是否包含正常的结果集'''
            if 'Response' in result and result.get('Response') is not None:
                instanceIds = []
                '''查询数据库中已存在的服务器信息'''
                instanceIdList = QcloudInstanceInfo.objects.findAllInstanceIds()
                for t in range(len(instanceIdList)):
                    instanceIds.append(str(instanceIdList[t].get('instance_id')))
                # print 'instanceIdList :------ %s' % instanceIdList
                # print 'instanceIds :------ %s' % instanceIds
                myResponse = result.get('Response')
                # 说明请求成功，可以正常获得结果集
                totalCount = myResponse.get('TotalCount')
                instanceSet = myResponse.get('InstanceSet')
                # print 'totalCount :%s'% totalCount
                # 单次可以取完所有数据
                createInstanceList = []
                updateInstanceList = []
                params['Version'] = version
                params['Offset'] = Offset
                params['Limit'] = Limit
                # '''如果返回的结果小于等于单次查询的最大条数，说明调用api结果获取的服务器信息不需要再次请求接口获取信息的信息'''
                # if totalCount is not None and totalCount <= 100:
                for i in range(len(instanceSet)):
                    '''获取查询的服务器的信息，每个属性进行解析'''
                    myinstance = instanceSet[i]
                    instanceId = str(myinstance.get('InstanceId'))
                    instanceName = str(myinstance.get('InstanceName'))
                    instanceType = str(myinstance.get('InstanceType'))
                    cpu = int(myinstance.get('CPU'))
                    memory = int(myinstance.get('Memory'))
                    status = 'RUNNING'
                    instanceChargeType = str(myinstance.get('InstanceChargeType'))
                    zone = str(myinstance.get('Placement').get('Zone'))
                    privateIp = str(myinstance.get('PrivateIpAddresses')[0])
                    publicIp = str(myinstance.get('PublicIpAddresses')[0])
                    imageId = str(myinstance.get('ImageId'))
                    osName = str(myinstance.get('OsName'))
                    systemDiskType = str(myinstance.get('SystemDisk').get('DiskType'))
                    systemDiskSize = int(myinstance.get('SystemDisk').get('DiskSize'))
                    internetMaxBandwidthOut = int(myinstance.get('InternetAccessible').get('InternetMaxBandwidthOut'))
                    internetChargeType = str(myinstance.get('InternetAccessible').get('InternetChargeType'))
                    renewFlag = str(myinstance.get('RenewFlag'))
                    createdTime = myinstance.get('CreatedTime')
                    expiredTime = myinstance.get('ExpiredTime')
                    createdTime = utils.utc_to_local(createdTime)
                    expiredTime = utils.utc_to_local(expiredTime)
                    '''组装腾讯云服务器实例对象'''
                    instance = QcloudInstanceInfo()
                    instance.instance_id = instanceId
                    instance.instance_name = instanceName
                    instance.instance_type = instanceType
                    instance.instance_charge_type = instanceChargeType
                    instance.cpu = cpu
                    instance.memory = memory
                    instance.status = status
                    instance.zone = zone
                    instance.private_ip_addresses = privateIp
                    instance.public_ip_addresses = publicIp
                    instance.image_id = imageId
                    instance.os_name = osName
                    instance.system_disk_size = systemDiskSize
                    instance.system_disk_type = systemDiskType
                    instance.internet_charge_type = internetChargeType
                    instance.internet_max_bandwidth_out = internetMaxBandwidthOut
                    instance.renew_flag = renewFlag
                    instance.created_time = createdTime
                    instance.expired_time = expiredTime
                    '''判断该服务器信息是否在数据库中存在，如果存在进行更新操作，如果不存在进行创建操作'''
                    if instanceId in instanceIds:
                        updateInstanceList.append(instance)
                        # print 'update instance ---------- %s' % updateInstanceList
                    else:
                        createInstanceList.append(instance)
                    key = 'InstprintanceIds.' + str(i + 1)
                    params[key] = instanceId
                '''调用获取服务器实例状态列表的接口，把上面查询的所有服务器的状态都查出来，因为腾讯云不支持状态和实例一同查询，所以只能分开进行查询'''
                statusrs = utils.requestQcloud(module, 'DescribeInstancesStatus', account_name, account_password, params)
                statusrs = json.loads(statusrs)
                if 'Response' in statusrs and statusrs.get('Response') is not None:
                    statusResponse = statusrs.get('Response')
                    # 说明请求成功，可以正常获得结果集
                    statustotalCount = statusResponse.get('TotalCount')
                    InstanceStatusSet = statusResponse.get('InstanceStatusSet')
                    statusdict = {}
                    '''解析服务器实例列表状态并进行更新封装'''
                    if totalCount == statustotalCount:
                        for m in range(len(InstanceStatusSet)):
                            instanceStatus = InstanceStatusSet[m]
                            instanceId = instanceStatus.get('InstanceId')
                            instanceState = instanceStatus.get('InstanceState')
                            statusdict[instanceId] = instanceState
                        for j in range(len(createInstanceList)):
                            getinstance = createInstanceList[j]
                            finalstatus = statusdict.get(getinstance.instance_id)
                            getinstance.status = finalstatus
                        for k in range(len(updateInstanceList)):
                            updateinstance = updateInstanceList[k]
                            updatefinalstatus = statusdict.get(updateinstance.instance_id)
                            # print 'updatefinalstatus : ---- %s' % updatefinalstatus
                            updateObject= QcloudInstanceInfo.objects.get(instance_id=updateinstance.instance_id)
                            # print 'updateObject : ---- %s' % updateObject
                            updateObject.instance_id = updateinstance.instance_id
                            updateObject.instance_name = updateinstance.instance_name
                            updateObject.instance_type = updateinstance.instance_type
                            updateObject.instance_charge_type = updateinstance.instance_charge_type
                            updateObject.cpu = updateinstance.cpu
                            updateObject.memory = memory
                            updateObject.status = updatefinalstatus
                            # print ' updateObject.status : ---- %s' % updateObject.status
                            updateObject.zone = updateinstance.zone
                            updateObject.private_ip_addresses = updateinstance.private_ip_addresses
                            updateObject.public_ip_addresses = updateinstance.public_ip_addresses
                            updateObject.image_id = updateinstance.image_id
                            updateObject.os_name = updateinstance.os_name
                            updateObject.system_disk_size = updateinstance.system_disk_size
                            updateObject.system_disk_type = updateinstance.system_disk_type
                            updateObject.internet_charge_type = updateinstance.internet_charge_type
                            updateObject.internet_max_bandwidth_out = updateinstance.internet_max_bandwidth_out
                            updateObject.renew_flag = updateinstance.renew_flag
                            updateObject.created_time = updateinstance.created_time
                            updateObject.expired_time = updateinstance.expired_time
                            updateObject.save()
                        if createInstanceList is not None and len(createInstanceList) > 0:
                            QcloudInstanceInfo.objects.bulk_create(createInstanceList)
                    else:
                        '''如果实例状态的数量与实例数量不一致，说明有些实例没有正常取到状态'''
                        res = {
                            'result': False,
                            'message': u"同步服务器实例信息有误",
                        }
                        return render_json(res)
                # print 'create instance ---------- %s' % createInstanceList
                '''如果返回的结果大于单次查询的最大条数，说明调用api结果获取的服务器信息需要再次请求接口获取信息的信息，循环调用该部分代码，公共部分后面将进行优化抽取'''
                if totalCount is not None and totalCount > 100:
                    num = int(math.ceil(float(totalCount) / Limit))
                    for i in range(num, -1, -1):
                        Offset = (i + 1) * Limit + 1
                        params = {}
                        '''调用腾讯云api根据需要查询的条件进行服务器列表实例查询'''
                        result = utils.getInstances(module, action, account_name, account_password, version, Offset, Limit)
                        result = json.loads(result)
                        '''判断返回的结果中是否包含正常的结果集'''
                        if 'Response' in result and result.get('Response') is not None:
                            instanceIds = []
                            '''查询数据库中已存在的服务器信息'''
                            instanceIdList = QcloudInstanceInfo.objects.findAllInstanceIds()
                            for t in range(len(instanceIdList)):
                                instanceIds.append(str(instanceIdList[t].get('instance_id')))
                            # print 'instanceIdList :------ %s' % instanceIdList
                            # print 'instanceIds :------ %s' % instanceIds
                            myResponse = result.get('Response')
                            # 说明请求成功，可以正常获得结果集
                            totalCount = myResponse.get('TotalCount')
                            instanceSet = myResponse.get('InstanceSet')
                            # print 'totalCount :%s'% totalCount
                            # 单次可以取完所有数据
                            createInstanceList = []
                            updateInstanceList = []
                            params['Version'] = version
                            params['Offset'] = Offset
                            params['Limit'] = Limit
                            # '''如果返回的结果小于等于单次查询的最大条数，说明调用api结果获取的服务器信息不需要再次请求接口获取信息的信息'''
                            # if totalCount is not None and totalCount <= 100:
                            for i in range(len(instanceSet)):
                                '''获取查询的服务器的信息，每个属性进行解析'''
                                myinstance = instanceSet[i]
                                instanceId = str(myinstance.get('InstanceId'))
                                instanceName = str(myinstance.get('InstanceName'))
                                instanceType = str(myinstance.get('InstanceType'))
                                cpu = int(myinstance.get('CPU'))
                                memory = int(myinstance.get('Memory'))
                                status = 'RUNNING'
                                instanceChargeType = str(myinstance.get('InstanceChargeType'))
                                zone = str(myinstance.get('Placement').get('Zone'))
                                privateIp = str(myinstance.get('PrivateIpAddresses')[0])
                                publicIp = str(myinstance.get('PublicIpAddresses')[0])
                                imageId = str(myinstance.get('ImageId'))
                                osName = str(myinstance.get('OsName'))
                                systemDiskType = str(myinstance.get('SystemDisk').get('DiskType'))
                                systemDiskSize = int(myinstance.get('SystemDisk').get('DiskSize'))
                                internetMaxBandwidthOut = int(
                                    myinstance.get('InternetAccessible').get('InternetMaxBandwidthOut'))
                                internetChargeType = str(myinstance.get('InternetAccessible').get('InternetChargeType'))
                                renewFlag = str(myinstance.get('RenewFlag'))
                                createdTime = myinstance.get('CreatedTime')
                                expiredTime = myinstance.get('ExpiredTime')
                                createdTime = utils.utc_to_local(createdTime)
                                expiredTime = utils.utc_to_local(expiredTime)
                                '''组装腾讯云服务器实例对象'''
                                instance = QcloudInstanceInfo()
                                instance.instance_id = instanceId
                                instance.instance_name = instanceName
                                instance.instance_type = instanceType
                                instance.instance_charge_type = instanceChargeType
                                instance.cpu = cpu
                                instance.memory = memory
                                instance.status = status
                                instance.zone = zone
                                instance.private_ip_addresses = privateIp
                                instance.public_ip_addresses = publicIp
                                instance.image_id = imageId
                                instance.os_name = osName
                                instance.system_disk_size = systemDiskSize
                                instance.system_disk_type = systemDiskType
                                instance.internet_charge_type = internetChargeType
                                instance.internet_max_bandwidth_out = internetMaxBandwidthOut
                                instance.renew_flag = renewFlag
                                instance.created_time = createdTime
                                instance.expired_time = expiredTime
                                '''判断该服务器信息是否在数据库中存在，如果存在进行更新操作，如果不存在进行创建操作'''
                                if instanceId in instanceIds:
                                    updateInstanceList.append(instance)
                                    # print 'update instance ---------- %s' % updateInstanceList
                                else:
                                    createInstanceList.append(instance)
                                key = 'InstanceIds.' + str(i + 1)
                                params[key] = instanceId
                            '''调用获取服务器实例状态列表的接口，把上面查询的所有服务器的状态都查出来，因为腾讯云不支持状态和实例一同查询，所以只能分开进行查询'''
                            statusrs = utils.requestQcloud(module, 'DescribeInstancesStatus', account_name,
                                                           account_password, params)
                            statusrs = json.loads(statusrs)
                            if 'Response' in statusrs and statusrs.get('Response') is not None:
                                statusResponse = statusrs.get('Response')
                                # 说明请求成功，可以正常获得结果集
                                statustotalCount = statusResponse.get('TotalCount')
                                InstanceStatusSet = statusResponse.get('InstanceStatusSet')
                                statusdict = {}
                                '''解析服务器实例列表状态并进行更新封装'''
                                if totalCount == statustotalCount:
                                    for m in range(len(InstanceStatusSet)):
                                        instanceStatus = InstanceStatusSet[m]
                                        instanceId = instanceStatus.get('InstanceId')
                                        instanceState = instanceStatus.get('InstanceState')
                                        statusdict[instanceId] = instanceState
                                    for j in range(len(createInstanceList)):
                                        getinstance = createInstanceList[j]
                                        finalstatus = statusdict.get(getinstance.instance_id)
                                        getinstance.status = finalstatus
                                    for k in range(len(updateInstanceList)):
                                        updateinstance = updateInstanceList[k]
                                        updatefinalstatus = statusdict.get(updateinstance.instance_id)
                                        # print 'updatefinalstatus : ---- %s' % updatefinalstatus
                                        updateObject = QcloudInstanceInfo.objects.get(
                                            instance_id=updateinstance.instance_id)
                                        # print 'updateObject : ---- %s' % updateObject
                                        updateObject.instance_id = updateinstance.instance_id
                                        updateObject.instance_name = updateinstance.instance_name
                                        updateObject.instance_type = updateinstance.instance_type
                                        updateObject.instance_charge_type = updateinstance.instance_charge_type
                                        updateObject.cpu = updateinstance.cpu
                                        updateObject.memory = memory
                                        updateObject.status = updatefinalstatus
                                        # print ' updateObject.status : ---- %s' % updateObject.status
                                        updateObject.zone = updateinstance.zone
                                        updateObject.private_ip_addresses = updateinstance.private_ip_addresses
                                        updateObject.public_ip_addresses = updateinstance.public_ip_addresses
                                        updateObject.image_id = updateinstance.image_id
                                        updateObject.os_name = updateinstance.os_name
                                        updateObject.system_disk_size = updateinstance.system_disk_size
                                        updateObject.system_disk_type = updateinstance.system_disk_type
                                        updateObject.internet_charge_type = updateinstance.internet_charge_type
                                        updateObject.internet_max_bandwidth_out = updateinstance.internet_max_bandwidth_out
                                        updateObject.renew_flag = updateinstance.renew_flag
                                        updateObject.created_time = updateinstance.created_time
                                        updateObject.expired_time = updateinstance.expired_time
                                        updateObject.save()
                                    if createInstanceList is not None and len(createInstanceList) > 0:
                                        QcloudInstanceInfo.objects.bulk_create(createInstanceList)
                                else:
                                    '''如果实例状态的数量与实例数量不一致，说明有些实例没有正常取到状态'''
                                    res = {
                                        'result': False,
                                        'message': u"同步服务器实例信息有误",
                                    }
                                    return render_json(res)
                responseResult = {
                    'result': True,
                    "content": {},
                    "message": u"操作成功"
                }
                return render_json(responseResult)

            else:
                '''无法获取腾讯云服务器正常数据，返回错误结果'''
                res = {
                    'result': False,
                    'message': u"同步服务器实例信息有误",
                }
                return render_json(res)
    except Exception, e:
        traceback.print_exc()
        logger.error('syncDescribeInstances is error :', e)
        res = {
            'result': False,
            'message': u"同步服务器实例信息有误",
        }
        return render_json(res)

'''
根据账号来同步
'''
def syncQcloud(accountModel):
    try:
        if accountModel is None:
            res = {
                'result': False,
                'message': "同步失败",
            }
            return render_json(res)
        else:
            qcloudAccount = accountModel
            account_name = str(qcloudAccount.cloud_public_key)
            account_password = str(qcloudAccount.cloud_private_key)
            version = str(qcloudAccount.vcenter_version)
            # print 'account_name : %s' % account_name
            # print 'account_password : %s' % account_password
            # print 'version : %s' % version
            module = 'cvm'
            '''
            action 对应接口的接口名，请参考产品文档上对应接口的接口名
            '''
            action = 'DescribeInstances'
            Offset = 0
            Limit = 100
            params = {}
            '''调用腾讯云api根据需要查询的条件进行服务器列表实例查询'''
            result = utils.getInstances(module, action, account_name, account_password, version, Offset, Limit)
            result = json.loads(result)
            import sys
            reload(sys)
            sys.setdefaultencoding('utf8')
            '''判断返回的结果中是否包含正常的结果集'''
            if 'Response' in result and result.get('Response') is not None:
                instanceIds = []
                '''查询数据库中已存在的服务器信息'''
                instanceIdList = QcloudInstanceInfo.objects.findAllInstanceIds()
                for t in range(len(instanceIdList)):
                    instanceIds.append(str(instanceIdList[t].get('instance_id')))
                # print 'instanceIdList :------ %s' % instanceIdList
                # print 'instanceIds :------ %s' % instanceIds
                myResponse = result.get('Response')
                # 说明请求成功，可以正常获得结果集
                totalCount = myResponse.get('TotalCount')
                instanceSet = myResponse.get('InstanceSet')
                # print 'totalCount :%s'% totalCount
                # 单次可以取完所有数据
                createInstanceList = []
                updateInstanceList = []
                params['Version'] = version
                params['Offset'] = Offset
                params['Limit'] = Limit
                # '''如果返回的结果小于等于单次查询的最大条数，说明调用api结果获取的服务器信息不需要再次请求接口获取信息的信息'''
                # if totalCount is not None and totalCount <= 100:
                for i in range(len(instanceSet)):
                    '''获取查询的服务器的信息，每个属性进行解析'''
                    myinstance = instanceSet[i]
                    instanceId = str(myinstance.get('InstanceId'))
                    instanceName = str(myinstance.get('InstanceName'))
                    instanceType = str(myinstance.get('InstanceType'))
                    cpu = int(myinstance.get('CPU'))
                    memory = int(myinstance.get('Memory'))
                    status = 'RUNNING'
                    instanceChargeType = str(myinstance.get('InstanceChargeType'))
                    zone = str(myinstance.get('Placement').get('Zone'))
                    privateIp = str(myinstance.get('PrivateIpAddresses')[0])
                    publicIp = str(myinstance.get('PublicIpAddresses')[0])
                    imageId = str(myinstance.get('ImageId'))
                    osName = str(myinstance.get('OsName'))
                    systemDiskType = str(myinstance.get('SystemDisk').get('DiskType'))
                    systemDiskSize = int(myinstance.get('SystemDisk').get('DiskSize'))
                    internetMaxBandwidthOut = int(myinstance.get('InternetAccessible').get('InternetMaxBandwidthOut'))
                    internetChargeType = str(myinstance.get('InternetAccessible').get('InternetChargeType'))
                    renewFlag = str(myinstance.get('RenewFlag'))
                    createdTime = myinstance.get('CreatedTime')
                    expiredTime = myinstance.get('ExpiredTime')
                    createdTime = utils.utc_to_local(createdTime)
                    expiredTime = utils.utc_to_local(expiredTime)
                    '''组装腾讯云服务器实例对象'''
                    instance = QcloudInstanceInfo()
                    instance.instance_id = instanceId
                    instance.instance_name = instanceName
                    instance.instance_type = instanceType
                    instance.instance_charge_type = instanceChargeType
                    instance.cpu = cpu
                    instance.memory = memory
                    instance.status = status
                    instance.zone = zone
                    instance.private_ip_addresses = privateIp
                    instance.public_ip_addresses = publicIp
                    instance.image_id = imageId
                    instance.os_name = osName
                    instance.system_disk_size = systemDiskSize
                    instance.system_disk_type = systemDiskType
                    instance.internet_charge_type = internetChargeType
                    instance.internet_max_bandwidth_out = internetMaxBandwidthOut
                    instance.renew_flag = renewFlag
                    instance.created_time = createdTime
                    instance.expired_time = expiredTime
                    '''判断该服务器信息是否在数据库中存在，如果存在进行更新操作，如果不存在进行创建操作'''
                    if instanceId in instanceIds:
                        updateInstanceList.append(instance)
                        # print 'update instance ---------- %s' % updateInstanceList
                    else:
                        createInstanceList.append(instance)
                    key = 'InstanceIds.' + str(i + 1)
                    params[key] = instanceId
                '''调用获取服务器实例状态列表的接口，把上面查询的所有服务器的状态都查出来，因为腾讯云不支持状态和实例一同查询，所以只能分开进行查询'''
                statusrs = utils.requestQcloud(module, 'DescribeInstancesStatus', account_name, account_password, params)
                statusrs = json.loads(statusrs)
                if 'Response' in statusrs and statusrs.get('Response') is not None:
                    statusResponse = statusrs.get('Response')
                    # 说明请求成功，可以正常获得结果集
                    statustotalCount = statusResponse.get('TotalCount')
                    InstanceStatusSet = statusResponse.get('InstanceStatusSet')
                    statusdict = {}
                    '''解析服务器实例列表状态并进行更新封装'''
                    if totalCount == statustotalCount:
                        for m in range(len(InstanceStatusSet)):
                            instanceStatus = InstanceStatusSet[m]
                            instanceId = instanceStatus.get('InstanceId')
                            instanceState = instanceStatus.get('InstanceState')
                            statusdict[instanceId] = instanceState
                        for j in range(len(createInstanceList)):
                            getinstance = createInstanceList[j]
                            finalstatus = statusdict.get(getinstance.instance_id)
                            getinstance.status = finalstatus
                        for k in range(len(updateInstanceList)):
                            updateinstance = updateInstanceList[k]
                            updatefinalstatus = statusdict.get(updateinstance.instance_id)
                            # print 'updatefinalstatus : ---- %s' % updatefinalstatus
                            updateObject= QcloudInstanceInfo.objects.get(instance_id=updateinstance.instance_id)
                            # print 'updateObject : ---- %s' % updateObject
                            updateObject.instance_id = updateinstance.instance_id
                            updateObject.instance_name = updateinstance.instance_name
                            updateObject.instance_type = updateinstance.instance_type
                            updateObject.instance_charge_type = updateinstance.instance_charge_type
                            updateObject.cpu = updateinstance.cpu
                            updateObject.memory = memory
                            updateObject.status = updatefinalstatus
                            # print ' updateObject.status : ---- %s' % updateObject.status
                            updateObject.zone = updateinstance.zone
                            updateObject.private_ip_addresses = updateinstance.private_ip_addresses
                            updateObject.public_ip_addresses = updateinstance.public_ip_addresses
                            updateObject.image_id = updateinstance.image_id
                            updateObject.os_name = updateinstance.os_name
                            updateObject.system_disk_size = updateinstance.system_disk_size
                            updateObject.system_disk_type = updateinstance.system_disk_type
                            updateObject.internet_charge_type = updateinstance.internet_charge_type
                            updateObject.internet_max_bandwidth_out = updateinstance.internet_max_bandwidth_out
                            updateObject.renew_flag = updateinstance.renew_flag
                            updateObject.created_time = updateinstance.created_time
                            updateObject.expired_time = updateinstance.expired_time
                            updateObject.save()
                        if createInstanceList is not None and len(createInstanceList) > 0:
                            QcloudInstanceInfo.objects.bulk_create(createInstanceList)
                    else:
                        '''如果实例状态的数量与实例数量不一致，说明有些实例没有正常取到状态'''
                        res = {
                            'result': False,
                            'message': u"同步服务器实例信息有误",
                        }
                        return render_json(res)
                # print 'create instance ---------- %s' % createInstanceList
                '''如果返回的结果大于单次查询的最大条数，说明调用api结果获取的服务器信息需要再次请求接口获取信息的信息，循环调用该部分代码，公共部分后面将进行优化抽取'''
                if totalCount is not None and totalCount > 100:
                    num = int(math.ceil(float(totalCount) / Limit))
                    for i in range(num, -1, -1):
                        Offset = (i + 1) * Limit + 1
                        params = {}
                        '''调用腾讯云api根据需要查询的条件进行服务器列表实例查询'''
                        result = utils.getInstances(module, action, account_name, account_password, version, Offset, Limit)
                        result = json.loads(result)
                        '''判断返回的结果中是否包含正常的结果集'''
                        if 'Response' in result and result.get('Response') is not None:
                            instanceIds = []
                            '''查询数据库中已存在的服务器信息'''
                            instanceIdList = QcloudInstanceInfo.objects.findAllInstanceIds()
                            for t in range(len(instanceIdList)):
                                instanceIds.append(str(instanceIdList[t].get('instance_id')))
                            # print 'instanceIdList :------ %s' % instanceIdList
                            # print 'instanceIds :------ %s' % instanceIds
                            myResponse = result.get('Response')
                            # 说明请求成功，可以正常获得结果集
                            totalCount = myResponse.get('TotalCount')
                            instanceSet = myResponse.get('InstanceSet')
                            # print 'totalCount :%s'% totalCount
                            # 单次可以取完所有数据
                            createInstanceList = []
                            updateInstanceList = []
                            params['Version'] = version
                            params['Offset'] = Offset
                            params['Limit'] = Limit
                            # '''如果返回的结果小于等于单次查询的最大条数，说明调用api结果获取的服务器信息不需要再次请求接口获取信息的信息'''
                            # if totalCount is not None and totalCount <= 100:
                            for i in range(len(instanceSet)):
                                '''获取查询的服务器的信息，每个属性进行解析'''
                                myinstance = instanceSet[i]
                                instanceId = str(myinstance.get('InstanceId'))
                                instanceName = str(myinstance.get('InstanceName'))
                                instanceType = str(myinstance.get('InstanceType'))
                                cpu = int(myinstance.get('CPU'))
                                memory = int(myinstance.get('Memory'))
                                status = 'RUNNING'
                                instanceChargeType = str(myinstance.get('InstanceChargeType'))
                                zone = str(myinstance.get('Placement').get('Zone'))
                                privateIp = str(myinstance.get('PrivateIpAddresses')[0])
                                publicIp = str(myinstance.get('PublicIpAddresses')[0])
                                imageId = str(myinstance.get('ImageId'))
                                osName = str(myinstance.get('OsName'))
                                systemDiskType = str(myinstance.get('SystemDisk').get('DiskType'))
                                systemDiskSize = int(myinstance.get('SystemDisk').get('DiskSize'))
                                internetMaxBandwidthOut = int(
                                    myinstance.get('InternetAccessible').get('InternetMaxBandwidthOut'))
                                internetChargeType = str(myinstance.get('InternetAccessible').get('InternetChargeType'))
                                renewFlag = str(myinstance.get('RenewFlag'))
                                createdTime = myinstance.get('CreatedTime')
                                expiredTime = myinstance.get('ExpiredTime')
                                createdTime = utils.utc_to_local(createdTime)
                                expiredTime = utils.utc_to_local(expiredTime)
                                '''组装腾讯云服务器实例对象'''
                                instance = QcloudInstanceInfo()
                                instance.instance_id = instanceId
                                instance.instance_name = instanceName
                                instance.instance_type = instanceType
                                instance.instance_charge_type = instanceChargeType
                                instance.cpu = cpu
                                instance.memory = memory
                                instance.status = status
                                instance.zone = zone
                                instance.private_ip_addresses = privateIp
                                instance.public_ip_addresses = publicIp
                                instance.image_id = imageId
                                instance.os_name = osName
                                instance.system_disk_size = systemDiskSize
                                instance.system_disk_type = systemDiskType
                                instance.internet_charge_type = internetChargeType
                                instance.internet_max_bandwidth_out = internetMaxBandwidthOut
                                instance.renew_flag = renewFlag
                                instance.created_time = createdTime
                                instance.expired_time = expiredTime
                                '''判断该服务器信息是否在数据库中存在，如果存在进行更新操作，如果不存在进行创建操作'''
                                if instanceId in instanceIds:
                                    updateInstanceList.append(instance)
                                    # print 'update instance ---------- %s' % updateInstanceList
                                else:
                                    createInstanceList.append(instance)
                                key = 'InstanceIds.' + str(i + 1)
                                params[key] = instanceId
                            '''调用获取服务器实例状态列表的接口，把上面查询的所有服务器的状态都查出来，因为腾讯云不支持状态和实例一同查询，所以只能分开进行查询'''
                            statusrs = utils.requestQcloud(module, 'DescribeInstancesStatus', account_name,
                                                           account_password, params)
                            statusrs = json.loads(statusrs)
                            if 'Response' in statusrs and statusrs.get('Response') is not None:
                                statusResponse = statusrs.get('Response')
                                # 说明请求成功，可以正常获得结果集
                                statustotalCount = statusResponse.get('TotalCount')
                                InstanceStatusSet = statusResponse.get('InstanceStatusSet')
                                statusdict = {}
                                '''解析服务器实例列表状态并进行更新封装'''
                                if totalCount == statustotalCount:
                                    for m in range(len(InstanceStatusSet)):
                                        instanceStatus = InstanceStatusSet[m]
                                        instanceId = instanceStatus.get('InstanceId')
                                        instanceState = instanceStatus.get('InstanceState')
                                        statusdict[instanceId] = instanceState
                                    for j in range(len(createInstanceList)):
                                        getinstance = createInstanceList[j]
                                        finalstatus = statusdict.get(getinstance.instance_id)
                                        getinstance.status = finalstatus
                                    for k in range(len(updateInstanceList)):
                                        updateinstance = updateInstanceList[k]
                                        updatefinalstatus = statusdict.get(updateinstance.instance_id)
                                        # print 'updatefinalstatus : ---- %s' % updatefinalstatus
                                        updateObject = QcloudInstanceInfo.objects.get(
                                            instance_id=updateinstance.instance_id)
                                        # print 'updateObject : ---- %s' % updateObject
                                        updateObject.instance_id = updateinstance.instance_id
                                        updateObject.instance_name = updateinstance.instance_name
                                        updateObject.instance_type = updateinstance.instance_type
                                        updateObject.instance_charge_type = updateinstance.instance_charge_type
                                        updateObject.cpu = updateinstance.cpu
                                        updateObject.memory = memory
                                        updateObject.status = updatefinalstatus
                                        # print ' updateObject.status : ---- %s' % updateObject.status
                                        updateObject.zone = updateinstance.zone
                                        updateObject.private_ip_addresses = updateinstance.private_ip_addresses
                                        updateObject.public_ip_addresses = updateinstance.public_ip_addresses
                                        updateObject.image_id = updateinstance.image_id
                                        updateObject.os_name = updateinstance.os_name
                                        updateObject.system_disk_size = updateinstance.system_disk_size
                                        updateObject.system_disk_type = updateinstance.system_disk_type
                                        updateObject.internet_charge_type = updateinstance.internet_charge_type
                                        updateObject.internet_max_bandwidth_out = updateinstance.internet_max_bandwidth_out
                                        updateObject.renew_flag = updateinstance.renew_flag
                                        updateObject.created_time = updateinstance.created_time
                                        updateObject.expired_time = updateinstance.expired_time
                                        updateObject.save()
                                    if createInstanceList is not None and len(createInstanceList) > 0:
                                        QcloudInstanceInfo.objects.bulk_create(createInstanceList)
                                else:
                                    '''如果实例状态的数量与实例数量不一致，说明有些实例没有正常取到状态'''
                                    res = {
                                        'result': False,
                                        'message': u"同步服务器实例信息有误",
                                    }
                                    return render_json(res)
                responseResult = {
                    'result': True,
                    "content": {},
                    "message": u"操作成功"
                }
                return render_json(responseResult)

            else:
                '''无法获取腾讯云服务器正常数据，返回错误结果'''
                res = {
                    'result': False,
                    'message': u"同步服务器实例信息有误",
                }
                return render_json(res)
    except Exception, e:
        traceback.print_exc()
        logger.error('syncQcloud is error :', e)
        res = {
            'result': False,
            'message': u"同步服务器实例信息有误",
        }
        return render_json(res)




'''
同步镜像信息
'''
def syncImages(request):
    pass



'''
查询腾讯云虚拟机实例列表
'''
def getQcloudVmList(request):
    try:
        QcloudInstanceInfo.objects.all()
        instanceList = QcloudInstanceInfo.objects.findAllInstances()
        # print instanceList
        res = {
            "recordsTotal": len(instanceList),
            'data': instanceList
        }
        return render_json(res)
    except Exception, e:
        traceback.print_exc()
        logger.error('getQcloudVmList is error :', e)
        res = {
            "recordsTotal": 0,
            'data': None
        }
        return render_json(res)



'''
腾讯云启动虚拟机实例
'''
def startQcloudVm(request):
    try:
        vmIds = request.POST.getlist('ids')
        vmInstanceIds = request.POST.getlist('instanceids')
        responseResult = {
            'result': True,
            "content": {},
            "message": u"操作成功"
        }
        if vmIds is None or vmInstanceIds is None or len(vmIds) == 0 or vmInstanceIds == 0:
            # 虚拟机的信息不全无法进行操作
            res = {
                'result': False,
                'message': u"虚拟机信息不正确,无法进行开启操作",
            }
            return render_json(res)
        accountObjectList = VcenterAccount.objects.filter(cloud_provider='qcloud')
        if accountObjectList is None or len(accountObjectList) <= 0:
            # 虚拟机的信息不全无法进行操作
            res = {
                'result': False,
                'message': u"腾讯云账号有误，无法正常使用",
            }
            return render_json(res)
        else:
            qcloudAccount = accountObjectList[0]
            account_name = str(qcloudAccount.account_name)
            account_password = str(qcloudAccount.account_password)
            version = str(qcloudAccount.vcenter_version)
            module = 'cvm'
            action = 'StartInstances'
            '''
            params 请求参数，请参考产品文档上对应接口的说明
            '''
            params = {
                'Version': version
            }
        if len(vmInstanceIds) == 1:
            params['InstanceIds.1'] =vmInstanceIds[0]
        else:
            for i in range(len(vmInstanceIds)):
                key = 'InstanceIds.'+str(i+1)
                params[key] = vmInstanceIds[i]
        result = utils.requestQcloud(module, action, account_name, account_password, params)
        if 'RequestId' in result:
            for i in range(len(vmInstanceIds)):
                instance = QcloudInstanceInfo.objects.get(instance_id=vmInstanceIds[i])
                instance.status = 'RUNNING'
                instance.save()
            return render_json(responseResult)
        else:
            res = {
                'result': False,
                'message': u"操作失败",
            }
            return render_json(res)
    except Exception, e:
        traceback.print_exc()
        logger.error('startQcloudVm is error :', e)
        res = {
            'result': False,
            'message': u"操作失败",
        }
        return render_json(res)



'''
腾讯云停止虚拟机实例
'''
def stopQcloudVm(request):
    try:
        vmIds = request.POST.getlist('ids')
        vmInstanceIds = request.POST.getlist('instanceids')
        responseResult = {
            'result': True,
            "content": {},
            "message": u"操作成功"
        }
        if vmIds is None or vmInstanceIds is None or len(vmIds) == 0 or vmInstanceIds == 0:
            # 虚拟机的信息不全无法进行操作
            res = {
                'result': False,
                'message': u"虚拟机信息不正确,无法进行开启操作",
            }
            return render_json(res)
        accountObjectList = VcenterAccount.objects.filter(cloud_provider='qcloud')
        if accountObjectList is None or len(accountObjectList) <= 0:
            # 虚拟机的信息不全无法进行操作
            res = {
                'result': False,
                'message': u"腾讯云账号有误，无法正常使用",
            }
            return render_json(res)
        else:
            qcloudAccount = accountObjectList[0]
            account_name = str(qcloudAccount.account_name)
            account_password = str(qcloudAccount.account_password)
            version = str(qcloudAccount.vcenter_version)
            module = 'cvm'
            action = 'StopInstances'
            '''
            params 请求参数，请参考产品文档上对应接口的说明
            '''
            params = {
                'Version': version
            }
        if len(vmInstanceIds) == 1:
            params['InstanceIds.1'] = vmInstanceIds[0]
        else:
            for i in range(len(vmInstanceIds)):
                key = 'InstanceIds.' + str(i + 1)
                params[key] = vmInstanceIds[i]
        result = utils.requestQcloud(module, action, account_name, account_password, params)
        if 'RequestId' in result:
            for i in range(len(vmInstanceIds)):
                instance = QcloudInstanceInfo.objects.get(instance_id=vmInstanceIds[i])
                instance.status = 'STOPPED'
                instance.save()
            return render_json(responseResult)
        else:
            res = {
                'result': False,
                'message': u"操作失败",
            }
            return render_json(res)
    except Exception, e:
        traceback.print_exc()
        logger.error('stopQcloudVm is error :', e)
        res = {
            'result': False,
            'message': u"操作失败",
        }
        return render_json(res)


