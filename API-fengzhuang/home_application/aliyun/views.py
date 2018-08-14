# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect

from common.mymako import render_mako_context, render_json
import utils
import json
from home_application.models import *
import traceback
from common.log import logger
import math


def aliyun(request):
    # 这里开始触发缓存数据，确保后续页面访问流畅。
    return render_mako_context(
        request, '/home_application/aliyun/aliyun.html'
    )

'''
查询阿里云虚拟机实例列表
'''
def getAliyunVmList(request):
    try:
        aliyunInstanceInfo.objects.all()
        instanceList = aliyunInstanceInfo.objects.findAllInstances()
        print instanceList
        res = {
            "recordsTotal": len(instanceList),
            'data': instanceList
        }
        return render_json(res)
    except Exception, e:
        traceback.print_exc()
        logger.error('getAliyunVmList is error :', e)
        res = {
            "recordsTotal": 0,
            'data': None
        }
        return render_json(res)


'''
根据账号来同步
'''


def syncAliyun(accountModel):
    try:
        if accountModel is None:
            res = {
                'result': False,
                'message': "同步失败",
            }
            return render_json(res)
        else:
            aliyunAccount = accountModel
            account_name = str(aliyunAccount.cloud_public_key)
            account_password = str(aliyunAccount.cloud_private_key)
            region = str(aliyunAccount.cloud_region)

            # print 'account_name : %s' % account_name
            # print 'account_password : %s' % account_password
            # print 'version : %s' % version
            module = 'ecs.aliyuncs.com'
            '''
            action 对应接口的接口名，请参考产品文档上对应接口的接口名
            '''
            action = 'DescribeInstances'
            version = '2014-05-26'
            PageNumber = 1
            PageSize = 30
            params = {}
            '''调用阿里云api根据需要查询的条件进行服务器列表实例查询'''
            result = utils.getInstances(module, action, account_name, account_password, region, version, PageNumber,
                                        PageSize)
            result = json.loads(result)
            print 'aliyun'
            print result
            import sys
            reload(sys)
            sys.setdefaultencoding('utf8')
            res = result
            '''判断返回的结果中是否包含正常的结果集'''
            if 'Instances' in result and result['Instances']["Instance"] is not None:
                instanceIds = []
                '''查询数据库中已存在的服务器信息'''
                instanceIdList = aliyunInstanceInfo.objects.findAllInstanceIds()
                for t in range(len(instanceIdList)):
                    instanceIds.append(str(instanceIdList[t].get('instance_id')))
                # print 'instanceIdList :------ %s' % instanceIdList
                # print 'instanceIds :------ %s' % instanceIds
                myResponse = result.get('Instances')
                # 说明请求成功，可以正常获得结果集
                totalCount = result.get('TotalCount')
                instanceSet = myResponse.get('Instance')
                # print 'totalCount :%s'% totalCount
                # 单次可以取完所有数据
                createInstanceList = []
                updateInstanceList = []
                params['Version'] = version
                params['PageNumber'] = PageNumber
                params['PageSize'] = PageSize
                # '''如果返回的结果小于等于单次查询的最大条数，说明调用api结果获取的服务器信息不需要再次请求接口获取信息的信息'''
                # if totalCount is not None and totalCount <= 100:
                for i in range(len(instanceSet)):
                    '''获取查询的服务器的信息，每个属性进行解析'''
                    myinstance = instanceSet[i]
                    instanceId = str(myinstance.get('InstanceId'))
                    instanceName = str(myinstance.get('InstanceName'))
                    imageId = str(myinstance.get('ImageId'))
                    RegionId = str(myinstance.get('RegionId'))
                    zone = str(myinstance.get('ZoneId'))
                    instanceType = str(myinstance.get('InstanceType'))
                    hostname = str(myinstance.get('HostName'))
                    serial_number = str(myinstance.get('SerialNumber'))
                    status = str(myinstance.get('Status'))
                    security_group_ids = str(','.join(myinstance.get('SecurityGroupIds').get('SecurityGroupId')))
                    publicIp = str(myinstance.get('PublicIpAddress').get('IpAddress')[0])
                    internetMaxBandwidthIn = int(myinstance.get('InternetMaxBandwidthIn'))
                    internetMaxBandwidthOut = int(myinstance.get('InternetMaxBandwidthOut'))
                    internetChargeType = str(myinstance.get('InternetChargeType'))
                    createdTime = myinstance.get('CreationTime')
                    expiredTime = myinstance.get('ExpiredTime')
                    createdTime = utils.utc_to_local(createdTime)
                    expiredTime = utils.utc_to_local(expiredTime)
                    VpcAttributes = str(myinstance.get('VpcAttributes'))
                    EipAddress = str(myinstance.get('EipAddress'))
                    inneripaddress = str(myinstance.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[0])
                    InstanceNetworkType = str(myinstance.get('InstanceNetworkType'))
                    OperationLocks = str(myinstance.get('OperationLocks'))
                    instanceChargeType = str(myinstance.get('InternetChargeType'))
                    DeviceAvailable = str(myinstance.get('DeviceAvailable'))
                    IoOptimized = str(myinstance.get('IoOptimized'))
                    Cpu =myinstance.get('Cpu')
                    Memory=myinstance.get('Memory')
                    InstanceTypeFamily=str(myinstance.get('InstanceTypeFamily'))
                    SpotStrategy=str(myinstance.get('SpotStrategy'))
                    NetworkInterfaces=str(myinstance.get('NetworkInterfaces'))

                    '''组装阿里云服务器实例对象'''
                    instance = aliyunInstanceInfo()
                    instance.instance_id = instanceId
                    instance.instance_name = instanceName
                    instance.description = ""
                    instance.image_id = imageId
                    instance.region_id = RegionId
                    instance.zone = zone
                    instance.cpu = Cpu
                    instance.memory = Memory
                    instance.instance_type = instanceType
                    instance.instance_type_family = InstanceTypeFamily
                    instance.hostname = hostname
                    instance.serial_number = serial_number
                    instance.status = status
                    instance.security_group_ids = security_group_ids
                    instance.public_ip_addresses = publicIp
                    instance.internet_max_bandwidth_out = internetMaxBandwidthOut
                    instance.internet_max_bandwidth_in = internetMaxBandwidthIn
                    instance.internet_charge_type = internetChargeType
                    instance.created_time = createdTime
                    instance.expired_time = expiredTime
                    instance.vpc_attributes = VpcAttributes
                    instance.eip_address = EipAddress
                    instance.inner_ip_address = inneripaddress
                    instance.instance_network_type = InstanceNetworkType
                    instance.operation_locks = OperationLocks
                    instance.instance_charge_type = instanceChargeType
                    instance.spot_strategy = SpotStrategy
                    instance.device_available = DeviceAvailable
                    instance.deployment_setId = ""
                    instance.network_interfaces = NetworkInterfaces
                    instance.io_optimized = IoOptimized
                    instance.key_pair_name = ""

                    '''判断该服务器信息是否在数据库中存在，如果存在进行更新操作，如果不存在进行创建操作'''
                    if instanceId in instanceIds:
                        updateInstanceList.append(instance)
                        # print 'update instance ---------- %s' % updateInstanceList
                    else:
                        createInstanceList.append(instance)
                    key = 'InstanceIds.' + str(i + 1)
                    params[key] = instanceId
                '''调用获取服务器实例状态列表的接口，把上面查询的所有服务器的状态都查出来，因为腾讯云不支持状态和实例一同查询，所以只能分开进行查询'''
                statusrs = utils.getInstances(module, 'DescribeInstanceStatus', account_name, account_password, region,
                                              version, PageNumber, PageSize)
                statusrs = json.loads(statusrs)
                print 'aliyun-status'
                print statusrs
                if 'InstanceStatuses' in statusrs and statusrs.get('InstanceStatuses').get(
                        'InstanceStatus') is not None:
                    statusResponse = statusrs.get('InstanceStatuses')
                    # 说明请求成功，可以正常获得结果集
                    statustotalCount = statusrs.get('TotalCount')
                    InstanceStatusSet = statusResponse.get('InstanceStatus')
                    statusdict = {}
                    '''解析服务器实例列表状态并进行更新封装'''
                    if totalCount == statustotalCount:
                        for m in range(len(InstanceStatusSet)):
                            instanceStatus = InstanceStatusSet[m]
                            instanceId = instanceStatus.get('InstanceId')
                            instanceState = instanceStatus.get('Status')
                            statusdict[instanceId] = instanceState
                        for j in range(len(createInstanceList)):
                            getinstance = createInstanceList[j]
                            finalstatus = statusdict.get(getinstance.instance_id)
                            getinstance.status = finalstatus
                        for k in range(len(updateInstanceList)):
                            updateinstance = updateInstanceList[k]
                            updatefinalstatus = statusdict.get(updateinstance.instance_id)
                            # print 'updatefinalstatus : ---- %s' % updatefinalstatus
                            updateObject = aliyunInstanceInfo.objects.get(instance_id=updateinstance.instance_id)
                            # print 'updateObject : ---- %s' % updateObject
                            updateObject.instance_id = updateinstance.instance_id
                            updateObject.instance_name = updateinstance.instance_name
                            updateObject.description = updateinstance.description
                            updateObject.image_id = updateinstance.description
                            updateObject.region_id = updateinstance.description
                            updateObject.zone = updateinstance.description
                            updateObject.cpu = updateinstance.description
                            updateObject.memory = updateinstance.description
                            updateObject.instance_type = updateinstance.description
                            updateObject.instance_type_family = updateinstance.description
                            updateObject.hostname = updateinstance.description
                            updateObject.serial_number = updateinstance.description
                            updateObject.status = updatefinalstatus
                            updateObject.security_group_ids = updateinstance.security_group_ids
                            updateObject.public_ip_addresses = updateinstance.public_ip_addresses
                            updateObject.internet_max_bandwidth_out = updateinstance.internet_max_bandwidth_out
                            updateObject.internet_max_bandwidth_in = updateinstance.internet_max_bandwidth_in
                            updateObject.internet_charge_type = updateinstance.internet_charge_type
                            updateObject.created_time = updateinstance.created_time
                            updateObject.expired_time = updateinstance.expired_time
                            updateObject.vpc_attributes = updateinstance.vpc_attributes
                            updateObject.eip_address = updateinstance.eip_address
                            updateObject.inner_ip_address = updateinstance.inner_ip_address
                            updateObject.instance_network_type = updateinstance.instance_network_type
                            updateObject.operation_locks = updateinstance.operation_locks
                            updateObject.instance_charge_type = updateinstance.instance_charge_type
                            updateObject.spot_strategy = updateinstance.spot_strategy
                            updateObject.device_available = updateinstance.device_available
                            updateObject.deployment_setId = updateinstance.deployment_setId
                            updateObject.network_interfaces = updateinstance.network_interfaces
                            updateObject.io_optimized = updateinstance.io_optimized
                            updateObject.key_pair_name = updateinstance.key_pair_name
                            updateObject.save()
                        if createInstanceList is not None and len(createInstanceList) > 0:
                            aliyunInstanceInfo.objects.bulk_create(createInstanceList)
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
                    num = int(math.ceil(float(totalCount) / PageSize))
                    for i in range(num, -1, -1):
                        Offset = (i + 1) * PageSize + 1
                        params = {}
                        '''调用阿里云api根据需要查询的条件进行服务器列表实例查询'''
                        result = utils.getInstances(module, action, account_name, account_password, region, version,
                                                    PageNumber, PageSize)
                        result = json.loads(result)
                        print 'aliyun'
                        print result
                        import sys
                        reload(sys)
                        sys.setdefaultencoding('utf8')
                        res = result
                        '''判断返回的结果中是否包含正常的结果集'''
                        if 'Instances' in result and result['Instances']["Instance"] is not None:
                            instanceIds = []
                            '''查询数据库中已存在的服务器信息'''
                            instanceIdList = aliyunInstanceInfo.objects.findAllInstanceIds()
                            for t in range(len(instanceIdList)):
                                instanceIds.append(str(instanceIdList[t].get('instance_id')))
                            # print 'instanceIdList :------ %s' % instanceIdList
                            # print 'instanceIds :------ %s' % instanceIds
                            myResponse = result.get('Instances')
                            # 说明请求成功，可以正常获得结果集
                            totalCount = result.get('TotalCount')
                            instanceSet = myResponse.get('Instance')
                            # print 'totalCount :%s'% totalCount
                            # 单次可以取完所有数据
                            createInstanceList = []
                            updateInstanceList = []
                            params['Version'] = version
                            params['PageNumber'] = PageNumber
                            params['PageSize'] = PageSize
                            # '''如果返回的结果小于等于单次查询的最大条数，说明调用api结果获取的服务器信息不需要再次请求接口获取信息的信息'''
                            # if totalCount is not None and totalCount <= 100:
                            for i in range(len(instanceSet)):
                                '''获取查询的服务器的信息，每个属性进行解析'''
                                myinstance = instanceSet[i]
                                instanceId = str(myinstance.get('InstanceId'))
                                instanceName = str(myinstance.get('InstanceName'))
                                imageId = str(myinstance.get('ImageId'))
                                RegionId = str(myinstance.get('RegionId'))
                                zone = str(myinstance.get('ZoneId'))
                                instanceType = str(myinstance.get('InstanceType'))
                                hostname = str(myinstance.get('HostName'))
                                serial_number = str(myinstance.get('SerialNumber'))
                                status = str(myinstance.get('Status'))
                                security_group_ids = str(
                                    ','.join(myinstance.get('SecurityGroupIds').get('SecurityGroupId')))
                                publicIp = str(myinstance.get('PublicIpAddress').get('IpAddress')[0])
                                internetMaxBandwidthIn = int(myinstance.get('InternetMaxBandwidthIn'))
                                internetMaxBandwidthOut = int(myinstance.get('InternetMaxBandwidthOut'))
                                internetChargeType = str(myinstance.get('InternetChargeType'))
                                createdTime = myinstance.get('CreationTime')
                                expiredTime = myinstance.get('ExpiredTime')
                                createdTime = utils.utc_to_local(createdTime)
                                expiredTime = utils.utc_to_local(expiredTime)
                                VpcAttributes = str(myinstance.get('VpcAttributes'))
                                EipAddress = str(myinstance.get('EipAddress'))
                                inneripaddress = str(myinstance.get('InnerIpAddress'))
                                InstanceNetworkType = str(myinstance.get('InstanceNetworkType'))
                                OperationLocks = str(myinstance.get('OperationLocks'))
                                instanceChargeType = str(myinstance.get('InternetChargeType'))
                                DeviceAvailable = str(myinstance.get('DeviceAvailable'))
                                IoOptimized = str(myinstance.get('IoOptimized'))
                                Cpu = myinstance.get('Cpu')
                                Memory = myinstance.get('Memory')
                                InstanceTypeFamily = str(myinstance.get('InstanceTypeFamily'))
                                SpotStrategy = str(myinstance.get('SpotStrategy'))
                                NetworkInterfaces = str(myinstance.get('NetworkInterfaces'))

                                '''组装阿里云服务器实例对象'''
                                instance = aliyunInstanceInfo()
                                instance.instance_id = instanceId
                                instance.instance_name = instanceName
                                instance.description = ""
                                instance.image_id = imageId
                                instance.region_id = RegionId
                                instance.zone = zone
                                instance.cpu = Cpu
                                instance.memory = Memory
                                instance.instance_type = instanceType
                                instance.instance_type_family = InstanceTypeFamily
                                instance.hostname = hostname
                                instance.serial_number = serial_number
                                instance.status = status
                                instance.security_group_ids = security_group_ids
                                instance.public_ip_addresses = publicIp
                                instance.internet_max_bandwidth_out = internetMaxBandwidthOut
                                instance.internet_max_bandwidth_in = internetMaxBandwidthIn
                                instance.internet_charge_type = internetChargeType
                                instance.created_time = createdTime
                                instance.expired_time = expiredTime
                                instance.vpc_attributes = VpcAttributes
                                instance.eip_address = EipAddress
                                instance.inner_ip_address = inneripaddress
                                instance.instance_network_type = InstanceNetworkType
                                instance.operation_locks = OperationLocks
                                instance.instance_charge_type = instanceChargeType
                                instance.spot_strategy = SpotStrategy
                                instance.device_available = DeviceAvailable
                                instance.deployment_setId = ""
                                instance.network_interfaces = NetworkInterfaces
                                instance.io_optimized = IoOptimized
                                instance.key_pair_name = ""

                                '''判断该服务器信息是否在数据库中存在，如果存在进行更新操作，如果不存在进行创建操作'''
                                if instanceId in instanceIds:
                                    updateInstanceList.append(instance)
                                    # print 'update instance ---------- %s' % updateInstanceList
                                else:
                                    createInstanceList.append(instance)
                                key = 'InstanceIds.' + str(i + 1)
                                params[key] = instanceId
                            '''调用获取服务器实例状态列表的接口，把上面查询的所有服务器的状态都查出来，因为腾讯云不支持状态和实例一同查询，所以只能分开进行查询'''
                            statusrs = utils.getInstances(module, 'DescribeInstanceStatus', account_name,
                                                          account_password, region, version, PageNumber, PageSize)
                            statusrs = json.loads(statusrs)
                            print 'aliyun-status'
                            print statusrs
                            if 'InstanceStatuses' in statusrs and statusrs.get('InstanceStatuses').get(
                                    'InstanceStatus') is not None:
                                statusResponse = statusrs.get('InstanceStatuses')
                                # 说明请求成功，可以正常获得结果集
                                statustotalCount = statusrs.get('TotalCount')
                                InstanceStatusSet = statusResponse.get('InstanceStatus')
                                statusdict = {}
                                '''解析服务器实例列表状态并进行更新封装'''
                                if totalCount == statustotalCount:
                                    for m in range(len(InstanceStatusSet)):
                                        instanceStatus = InstanceStatusSet[m]
                                        instanceId = instanceStatus.get('InstanceId')
                                        instanceState = instanceStatus.get('Status')
                                        statusdict[instanceId] = instanceState
                                    for j in range(len(createInstanceList)):
                                        getinstance = createInstanceList[j]
                                        finalstatus = statusdict.get(getinstance.instance_id)
                                        getinstance.status = finalstatus
                                    for k in range(len(updateInstanceList)):
                                        updateinstance = updateInstanceList[k]
                                        updatefinalstatus = statusdict.get(updateinstance.instance_id)
                                        # print 'updatefinalstatus : ---- %s' % updatefinalstatus
                                        updateObject = aliyunInstanceInfo.objects.get(
                                            instance_id=updateinstance.instance_id)
                                        # print 'updateObject : ---- %s' % updateObject
                                        updateObject.instance_id = updateinstance.instance_id
                                        updateObject.instance_name = updateinstance.instance_name
                                        updateObject.description = updateinstance.description
                                        updateObject.image_id = updateinstance.description
                                        updateObject.region_id = updateinstance.description
                                        updateObject.zone = updateinstance.description
                                        updateObject.cpu = updateinstance.description
                                        updateObject.memory = updateinstance.description
                                        updateObject.instance_type = updateinstance.description
                                        updateObject.instance_type_family = updateinstance.description
                                        updateObject.hostname = updateinstance.description
                                        updateObject.serial_number = updateinstance.description
                                        updateObject.status = updatefinalstatus
                                        updateObject.security_group_ids = updateinstance.security_group_ids
                                        updateObject.public_ip_addresses = updateinstance.public_ip_addresses
                                        updateObject.internet_max_bandwidth_out = updateinstance.internet_max_bandwidth_out
                                        updateObject.internet_max_bandwidth_in = updateinstance.internet_max_bandwidth_in
                                        updateObject.internet_charge_type = updateinstance.internet_charge_type
                                        updateObject.created_time = updateinstance.created_time
                                        updateObject.expired_time = updateinstance.expired_time
                                        updateObject.vpc_attributes = updateinstance.vpc_attributes
                                        updateObject.eip_address = updateinstance.eip_address
                                        updateObject.inner_ip_address = updateinstance.inner_ip_address
                                        updateObject.instance_network_type = updateinstance.instance_network_type
                                        updateObject.operation_locks = updateinstance.operation_locks
                                        updateObject.instance_charge_type = updateinstance.instance_charge_type
                                        updateObject.spot_strategy = updateinstance.spot_strategy
                                        updateObject.device_available = updateinstance.device_available
                                        updateObject.deployment_setId = updateinstance.deployment_setId
                                        updateObject.network_interfaces = updateinstance.network_interfaces
                                        updateObject.io_optimized = updateinstance.io_optimized
                                        updateObject.key_pair_name = updateinstance.key_pair_name
                                        updateObject.save()
                                    if createInstanceList is not None and len(createInstanceList) > 0:
                                        aliyunInstanceInfo.objects.bulk_create(createInstanceList)
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
                '''无法获取阿里云服务器正常数据，返回错误结果'''
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
