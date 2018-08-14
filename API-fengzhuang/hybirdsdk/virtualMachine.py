#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
function:vcenter manage
"""

import traceback

from pyVim.connect import SmartConnectNoSSL,Disconnect
from pyVmomi import vim, vmodl
import time

from common.log import logger

#打印虚拟机对象
def PrintVmInfo(vm, depth=1):
    """
    Print information for a particular virtual machine or recurse into a folder
    or vApp with depth protection
    """
    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = vm.childEntity
        for c in vmList:
            PrintVmInfo(c, depth+1)
        return

    # if this is a vApp, it likely contains child VMs
    # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
    if isinstance(vm, vim.VirtualApp):
        vmList = vm.vm
        for c in vmList:
            PrintVmInfo(c, depth + 1)
        return

    summary = vm.summary
    print("Name       : ", summary.config.name)
    print("Path       : ", summary.config.vmPathName)
    print("Guest      : ", summary.config.guestFullName)
    annotation = summary.config.annotation
    if annotation != None and annotation != "":
        print("Annotation : ", annotation)
    print("State      : ", summary.runtime.powerState)
    if summary.guest != None:
        ip = summary.guest.ipAddress
        if ip != None and ip != "":
            print("IP         : ", ip)
    if summary.runtime.question != None:
        print("Question  : ", summary.runtime.question.text)
    print("")

class   VmManage(object):

    def __init__(self,host,user,password,port,ssl):
        self.host = host
        self.user = user
        self.pwd = password
        self.port = port
        self.sslContext = ssl
        self.client = SmartConnectNoSSL(host=host,
                                      user=user,
                                      pwd=password,
                                      port=443
                                    )
        self.content = self.client.RetrieveContent()

        if not self.client:
           raise Exception("构建虚拟机管理器失败")

    #vcenter执行动作等待
    def wait_for_task(self,task):
        """ wait for a vCenter task to finish """
        task_done = False

        while not task_done:
            print "task.....%s "% task.info.state
            if task.info.state == 'success':
                return True

            if task.info.state == 'error':
                print "there was an error"
                return False

    #根据资源类型和名称，获取资源对象
    def _get_obj(self, vimtype, name):
        """
        Get the vsphere object associated with a given text name
        """
        obj = None
        content = self.client.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj

    def _get_all_objs(self,vimtype,folder=None):
        """
        Get all the vsphere objects associated with a given type
        """
        #obj = {}
        container = None
        if folder is None:
            container = self.content.viewManager.CreateContainerView(self.content.rootFolder, vimtype, True)
        else:
            container = self.content.viewManager.CreateContainerView(folder, vimtype, True)
        # for c in container.view:
        #     obj.update({c: c.name})
        #return obj
        return container.view

    def login_in_guest(self,username, password):
        return vim.vm.guest.NamePasswordAuthentication(username=username,password=password)

    def start_process(self,si, vm, auth, program_path, args=None, env=None, cwd=None):
        cmdspec = vim.vm.guest.ProcessManager.ProgramSpec(arguments=args, programPath=program_path, envVariables=env, workingDirectory=cwd)
        cmdpid = si.content.guestOperationsManager.processManager.StartProgramInGuest(vm=vm, auth=auth, spec=cmdspec)
        return cmdpid

    def is_ready(self,vm):

        while True:
            system_ready = vm.guest.guestOperationsReady
            system_state = vm.guest.guestState
            system_uptime = vm.summary.quickStats.uptimeSeconds
            if system_ready and system_state == 'running' and system_uptime > 90:
                break
            time.sleep(10)

    #获取虚拟机列表
    def get_vms(self,vmFolder=None):
        content = self.client.content
        vmObjectList = None
        if vmFolder is None:
            objView = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine],True)
            vmObjectList = objView.view
        else:
            objView = content.viewManager.CreateContainerView(vmFolder,[vim.VirtualMachine],True)
            vmObjectList = objView.view
        # vmAllList = []
        # content = self.client.RetrieveContent()
        # for child in content.rootFolder.childEntity:
        #     if hasattr(child, 'vmFolder'):
        #         datacenter = child
        #         vmFolder = datacenter.vmFolder
        #         vmList = vmFolder.childEntity
        #         vmAllList.append(vmList)

        return vmObjectList


    def get_vm_by_name(self,name):
        """
        Find a virtual machine by it's name and return it
        """

        return self._get_obj([vim.VirtualMachine], name)

    def get_host_by_name(self, name):
        """
        Find a virtual machine by it's name and return it
        """

        return self._get_obj([vim.HostSystem], name)

    def get_hosts(self,hostFolder):
        """
        Find a virtual machine by it's name and return it
        """

        return self._get_all_objs([vim.HostSystem],hostFolder)

    def get_distributed_virtual_switchs(self,networkFolder):
        """
        获取分布式交换机
        """
        return self._get_all_objs([vim.DistributedVirtualSwitch],None)

    def get_resource_pool(self, name):
        """
        Find a virtual machine by it's name and return it
        """

        return self._get_obj([vim.ResourcePool], name)

    def get_resource_pools(self):
        """
        Returns all resource pools
        """
        return self._get_all_objs([vim.ResourcePool])

    def get_cluster_pools(self,hostFolder=None):
        """
        Returns all resource pools
        """
        return self._get_all_objs([vim.ClusterComputeResource],hostFolder)

    #通过集群名,数据中心名称获取集群
    def get_cluster_by_name(self, cluster_name=None, datacenter=None):
        if datacenter:
            folder = datacenter.hostFolder
        else:
            folder = self.content.rootFolder

        container = self.content.viewManager.CreateContainerView(folder, [vim.ClusterComputeResource], True)
        clusters = container.view
        print clusters
        for cluster in clusters:
            if cluster.name == cluster_name:
                return cluster
        return None

    def get_datastores(self,folder=None):
        """
        Returns all datastores
        """
        return self._get_all_objs([vim.Datastore],folder)

    def get_datastores_info(self):
        content = self.client.RetrieveContent()
        # Search for all ESXi hosts

        objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.HostSystem],
                                                          True)
        #获取主机视图
        esxi_hosts = objview.view
        objview.Destroy()

        datastores = {}
        datastores_all_capacity = 0
        for esxi_host in esxi_hosts:

            # All Filesystems on ESXi host
            storage_system = esxi_host.configManager.storageSystem
            host_file_sys_vol_mount_info = \
                storage_system.fileSystemVolumeInfo.mountInfo

            datastore_dict = {}
            # Map all filesystems
            for host_mount_info in host_file_sys_vol_mount_info:
                # Extract only VMFS volumes
                if host_mount_info.volume.type == "VMFS":
                    extents = host_mount_info.volume.extent
                    datastore_details = {
                        'uuid': host_mount_info.volume.uuid,
                        'capacity': host_mount_info.volume.capacity,
                        'vmfs_version': host_mount_info.volume.version,
                        'local': host_mount_info.volume.local,
                        'ssd': host_mount_info.volume.ssd
                    }
                    datastores_all_capacity+=host_mount_info.volume.capacity

                    extent_arr = []
                    for extent in extents:
                        # create an array of the devices backing the given
                        # datastore
                        extent_arr.append(extent.diskName)
                        # add the extent array to the datastore info
                        datastore_details['extents'] = extent_arr
                        # associate datastore details with datastore name
                        datastore_dict[host_mount_info.volume.name] = datastore_details

            # associate ESXi host with the datastore it sees
            datastores[esxi_host.name] = datastore_dict
            datastores['datastores_all_capacity'] = datastores_all_capacity

        return datastores

    def get_hosts(self,hostFolder):
        """
        Returns all hosts
        """
        return self._get_all_objs([vim.HostSystem],hostFolder)

    def get_hosts_array(self):
        host_view = self.content.viewManager.CreateContainerView(self.content.rootFolder,
                                                            [vim.HostSystem],
                                                            True)
        obj = [host for host in host_view.view]
        host_view.Destroy()
        return obj

    def get_datacenters(self):
        """
        Returns all datacenters
        """
        return self._get_all_objs([vim.Datacenter])

    def get_registered_vms(self):
        """
        Returns all vms
        """
        return self._get_all_objs([vim.VirtualMachine])

    def get_dvs_distributed_virtual_portgroup(self,network_name):
        objview = self.content.viewManager.CreateContainerView(self.content.rootFolder,
                                                          [vim.dvs.DistributedVirtualPortgroup],
                                                          True)
        obj = None
        for view in objview.view:
            if view.name == network_name:
                obj = view
                break
        objview.Destroy()
        return obj

    #通过uuid查询对象
    def find_by_uuid(self,uuid):
        search_index = self.client.content.searchIndex
        obj = search_index.FindByUuid(None,uuid, True, True)
        return obj

    #获取主机端口组
    def get_hosts_portgroups(self,hosts):
        hostPgDict = {}
        for host in hosts:
            pgs = host.config.network.portgroup
            print pgs
            hostPgDict[host] = pgs
        return hostPgDict

    #获取overheadMemory
    def get_overhead_memory(self,vm,host):
        overheadMemory = self.content.overheadMemoryManager.LookupVmOverheadMemory(vm,host)
        print overheadMemory
        return overheadMemory

    #获取dvs的特性
    def get_dvs_featurecapability(self):
        dvsFeature = {}
        dVSFeatureCapability = self.content.dvSwitchManager.QueryDvsFeatureCapability()
        dvsFeature['ipFix'] = dVSFeatureCapability.ipfixSupported
        dvsFeature['vspan'] = dVSFeatureCapability.vspanSupported
        dvsFeature['vmDirectPathGen2'] = dVSFeatureCapability.vmDirectPathGen2Supported
        dvsFeature['multicastSnooping'] = dVSFeatureCapability.multicastSnoopingSupported
        return  dvsFeature

    #获取虚拟机网卡信息
    def get_vm_nics(self,vm):

        hosts = self.get_hosts_array()
        for dev in vm.config.hardware.device:

            if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                dev_backing = dev.backing
                portGroup = None
                vlanId = None
                vSwitch = None

                if hasattr(dev_backing, 'network'):
                    # portGroupKey = dev.backing.port.portgroupKey
                    # dvsUuid = dev.backing.port.switchUuid
                    portGroup = dev.backing.network.name
                    network = self.get_dvs_distributed_virtual_portgroup(portGroup)
                    print network
                    # for p in pgs:
                    #     vlanId = str(p.spec.vlanId)
                    #     vSwitch = str(p.spec.vswitchName)
                    #     print vlanId
                    #     print vSwitch
                    # try:
                    #     #查询分布式交换机
                    #     dvs = self.content.dvSwitchManager.QueryDvsByUuid(dvsUuid)
                    #     print dvs
                    # except:
                    #     portGroup = "** Error: DVS not found **"
                    #     vlanId = "NA"
                    #     vSwitch = "NA"
                    # else:
                    #     pgObj = dvs.LookupDvPortGroup(portGroupKey)
                    #     portGroup = pgObj.config.name
                    #     vlanId = str(pgObj.config.defaultPortConfig.vlan.vlanId)
                    #     vSwitch = str(dvs.name)



    #分析网络流浪
    def get_flows_info(self):
        """
        获取网卡流量信息
        """
        vms = self.get_vms()
        for vm in vms:
            if vm is not None:
                self.get_vm_nics(vm)





    #创建
    def create(self):
        pass

    #克隆
    def clone(self,template,vm_name,datacenter_name,vm_folder,datastore_name,cluster_name,resource_pool,power_on,vmconf):

        #选择克隆的虚拟机存放位置,通过数据中心获取对象
        datacenter = self._get_obj([vim.Datacenter], datacenter_name)
        if vm_folder:
            destfolder = self._get_obj([vim.Folder], vm_folder)
        else:
            destfolder = datacenter.vmFolder

        if datastore_name:
            datastore = self._get_obj([vim.Datastore], datastore_name)
        else:
            datastore = self._get_obj([vim.Datastore], template.datastore[0].info.name)

        # if None, get the first one
        cluster = self._get_obj([vim.ClusterComputeResource], cluster_name)
        if resource_pool:
            resource_pool = self._get_obj([vim.ResourcePool], resource_pool)
        else:
            resource_pool = cluster.resourcePool

        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = power_on
        if vmconf is not None:
            clonespec.config = vmconf
        print "cloning VM..."
        task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)

        return self.wait_for_task(task)




    #关闭虚拟机
    def stop(self,vmnames,uuid=None):
        print 'vm manage stop...'
        content = self.client.content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.VirtualMachine],
                                                          True)
        vmList = objView.view
        objView.Destroy()

        # Find the vm and power it on
        tasks = [vm.PowerOff() for vm in vmList if vm.name in vmnames]

        return tasks

    #操作任务等待处理
    def handleTask(self,tasks=None):
        if tasks is None:
            return False
        else:
            from pyVim.task import WaitForTasks
            try:
                WaitForTasks(tasks=tasks,si=self.client)
            except Exception as e:
                traceback.print_exc()
                print str(e)
                return False

    #开启
    def start(self,vmnames,uuid=None):
        print 'vm manage start...'
        content = self.client.content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.VirtualMachine],
                                                          True)
        vmList = objView.view
        objView.Destroy()

        #如果是多个虚拟机，则返回多个tasks
        tasks = [vm.PowerOn() for vm in vmList if vm.name in vmnames]

        return  tasks


    #重启
    def reboot(self,vmnames,uuid=None):
        print 'vm manage reboot...'
        content = self.client.content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.VirtualMachine],
                                                          True)
        vmList = objView.view
        objView.Destroy()

        #如果是多个虚拟机，则返回多个tasks
        tasks = [vm.RebootGuest() for vm in vmList if vm.name in vmnames]

        return  tasks
        # vm = self.get_vm_by_name(self.client, vmnames)
        # try:
        #     vm.RebootGuest()
        # except:
        #     # forceably shutoff/on
        #     # need to do if vmware guestadditions isn't running
        #     vm.ResetVM_Task()
        #
        # Disconnect(self.client)

    #销毁虚拟机
    def destroy(self,vmnames,uuid=None):
        print 'vm manage reboot...'
        content = self.client.content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.VirtualMachine],
                                                          True)
        vmList = objView.view
        objView.Destroy()

        #如果是多个虚拟机，则返回多个tasks
        tasks = [vm.Destroy_Task() for vm in vmList if vm.name in vmnames]

        return  tasks

    '''根据uuid信息查询虚拟机信息'''
    def get_vm_by_uuid(self,vmUuid):
        content = self.client.content
        vm = None
        if vmUuid:
            search_index = content.searchIndex
            vm = search_index.FindByUuid(None, vmUuid, True, True)
        print vm
        return vm


    def ReconfigVM(self,vm,newCpuNum,newMemory):
        configSpec = vim.vm.VirtualMachineConfigSpec()
        if newCpuNum is not None :
            configSpec.numCPUs(newCpuNum)

        updatetask = vm.ReconfigVM_Task(spec=configSpec)
        # result = updatetask.wait_for_task(updatetask)
        return self.wait_for_task(updatetask)




    '''根据uuid信息查询虚拟机信息'''

    def get_vm_by_uuid(self, vmUuid):
        content = self.client.content
        vm = None
        if vmUuid:
            search_index = content.searchIndex
            vm = search_index.FindByUuid(None, vmUuid, True, True)
        print vm
        return vm

    '''修改虚拟机配置信息（仅实现cpu和内存，待完善）'''
    def reconfigVM(self, vm, newCpuNum, newMemory):
        configSpec = vim.VirtualMachineConfigSpec()
        if newCpuNum is not None:
            configSpec.numCPUs = newCpuNum
        if newMemory is not None:
            configSpec.memoryMB = newMemory
        updatetask = vm.ReconfigVM_Task(spec=configSpec)
        return self.wait_for_task(updatetask)

    '''关闭已知虚拟机'''
    def powerOffvm(self,vm):
        if vm is not None:
            task = vm.PowerOff()
            return self.wait_for_task(task)
        else:
            return None

    ''''#开启已知虚拟机'''
    def powerOnvm(self,vm):
        if vm is not None:
            task = vm.PowerOn()
            return self.wait_for_task(task)
        else:
            return None


    '''为虚拟机创建快照'''
    def createSnapshot(self, vm, name, description,memory,quiesce):
        #如果快照名称为空，给快照创建默认名称：虚拟机名称+当前时间
        desc = None
        if description:
            desc = description
        if memory is None:
            memory = True
        if quiesce is None:
            quiesce = False
        task = vm.CreateSnapshot_Task(name=name,
                                      description=desc,
                                      memory=memory,
                                      quiesce=quiesce)
        return self.wait_for_task(task)

    def revertToSnapshot(self, vm):
        pass
        # task = vm.RevertToSnapshot_Task(name=name,
        #                               description=desc,
        #                               memory=memory,
        #                               quiesce=quiesce)
        # return self.wait_for_task(task)

    def removeAllSnapshots(self, vm):
        task = vm.RemoveAllSnapshots_Task()
        return self.wait_for_task(task)

    '''
    该接口为虚拟机获取监控数据的通用接口，使用者可以根据自己的需求传入相应的监控指标，方法将返回接口的原始数据
    需要调用者进行自主解析，具体的参数如下：
    vm：虚拟机对象
    startTime：获取监控数据的开始时间
    endTime：获取监控数据的结束时间
    intervalId 采集监控数据的间隔
    '''
    def getVmMonitorInfos(self, entityObject, startTime, endTime, intervalId, metricName,maxSample):
        content = self.content
        perfManager = content.perfManager
        perfList = content.perfManager.perfCounter
        perf_dict = {}
        for counter in perfList:
            counter_full = "{}.{}.{}".format(counter.groupInfo.key, counter.nameInfo.key, counter.rollupType)
            perf_dict[counter_full] = counter.key
        print perf_dict
        perfDictID = perf_dict[metricName]
        metricId = vim.PerformanceManager.MetricId(counterId=perfDictID, instance="")

        query = vim.PerformanceManager.QuerySpec(entity=entityObject,metricId=[metricId],intervalId=20,startTime=startTime,endTime=endTime)
        perfResults = perfManager.QueryPerf(querySpec=[query])

        count=0
        output=[]
        if perfResults is not None and len(perfResults):
            for val in perfResults[0].value[0].value:
                perfinfo={}
                val=float(val/100)

                monitor_time = perfResults[0].sampleInfo[count].timestamp
                perfinfo['unix_time']=time.mktime(monitor_time.timetuple())
                perfinfo['value']=val
                output.append(perfinfo)
                count+=1

        return output


    '''根据name信息查询主机信息'''
    def get_host_by_name(self, hostname):
        content = self.client.content
        host = None
        if hostname:
            search_index = content.searchIndex
            host = search_index.FindByDnsName(dnsName=hostname, vmSearch=False)
        # print host
        return host