#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = CXH
# __time__ = 17/11/6 下午4:45


from ..base import ComponentAPI


# 系统组件集合类的名称，一般为 Collections + 系统名
class CollectionsVM(object):

    def __init__(self, client):
        self.client = client

        # create_task为组件名，method为请求组件使用的方法，path为组件路径，组件域名为系统默认域名
        self.get_vms_list = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/vm/get_vms_list/',
            description=u'获取虚拟机列表',
        )
        self.close_vm = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/vm/close_vm/',
            description=u'关闭虚拟机',
        )
        self.start_vm = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/vm/start_vm/',
            description=u'开启虚拟机',
        )
        self.reboot_vm = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/vm/reboot_vm/',
            description=u'重启虚拟机',
        )
        self.destroy_vm = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/vm/destroy_vm/',
            description=u'重启虚拟机',
        )
        self.get_vm_vcenter = ComponentAPI(
            client = self.client, method='GET' ,path='/api/c/compapi/vm/get_vm_vcenter/',
            description=u'获取vcenter配置'
        )
        self.get_vm_cluster = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/vm/get_vm_cluster/',
            description=u'获取集群',
        )
        self.get_vm_datastore = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/vm/get_vm_datastore/',
            description=u'获取存储',
        )
        self.get_vm_datacenter = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/vm/get_vm_datacenter/',
            description=u'获取数据中心',
        )
        self.get_vm_flowanalysis = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/vm/get_vm_flowanalysis/',
            description=u'获取流量分析数据',
        )
        self.get_vm_flowanalysis = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/vm/get_vm_memoryanalysis/',
            description=u'获取内存分析数据',
        )
        self.clone_vm = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/vm/clone_vm/',
            description=u'克隆虚拟机',
        )
        self.update_vm_config = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/vm/update_vm_config/',
            description=u'更新虚拟机的配置信息',
        )
        self.sync_cloud_account = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/vm/sync_cloud_account/',
            description=u'同步虚拟机信息',
        )
