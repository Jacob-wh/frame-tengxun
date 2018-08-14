# -*- coding: utf-8 -*-
import json

from home_application.models import VcenterVirtualMachine
from pyVmomi import vim, vmodl

def convertVmEntityToVcenterVirtualMachine(vm,depth=1):

    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return None
        vmList = vm.childEntity
        for c in vmList:
            convertVmEntityToVcenterVirtualMachine(c, depth+1)
        return None

    # if this is a vApp, it likely contains child VMs
    # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
    if isinstance(vm, vim.VirtualApp):
        vmList = vm.vm
        for c in vmList:
            convertVmEntityToVcenterVirtualMachine(c, depth + 1)
        return None

    vcenterVirtualMachineModel = VcenterVirtualMachine()
    summary = vm.summary


    """
    runtime
    host = 'vim.HostSystem:host-193',
      connectionState = 'connected',
      powerState = 'poweredOn',
      faultToleranceState = 'notConfigured',
      dasVmProtection = <unset>,
      toolsInstallerMounted = false,
      suspendTime = <unset>,
      bootTime = 2017-07-17T08:54:57.662067Z,
      suspendInterval = 0L,
      question = <unset>,
      memoryOverhead = <unset>,
      maxCpuUsage = 2133,
      maxMemoryUsage = 4096,
      numMksConnections = 0,
      recordReplayState = 'inactive',
      cleanPowerOff = <unset>,
      needSecondaryReason = <unset>,
      onlineStandby = false,
      minRequiredEVCModeKey = <unset>,
      consolidationNeeded = false,
      offlineFeatureRequirement = (vim.vm.FeatureRequirement) [
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.lm',
            featureName = 'cpuid.lm',
            value = 'Bool:Min:1'
         }
      ],
      featureRequirement = (vim.vm.FeatureRequirement) [
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.SSE3',
            featureName = 'cpuid.SSE3',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.SSSE3',
            featureName = 'cpuid.SSSE3',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.CMPXCHG16B',
            featureName = 'cpuid.CMPXCHG16B',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.SSE41',
            featureName = 'cpuid.SSE41',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.SSE42',
            featureName = 'cpuid.SSE42',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.POPCNT',
            featureName = 'cpuid.POPCNT',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.DS',
            featureName = 'cpuid.DS',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.SS',
            featureName = 'cpuid.SS',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.LAHF64',
            featureName = 'cpuid.LAHF64',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.NX',
            featureName = 'cpuid.NX',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.RDTSCP',
            featureName = 'cpuid.RDTSCP',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.LM',
            featureName = 'cpuid.LM',
            value = 'Bool:Min:1'
         },
         (vim.vm.FeatureRequirement) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            key = 'cpuid.Intel',
            featureName = 'cpuid.Intel',
            value = 'Bool:Min:1'
         }
      ],
      featureMask = (vim.host.FeatureMask) [],
      vFlashCacheAllocation = 0L,
      paused = false,
      snapshotInBackground = false,
      quiescedForkParent = <unset>
   },
   guest = (vim.vm.Summary.GuestSummary) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      guestId = <unset>,
      guestFullName = <unset>,
      toolsStatus = 'toolsNotInstalled',
      toolsVersionStatus = 'guestToolsNotInstalled',
      toolsVersionStatus2 = 'guestToolsNotInstalled',
      toolsRunningStatus = 'guestToolsNotRunning',
      hostName = <unset>,
      ipAddress = <unset>
   },
   config = (vim.vm.Summary.ConfigSummary) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      name = 'test_clone',
      template = false,
      vmPathName = '[9-data] test_clone/test_clone.vmx',
      memorySizeMB = 4096,
      cpuReservation = 0,
      memoryReservation = 0,
      numCpu = 1,
      numEthernetCards = 1,
      numVirtualDisks = 1,
      uuid = '421f1df1-cd10-74c7-35c8-b9d0d77bbdfc',
      instanceUuid = '501f54b3-f8b7-e566-2360-265ee5155a05',
      guestId = 'windows7Server64Guest',
      guestFullName = 'Microsoft Windows Server 2008 R2 (64-bit)',
      annotation = '',
      product = <unset>,
      installBootRequired = false,
      ftInfo = <unset>,
      managedBy = <unset>
   },
   storage = (vim.vm.Summary.StorageSummary) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      committed = 4494330848L,
      uncommitted = 42949673481L,
      unshared = 4494330848L,
      timestamp = 2017-07-19T08:48:09.8151Z
   },
   quickStats = (vim.vm.Summary.QuickStats) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      overallCpuUsage = 0,
      overallCpuDemand = 0,
      guestMemoryUsage = 0,
      hostMemoryUsage = 19,
      guestHeartbeatStatus = 'gray',
      distributedCpuEntitlement = 0,
      distributedMemoryEntitlement = 0,
      staticCpuEntitlement = 0,
      staticMemoryEntitlement = 0,
      privateMemory = 1,
      sharedMemory = 5,
      swappedMemory = 0,
      balloonedMemory = 0,
      consumedOverheadMemory = 19,
      ftLogBandwidth = -1,
      ftSecondaryLatency = -1,
      ftLatencyStatus = 'gray',
      compressedMemory = 0L,
      uptimeSeconds = 175788,
      ssdSwappedMemory = 0L
   },
   overallStatus = 'green',
   customValue = (vim.CustomFieldsManager.Value) []
    """
    vcenterVirtualMachineModel.name = summary.config.name
    vcenterVirtualMachineModel.vm_pathname = summary.config.vmPathName
    vcenterVirtualMachineModel.guest_fullname = summary.config.guestFullName
    vcenterVirtualMachineModel.power_state = summary.runtime.powerState
    vcenterVirtualMachineModel.instance_uuid = summary.config.instanceUuid
    vcenterVirtualMachineModel.memorySizeMB = summary.config.memorySizeMB

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
        if ip != None and ip != "":
            vcenterVirtualMachineModel.ipaddress = ip
    else:
        vcenterVirtualMachineModel.ipaddress=""
    return vcenterVirtualMachineModel


"""
封装端口组相关属性
"""
class PortgroupVO(object):
    def __init__(self):
        pass

"""
端口属性： pgs = host.config.network.portgroup
"""
def convertPortGroupEntityToPortGroupVo(pgs):
    if pgs is None:
        return None
    if pgs is not None and len(pgs)>0:
        for portgroup in pgs:
            hostPortGroupPorts = portgroup.port
            if hostPortGroupPorts is not None and len(hostPortGroupPorts)>0:
                for hostPortGroupPort in hostPortGroupPorts:
                    macs = hostPortGroupPort.mac
                    if macs is not None and len(macs)>0:
                        for mac in macs:
                            print "mac is %s" % mac

            portGroupSpec = portgroup.spec
            if portGroupSpec is not  None:
                print "port group is %s" %portGroupSpec.name
                print "vlanId is %s" % portGroupSpec.vlanId
                print "vswitchName is %s" %portGroupSpec.vswitchName
                hostNetworkPolicy  = portGroupSpec.policy

                hostNetOffloadCapabilities = hostNetworkPolicy.offloadPolicy
                if hostNetOffloadCapabilities is not None:
                    print "hostNetOffloadCapabilities info "
                    print hostNetOffloadCapabilities.csumOffload
                    print hostNetOffloadCapabilities.tcpSegmentation
                    print hostNetOffloadCapabilities.zeroCopyXmit

                hostNetworkSecurityPolicy = hostNetworkPolicy.security
                if hostNetworkSecurityPolicy is not None:
                    print "hostNetworkSecurityPolicy info "
                    print hostNetworkSecurityPolicy.allowPromiscuous
                    print hostNetworkSecurityPolicy.forgedTransmits
                    print hostNetworkSecurityPolicy.macChanges

                hostNetworkTrafficShapingPolicy = hostNetworkPolicy.shapingPolicy
                if hostNetworkTrafficShapingPolicy is not None:
                    print "hostNetworkTrafficShapingPolicy info "
                    print hostNetworkTrafficShapingPolicy.averageBandwidth
                    print hostNetworkTrafficShapingPolicy.burstSize
                    print hostNetworkTrafficShapingPolicy.enabled
                    print hostNetworkTrafficShapingPolicy.peakBandwidth

                if hostNetworkPolicy is not None:
                    hostNicTeamingPolicy = hostNetworkPolicy.nicTeaming
                    if hostNicTeamingPolicy is not None:
                        reversePolicy = hostNicTeamingPolicy.reversePolicy
                        rollingOrder = hostNicTeamingPolicy.rollingOrder
                        notifySwitches = hostNicTeamingPolicy.notifySwitches
                        policy = hostNicTeamingPolicy.policy
                        print "notifySwitches is %s" % notifySwitches
                        print "policy is %s" % policy

                        print "reversePolicy is %s" % reversePolicy
                        print "rollingOrder is %s" % rollingOrder

                        hostNicFailureCriteria = hostNicTeamingPolicy.failureCriteria
                        if hostNicFailureCriteria is not None:
                            print "hostNicFailureCriteria info"
                            print hostNicFailureCriteria.checkBeacon
                            print hostNicFailureCriteria.checkDuplex
                            print hostNicFailureCriteria.checkErrorPercent
                            print hostNicFailureCriteria.checkSpeed
                            print hostNicFailureCriteria.fullDuplex
                            print hostNicFailureCriteria.percentage
                            print hostNicFailureCriteria.speed

                        hostNicOrderPolicy = hostNicTeamingPolicy.nicOrder
                        if hostNicOrderPolicy is not None:
                            print "hostNicOrderPolicy info "
                            print hostNicOrderPolicy.activeNic
                            print hostNicOrderPolicy.standbyNic
