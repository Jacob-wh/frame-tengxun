#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = CXH
# __time__ = 17/11/3 下午3:22


from gevent import Greenlet
from blueking.component.base import logger
from common.mymako import render_mako_context, render_json
from home_application.celery_tasks import execute_task
from home_application.models import *
from home_application.vmware.object_convert import convertVmEntityToVcenterVirtualMachine
from hybirdsdk.virtualMachine import VmManage
from pyVmomi import vim
from account.decorators import login_exempt
from pyVim.connect import Disconnect
import time
import traceback
import random
import gevent
import datetime
import threading
import json
import logging
from django.http import HttpRequest

logging.basicConfig(filename='vm-saas.log', level=logging.DEBUG)


#获取虚拟机列表
@login_exempt
def getVirtualMachineList(request):
    logging.info("获取虚拟机列表")
    try:
        #logging.info('请求的数据: %s' % json.dumps(request.body))
        request_data = json.loads(request.body)
        if 'type' in request_data.keys():
            vm_type = int(request_data.get('type'))
            vcenterVirtualMachineObjectList = VcenterVirtualMachine.objects.filter(template=vm_type)
        else:
            vcenterVirtualMachineObjectList = VcenterVirtualMachine.objects.all()
        vmJsonList = []
        from django.forms.models import model_to_dict
        for vm in vcenterVirtualMachineObjectList:
            tempvm = model_to_dict(vm)
            vmJsonList.append(tempvm)
        logger.info("数据：%s" % json.dumps(vmJsonList))
        res = {
            "code": '0',
            "msg": u'获取虚拟机列表成功',
            "recordsTotal": len(vmJsonList),
            'data': vmJsonList,
        }
    except Exception as e:
        res = {
            "code": '50000',
            "msg": e.message,
        }

    return render_json(res)

#关闭虚拟机
@login_exempt
def closeVirtualMachine(request):
    logger.info("关闭虚拟机")
    try:
        if request.method == 'POST':
            vmId = request.POST['vmId']
            print 'vmid is %s ' % vmId
            vcenterVirtualMachineModel = VcenterVirtualMachine.objects.get(id=vmId)
            accountModel = vcenterVirtualMachineModel.account

        if accountModel is None:
            res = {
                'code': '10001',
                'msg': u"关机失败，资源账号错误",
            }
        else:
            vmManager = VmManage(host=accountModel.vcenter_host,user=accountModel.account_name,password=accountModel.account_password,port=accountModel.vcenter_port,ssl=None)
            task = vmManager.stop(vcenterVirtualMachineModel.name)
            result = vmManager.handleTask(task)
            #同步信息
            if result == False:
                res = {
                    'code': '10002',
                    'msg': u"关机失败",
                }
            else:
                vm = vmManager.find_by_uuid(vcenterVirtualMachineModel.instance_uuid)
                vcenterVirtualMachineModel.power_state = vm.summary.runtime.powerState
                vcenterVirtualMachineModel.save()
                res = {
                    'code': '0',
                    'msg': u"关机成功",
                }
    except Exception as e:
        res = {
            'code': '50000',
            'msg': e.message,
        }

    return render_json(res)

#开启虚拟机
@login_exempt
def startVirtualMachine(request):
    logger.info("开启虚拟机")
    try:
        if request.method == 'POST':
            vmId = request.POST['vmId']
            print 'vmid is %s ' % vmId
            vcenterVirtualMachineModel = VcenterVirtualMachine.objects.get(id=vmId)
            accountModel = vcenterVirtualMachineModel.account
            # print accountModel.account_name

        if accountModel is None:
            res = {
                'code': '10011',
                'msg': u"开启失败，资源账号错误",
            }
            return render_json(res)
        else:
            vmManager = VmManage(host=accountModel.vcenter_host,user=accountModel.account_name,password=accountModel.account_password,port=accountModel.vcenter_port,ssl=None)

            task = vmManager.start(vcenterVirtualMachineModel.name)
            result = vmManager.handleTask(task)

            #同步信息
            if result == False:
                res = {
                    'code': '10012',
                    'msg': u"开机失败",
                }
            else:
                vm = vmManager.find_by_uuid(vcenterVirtualMachineModel.instance_uuid)
                vcenterVirtualMachineModel.power_state = vm.summary.runtime.powerState
                vcenterVirtualMachineModel.save()
                res = {
                    'code': '0',
                    'msg': u"开机成功",
                }
    except Exception as e:
        traceback.print_exc()
        res = {
            'code': '50000',
            'msg': "开机失败"
        }

    return render_json(res)

#重启
@login_exempt
def rebootVirtualMachine(request):
    logger.info("重启虚拟机")
    try:
        if request.method == 'POST':
            vmId = request.POST['vmId']
            print 'vmid is %s ' % vmId

            vcenterVirtualMachineModel = VcenterVirtualMachine.objects.get(id=vmId)
            accountModel = vcenterVirtualMachineModel.account
            #print accountModel

        if accountModel is None:
            res = {
                'code': '10021',
                'msg': u"重启失败，资源账号错误",
            }
            return render_json(res)
        else:
            vmManager = VmManage(host=accountModel.vcenter_host,user=accountModel.account_name,password=accountModel.account_password,port=accountModel.vcenter_port,ssl=None)

            task = vmManager.reboot(vcenterVirtualMachineModel.name)
            result = vmManager.handleTask(task)

            #同步信息
            if result == False:
                res = {
                    'code': '10022',
                    'msg': u"重启失败",
                }
            else:
                vm = vmManager.find_by_uuid(vcenterVirtualMachineModel.instance_uuid)
                vcenterVirtualMachineModel.power_state = vm.summary.runtime.powerState
                vcenterVirtualMachineModel.save()
                res = {
                    'code': '0',
                    'msg': u"重启成功",
                }

    except Exception as e:
        traceback.print_exc()
        res = {
            'code': '50000',
            'msg': e.message,
        }
    return render_json(res)


#销毁
@login_exempt
def destroyVirtualMachine(request):
    logger.info("销毁虚拟机")
    try:
        if request.method == 'POST':
            vmId = request.POST['vmId']
            vcenterVirtualMachineModel = VcenterVirtualMachine.objects.get(id=vmId)
            accountModel = vcenterVirtualMachineModel.account

        if accountModel is None:
            res = {
                'code': '10031',
                'msg': u"销毁失败，资源账号错误",
            }
            return render_json(res)
        else:
            vmManager = VmManage(host=accountModel.vcenter_host,user=accountModel.account_name,password=accountModel.account_password,port=accountModel.vcenter_port,ssl=None)

            task = vmManager.destroy(vcenterVirtualMachineModel.name)
            result = vmManager.handleTask(task)
            #同步信息
            if result == False:
                res = {
                    'code': '10032',
                    'msg': u"销毁失败",
                }
            else:
                vcenterVirtualMachineModel.delete()
                res = {
                    'code': '0',
                    'msg': u"销毁成功",
                }

    except Exception as e:
        res = {
            'code': '50000',
            'msg': e.message,
        }
    return render_json(res)

#查询vcenter账号配置
@login_exempt
def getVcenterAccountList(request):
    logger.info("查询配置vcenter配置")

    try:
        accountObjectList = VcenterAccount.objects.filter(cloud_provider='vmware')
        accountJsonList = []
        from django.forms.models import model_to_dict
        for account in accountObjectList:
            tempAccount = model_to_dict(account)
            accountJsonList.append(tempAccount)

        res = {
            "code": '0',
            "msg": u'获取vcenter列表成功',
            "recordsTotal": len(accountObjectList),
            'data': accountJsonList,
        }
    except Exception as e:
        res = {
            "code": '50000',
            "msg": e.message,
        }

    return render_json(res)


#克隆虚拟机
def cloneVmRequest(request):
    logger.info("克隆虚拟机")
    try:
        if request.method == 'POST':
            vmId = request.POST['vmId']
            vmName = request.POST['vmName']
            vmDatacenter = request.POST['vmDatacenter']
            vmCluster = request.POST['vmCluster']
            vmDatastore = request.POST['vmDatastore']

            print 'vmid is %s, vmName is %s , vmDatacenter is %s, vmCluster is %s, vmDatastore is %s '.format(vmId,vmName,vmDatacenter,vmCluster,vmDatastore)
            vcenterVirtualMachineModel = VcenterVirtualMachine.objects.get(id=vmId)
            accountModel = vcenterVirtualMachineModel.account

        if accountModel is None:
            res = {
                'result': True,
                'message': u"克隆失败，资源账号错误",
            }
            return render_json(res)
        else:
            vmManager = VmManage(host=accountModel.vcenter_host,user=accountModel.account_name,password=accountModel.account_password,port=accountModel.vcenter_port,ssl=None)

            template = vmManager.get_vm_by_name(vcenterVirtualMachineModel.name)
            # print template
            result = vmManager.clone(template=template,
                                     vm_name=vmName,
                                     datacenter_name=vmDatacenter,
                                     vm_folder=None,
                                     datastore_name=vmDatastore,
                                     cluster_name=vmCluster,
                                     resource_pool=None,
                                     power_on=True)

            #同步信息
            if result == False:
                res = {
                    'result': True,
                    'message': u"克隆失败",
                }
            else:
                # vm = vmManager.find_by_uuid(vcenterVirtualMachineModel.instance_uuid)
                # vcenterVirtualMachineModel.power_state = vm.summary.runtime.powerState
                vm = vmManager.get_vm_by_name(vmName)
                cloneVmModel = convertVmEntityToVcenterVirtualMachine(vm)
                #数据中心，需要通过名字查询 todo
                cloneVmModel.datacenter = vcenterVirtualMachineModel.datacenter
                #集群需要通过名字查询 todo
                cloneVmModel.cluster = vcenterVirtualMachineModel.cluster
                cloneVmModel.account = vcenterVirtualMachineModel.account
                cloneVmModel.save()
                res = {
                    'result': True,
                    'message': u"克隆成功",
                }
    except Exception as e:
        traceback.print_exc()
        # print str(e)
        res = {
            'result': False,
            'message': u"克隆失败",
        }
    return render_json(res)


# 获取数据中心
@login_exempt
def getDatacenterList(request):
    logger.info("获取数据中心")
    try:
        request_data = json.loads(request.body)
        if 'vaId' in request_data.keys():
            accountModelList = []
            vaId = int(request_data.get('vaId'))
            logging.info('请求的vaId: %d' % vaId)
            accountModelList = VcenterAccount.objects.filter(id=vaId)
            print vaId
            if len(accountModelList) == 0 :
                logging.info('请求得到的accountModelList长度: %d' % len(accountModelList) )
                res = {
                   'code': '20011',
                   'msg': u'获取数据失败，vcenter账号错误'
                }
            else:
                accountModel = accountModelList[0]
                logging.info('请求获取accountModel对象:')
                vmManager = VmManage(host=accountModel.vcenter_host,user=accountModel.account_name,password=accountModel.account_password,port=accountModel.vcenter_port,ssl=None)
                dataCenters = vmManager.get_datacenters()
                datacenterList = []

                if dataCenters is not None:
                    for datacenter in dataCenters:
                        datacenterList.append({
                            'id': datacenter.name,
                            'text': datacenter.name
                        })

                res = {
                    "code": '0',
                    "msg": u'获取数据中心列表成功',
                    "recordsTotal": len(datacenterList),
                    'data': datacenterList,
                }
        else:
            res = {
                'code': '20012',
                'msg': u'va_id为必须参数'
            }
    except Exception as e:
        print e.message
        logging.info('请求抛出的异常: %s' % e.message)
        res = {
            'code': '50000',
            'msg': e.message
        }
        print res
    return render_json(res)


# 获取数据中心所有的集群
def getClusterByDatacenterList(request):
    res = {}
    return  render_json(res)

# 获取集群
@login_exempt
def getClusterList(request):
    logger.info("获取集群")
    try:
        request_data = json.loads(request.body)
        if 'vaId' in request_data.keys():
            accountModelList = []
            vaId = int(request_data.get('vaId'))
            logging.info('请求的vaId: %d' % vaId)
            accountModelList = VcenterAccount.objects.filter(id=vaId)

            if len(accountModelList) == 0:
                logging.info('请求的accountModelList的长度: %d' % len(accountModelList))
                res = {
                    'code': '30011',
                    'msg': u'获取数据失败，vcenter账号错误'
                }
            else:
                accountModel = accountModelList[0]
                logging.info('获得accountModel对象')
                vmManage = VmManage(host=accountModel.vcenter_host,user=accountModel.account_name,password=accountModel.account_password,port=accountModel.vcenter_port,ssl=None)
                clisters = vmManage.get_cluster_pools()
                clisterList = []
                if clisters is not None:
                    for cluster in clisters:
                       clisterList.append({
                           'id': cluster.name,
                           'text': cluster.name
                       })

                res = {
                    'code': '0',
                    'msg': u'获取集群列表成功',
                    'recordsTotal': len(clisterList),
                    'data': clisterList
                }
        else:
            res = {
                'code': '30012',
                'msg': u'va_id为必须参数'
            }
    except Exception as e:
        logging.info('请求抛出的异常：%s',e.message)
        res = {
            'code': '50000',
            'msg': e.message
        }
    return render_json(res)


# 获取存储
@login_exempt
def getDatastoreList(request):
    logger.info("获取存储")
    try:
        request_data = json.loads(request.body)
        if 'vaId' in request_data.keys():
            accountModelList = []
            vaId = int(request_data.get('vaId'))
            logging.info('请求的vaId: %d' % vaId)
            accountModelList = VcenterAccount.objects.filter(id=vaId)
            if len(accountModelList) ==0 :
                logging.info('请求的accountModelList的长度: %d' % len(accountModelList))
                res = {
                    'code': '40011',
                    'msg': u'获取数据失败，vcenter账号错误'
                }
            else:
                accountModel = accountModelList[0]
                logging.info('获取accountModel对象')
                vmManage = VmManage(host=accountModel.vcenter_host,user=accountModel.account_name,password=accountModel.account_password,port=accountModel.vcenter_port,ssl=None)
                datastores = vmManage.get_datastores()
                datastoresList = []
                if datastores is not None:
                    for datastore in datastores:
                        datastoresList.append({
                           'id': datastore.name,
                           'text': datastore.name
                       })
                res = {
                    'code': '0',
                    'msg': u'获取存储列表成功',
                    'recordsTotal': len(datastoresList),
                    'data': datastoresList
                }
        else:
            logging.info('没有va_id参数')
            res = {
                'code': '40012',
                'msg': u'va_id为必须参数'
            }
    except Exception as e:
        logging.info('请求抛出的异常：%s', e.message)
        res = {
            'code': '50000',
            'msg': e.message
        }

    return render_json(res)


#获取流量分析数据
@login_exempt
def getFlowAnalysisList(request):
    logging.info('获取流量分析数据')
    try:
        request_data = json.load(request.body)
        #request_data = request.GET
        if 'vaId' in request_data.keys():
            vaId = int(request_data.get('vaId'))
            accountModelList = VcenterAccount.objects.filter(id=vaId)
            if len(accountModelList) == 0:
                logging.info('请求的accountModelList的长度: %d' % len(accountModelList))
                res = {
                    'code': '51011',
                    'msg': u'获取数据失败，vcenter账号错误'
                }
            else:
                accountModel = accountModelList[0]
                logging.info('请求获取accountModel')
                vmManager = VmManage(host=accountModel.vcenter_host, user=accountModel.account_name,password=accountModel.account_password, port=accountModel.vcenter_port, ssl=None)
                clusters = vmManager.get_cluster_pools()

                storageList = []
                memroyList = []
                cpuList = []
                cpuCoresList = []

                analysis_data ={
                    'storage': [],
                    'memroy': [],
                    'cpu': [],
                    'cpuCores': []
                }
                for cluster in clusters :
                    datastores = cluster.datastore
                    clusterForDatastoreTotal = 0
                    # if len(datastores) > 0 :
                    #     for datastore in datastores:
                    #         clusterForDatastoreTotal += datastore.summary.capacity

                    memroyList.append({'category': cluster.name, 'value': cluster.summary.totalMemory})
                    cpuList.append({'category': cluster.name, 'value': cluster.summary.totalCpu})
                    storageList.append({'category': cluster.name, 'value': clusterForDatastoreTotal / 1000})
                    cpuCoresList.append({'category': cluster.name, 'value': cluster.summary.numCpuCores})
                analysis_data['memroy'] = memroyList
                analysis_data['cpu'] = cpuList
                analysis_data['storage'] = storageList
                analysis_data['cpuCores'] = cpuCoresList

                res = {
                    'code': '0',
                    'msg': '获取流量分析数据成功',
                    'data': analysis_data
                }
        else:
            res = {
                'code': '51012',
                'msg': u'va_id为必须参数'
            }
    except Exception as e:
        res = {
            'code':'50000',
            'msg': e.message
        }
    return render_json(res)

# 获取内存分析数据
@login_exempt
def getMemoryAnalysisList(request):
    logging.info('获取内存分析数据')
    request_data = json.load(request.body)
    if 'vaId' in request_data.keys():
        vaId = int(request_data.get('vaId'))
        accountModelList = VcenterAccount.objects.filter(id=vaId)
        if len(accountModelList) == 0:
            res = {
                'code': '52011',
                'code': u'获取资源错误，vcenter账号错误'
            }
        else:
            accountModel = accountModelList[0]
            vmManager = VmManage(host=accountModel.vcenter_host, user=accountModel.account_name,
                                 password=accountModel.account_password, port=accountModel.vcenter_port, ssl=None)
            res = {}
    else:
        res ={
            'code': '52012',
            'msg':u'va_id为必须参数'
        }
    return render_json(res)


#克隆虚拟机
@login_exempt
def cloneVm(request):
    logging.info('克隆虚拟机')
    try:
        request_data = json.loads(request.body)
        keys = request_data.keys()
        if keys is not None:
            vmParamter = ['template_vm_id', 'new_vm_name', 'vm_datacenter', 'vm_cluster', 'vm_datastore', 'memory',
                                'cpu_num']
            paramCheck = False
            for param in vmParamter:
                if param not in keys:
                    paramCheck = True
                    res = {
                        'code': '60011',
                        'message': '克隆失败，缺少参数 %s' % param
                    }
                    break
            if paramCheck :
                return render_json(res)
            # 模板ID
            templateVmId = request_data.get('template_vm_id')

            # 获取配置信息
            newVmName = request_data.get('new_vm_name')
            vmDatacenter = request_data.get('vm_datacenter')
            vmCluster = request_data.get('vm_cluster')
            vmDatastore = request_data.get('vm_datastore')
            vmMemory = request_data.get('memory')
            cpuNum = request_data.get('cpu_num')


            logging.info('获取vcenter')
            vcenterVirtualMachineModel = VcenterVirtualMachine.objects.get(id=templateVmId)
            accountModel = vcenterVirtualMachineModel.account

            if accountModel is None:
                logging.info('vcenter为空')
                res = {
                    'code': '60012',
                    'message': u"克隆失败，虚拟机账号错误",
                }
                return render_json(res)
            else:
                logging.info('vcenter不为空')
                vmManager = VmManage(host=accountModel.vcenter_host,user=accountModel.account_name,password=accountModel.account_password,port=accountModel.vcenter_port,ssl=None)
                template = vmManager.get_vm_by_name(vcenterVirtualMachineModel.name)

                # vm 配置信息
                vmconf = vim.vm.ConfigSpec(numCPUs=int(cpuNum), memoryMB=int(vmMemory))
                result = vmManager.clone(template=template,
                         vm_name=newVmName,
                         datacenter_name=vmDatacenter,
                         vm_folder=None,
                         datastore_name=vmDatastore,
                         cluster_name=vmCluster,
                         resource_pool=None,
                         power_on=False,
                         vmconf=vmconf
                    )
                logging.info('克隆结果：%s' % str(result))
                # close out connection
                Disconnect(vmManager)

                if result == False:
                    res = {
                        'code': '60013',
                        'message': '虚拟机克隆失败'
                    }
                    return render_json(res)
                else:

                    res = {
                        'code': '0',
                        'message': u"克隆成功",
                    }
                    return render_json(res)
        else:
            res = {
                'code': '60014',
                'message': u"请求方式错误",
            }
            return render_json(res)
    except Exception as e:
        logging.info('程序抛出错误：%s' % e.message )
        res = {
            'code': '50000',
            'message': e.message,
        }
        return render_json(res)

# 同步信息
@login_exempt
def syncCloudAccount(request):

    try:
        if request.method =='POST':
            templateVmId = request.POST['templateVmId']
            vmName = request.POST['vmName']
            if templateVmId is None:
                res = {
                    'code': '60021',
                    'message': '同步失败，缺少参数templateVmId'
                }
                return render_json(res)
            if vmName is None:
                res = {
                    'code': '60022',
                    'message': '同步失败，缺少参数 vmName'
                }
                return render_json(res)

            vcenterVirtualMachineModel = VcenterVirtualMachine.objects.get(id=templateVmId)
            accountModel = vcenterVirtualMachineModel.account
            vmManager = VmManage(host=accountModel.vcenter_host, user=accountModel.account_name,
                                 password=accountModel.account_password, port=accountModel.vcenter_port, ssl=None)

            vm = vmManager.get_vm_by_name(vmName)
            cloneVmModel = convertVmEntityToVcenterVirtualMachine(vm)
            # 数据中心，需要通过名字查询 todo
            cloneVmModel.datacenter = vcenterVirtualMachineModel.datacenter
            # 集群需要通过名字查询 todo
            cloneVmModel.cluster = vcenterVirtualMachineModel.cluster
            cloneVmModel.account = vcenterVirtualMachineModel.account
            cloneVmModel.save()
            res = {
                'code':'0',
                'message':''
            }
        else:
            res = {
                'code':'60023',
                'message':''
            }
    except Exception as e:
        res = {
            'code':'50000' ,
            'message':"同步失败 ,%s" %e.message
        }
    return render_json(res)
#更新虚拟机的配置信息，前期支持cpu和内存的调整，后期会提供更多的配置调整
@login_exempt
def updateVMConfiguration(request):
    logging.info(u'更新虚拟机的配置信息')
    from home_application.celery_tasks import sync_virtualmachine
    try:
        request_data = json.loads(request.body)
        logger.info(u'request_data数据 %s' % request_data)
        keys = request_data.keys()
        logger.info(u'request_data的keys值： %s' % str(keys))
        if keys is not None:
            template_vm_id = request_data.get('template_vm_id')

            vm_name = request_data.get('vm_name')
            vm_address = request_data.get('vm_address')
            vm_subnetmask = request_data.get('vm_subnetmask')
            vm_gateway = request_data.get('vm_gateway')
            dns = request_data.get('dns')

            if vm_name is None :
                # 虚拟机的信息不全无法进行操作
                logger.info(u'vm_name的值: %s' % vm_name)
                res = {
                    'code': '60031',
                    'message': u"调整配置失败，获取虚拟机名称失败",
                }
                return render_json(res)
            if vm_address is None or vm_subnetmask is None or vm_gateway is None or dns is None:
                logger.info(u'配置参数不足')
                res = {
                    'code': '60032',
                    'message': u"调整配置失败，虚拟机配置信息有误",
                }
                return render_json(res)

            # 根据vmid查询vmid在vmware中的具体信息
            vcenterVirtualMachineModel = VcenterVirtualMachine.objects.get(id=int(template_vm_id))
            accountModel = vcenterVirtualMachineModel.account

            if accountModel is None:
                logger.info(u'通过虚拟机模板获取vcenter失败')
                res = {
                    'code': '60033',
                    'message': u"调整配置失败，虚拟机模板账号错误",
                }
                return render_json(res)

            vmManager = VmManage(host=accountModel.vcenter_host, user=accountModel.account_name,password=accountModel.account_password, port=accountModel.vcenter_port, ssl=None)

            template_vm = vmManager.get_vm_by_name(vm_name)
            vmstatus = template_vm.summary.runtime.powerState
            if template_vm is not None:
                if vmstatus == 'poweredOn':
                    logger.info(u'虚拟机没有关闭,无法操作')
                    # 关闭虚拟机
                    res = {
                        'code':'60034',
                        'message':u'虚拟机没有关机，请先关机'
                    }
                    return render_json(res)

                # 获取dns

                dsn_list = str(dns).split('-')
                dsn_list_value = []
                for lst in dsn_list:
                    if lst is not None and lst != '':
                        dsn_list_value.append(lst)
                logging.info(u'获取dsn_list：%s' % str(len(dsn_list_value)))

                if len(dsn_list_value) == 0:
                    logging.info(u'dsn为空')
                    res = {
                        'code': '60035',
                        'message': u'dns至少填一个'
                    }
                    return render_json(res)

                # 调整虚拟机的配置
                adaptermap = vim.vm.customization.AdapterMapping()
                # Network adapter settings
                adaptermap.adapter = vim.vm.customization.IPSettings(
                    ip=vim.vm.customization.FixedIp(ipAddress=vm_address),
                    subnetMask=vm_subnetmask, gateway=vm_gateway)
                # IP
                globalip = vim.vm.customization.GlobalIPSettings(dnsServerList=dsn_list_value)
                ident = vim.vm.customization.LinuxPrep(domain='domain.local', hostName=vim.vm.customization.FixedName(
                    name=vm_name))
                # Putting all these pieces together in a custom spec
                customspec = vim.vm.customization.Specification(nicSettingMap=[adaptermap], globalIPSettings=globalip,
                                                                identity=ident)
                task = template_vm.Customize(spec=customspec)

                result = vmManager.wait_for_task(task)
                Disconnect(vmManager)

                # 同步数据
                sync_virtualmachine.delay(template_vm_id, vm_name)

                if result :
                    logger.info(u'更新虚拟机配置成功 ')
                    res = {
                        'code':'0',
                        'message':u'更新虚拟机配置成功'
                    }
                    return render_json(res)
                else:
                    logger.info(u'更新虚拟机配置失败')
                    res = {
                        'code':'60037',
                        'message':u'更新虚拟机配置失败'
                    }
                    return render_json(res)
        else:
            logger.info(u'传入参数不足 ')
            res = {
                'code': '60036',
                'message': u"调整配置失败，虚拟机信息不存在",
            }
            return render_json(res)
    except Exception as e:
        logger.info('程序抛出异常 %s ' % e.message)
        res ={
            "code": '50000',
            'message': e.message
        }
        return render_json(res)


@login_exempt
def change_vm_cpu(request):
    print('test')
    pass


@login_exempt
def change_vm_disks(request):
    print('test')
    pass


@login_exempt
def change_vm_disk(request, vm_id, disk_id):
    print(vm_id, disk_id)
    pass


@login_exempt
def change_vm_memory(request):
    print('test')
    pass


@login_exempt
def connect_host(request):
    print('test')
    pass


@login_exempt
def create_host(request):
    print('test')
    pass


@login_exempt
def create_vm(request):
    print('test')
    pass


@login_exempt
def delete_host(request):
    print('test')
    pass


@login_exempt
def delete_vm(request):
    print('test')
    pass