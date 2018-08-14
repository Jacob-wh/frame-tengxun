# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger

@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y

from pyVim.connect import Disconnect
from models import VcenterVirtualMachine
from hybirdsdk.virtualMachine import VmManage
'''
同步虚拟机信息
'''
@task()
def sync_virtualmachine(templateid,name):
    print u'start updata'
    template_vm_list = VcenterVirtualMachine.objects.filter(id=templateid)
    if len(template_vm_list) == 0:
        print 'tempalte_vm_list'
        pass
    else:
        vcenterVirtualMachineModel = VcenterVirtualMachine.objects.get(id=int(templateid))
        accountModel = vcenterVirtualMachineModel.account
        if accountModel is None:
            print 'accountModel'
            pass
        else:
            vmManager = VmManage(host=accountModel.vcenter_host, user=accountModel.account_name,password=accountModel.account_password, port=accountModel.vcenter_port, ssl=None)
            vm = vmManager.get_vm_by_name(name)
            # 获取virtualMachine信息
            print vm
            summary = vm.summary
            vcenterVirtualMachineModelList = VcenterVirtualMachine.objects.filter(instance_uuid=summary.config.instanceUuid)
            if len(vcenterVirtualMachineModelList) == 0 :
                vcenterVirtualMachineModel = VcenterVirtualMachine()
            else:
                vcenterVirtualMachineModel = vcenterVirtualMachineModelList[0]

            vcenterVirtualMachineModel.name = summary.config.name
            vcenterVirtualMachineModel.vm_pathname = summary.config.vmPathName
            vcenterVirtualMachineModel.guest_fullname = summary.config.guestFullName
            vcenterVirtualMachineModel.power_state = summary.runtime.powerState
            vcenterVirtualMachineModel.instance_uuid = summary.config.instanceUuid
            vcenterVirtualMachineModel.memorySizeMB = summary.config.memorySizeMB

            print summary.config.name
            print summary.runtime.powerState
            print summary.config.vmPathName
            print summary.config.instanceUuid
            print summary.config.memorySizeMB

            if summary.runtime.maxCpuUsage is not None:
                vcenterVirtualMachineModel.maxCpuUsage = summary.runtime.maxCpuUsage
            else:
                vcenterVirtualMachineModel.maxCpuUsage = 0

            if summary.runtime.maxMemoryUsage is not None:
                vcenterVirtualMachineModel.maxMemoryUsage = summary.runtime.maxMemoryUsage
            else:
                vcenterVirtualMachineModel.maxMemoryUsage = 0

            vcenterVirtualMachineModel.guestId = summary.config.guestId
            vcenterVirtualMachineModel.numCpu = summary.config.numCpu
            vcenterVirtualMachineModel.numEthernetCards = summary.config.numEthernetCards
            vcenterVirtualMachineModel.numVirtualDisks = summary.config.numVirtualDisks
            vcenterVirtualMachineModel.overallStatus = summary.overallStatus
            vcenterVirtualMachineModel.storage_committed = summary.storage.committed
            vcenterVirtualMachineModel.storage_unshared = summary.storage.unshared
            vcenterVirtualMachineModel.storage_uncommitted = summary.storage.uncommitted
            if summary.config.template == True:
                vcenterVirtualMachineModel.template = True
            else:
                vcenterVirtualMachineModel.template = False

            if summary.guest != None:
                ip = summary.guest.ipAddress
                print ip
                if ip != None and ip != "":
                    vcenterVirtualMachineModel.ipaddress = ip
            else:
                vcenterVirtualMachineModel.ipaddress = ""
            vcenterVirtualMachineModel.save()
            Disconnect(vmManager)


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    result = async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))

    #调用处理结果
    print u'调用处理结果'
    print result

    #是否处理完毕
    print result.ready()
    logger.info(result)




@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))

