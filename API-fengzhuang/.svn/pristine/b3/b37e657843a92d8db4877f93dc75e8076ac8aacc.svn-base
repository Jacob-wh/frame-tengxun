# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'home_application.vmware.views',
    #视图处理
    url(r'^vm/manage$', 'getVmManageView'),
    url(r'^host/manage$', 'getHostManageView'),
    url(r'^cluster/manage$', 'getClusterManageView'),
    url(r'^datacenter/manage$', 'getDatacenterManageView'),
    url(r'^department/manage', 'getDepartmentManageView'),
    url(r'^department/resource/manage', 'getDepartmentResourceManageView'),
    url(r'^user/manage', 'getUserManageView'),
    url(r'^storage/manage$', 'getStorageManageView'),
    url(r'^network/manage$', 'getNetworkManageView'),
    url(r'^webssh/manage$', 'getWebsshView'),

    #配置类
    url(r'^monitor/config$', 'getMonitorConfigView'),
    url(r'^system/config$', 'getVmConfigView'),

    #表格
    url(r'api/getVcenterAccountList$', 'getVcenterAccountList'),
    url(r'api/getVcenterDatacenterList$', 'getVcenterDatacenterList'),
    url(r'api/getVcenterClusterList$', 'getVcenterClusterList'),
    url(r'api/getVcenterDatastoreList$', 'getVcenterDatastoreList'),
    url(r'api/getVcenterNetworkList$', 'getVcenterNetworkList'),
    url(r'api/getVcenterHostList$', 'getVcenterHostList'),



    #管理类
    url(r'api/deleteAccount', 'deleteAccount'),
    url(r'api/desctroyAccount', 'desctroyAccount'),
    url(r'api/createVCenterAccount$', 'createVCenterAccount'),
    url(r'api/syncCloudAccount', 'syncCloudAccount'),
    url(r'api/getVcenterVirtualMachineList', 'getVcenterVirtualMachineList'),
    url(r'api/create$', 'createVmRequest'),
    url(r'api/clone', 'cloneVmRequest'),
    url(r'api/poweroff', 'poweroffVmRequest'),
    url(r'api/start', 'startVmRequest'),
    url(r'api/reboot', 'rebootVmRequest'),
    url(r'api/destroy', 'destroyVmRequest'),
    url(r'api/getAppList', 'getAppList'),
    url(r'api/getAllDatacenter', 'getAllDatacenterRequest'),
    url(r'api/getAllCluster', 'getAllClusterRequest'),
    url(r'api/getAllDatastore', 'getAllDatastoreRequest'),
    url(r'api/getClusterByDatacenter', 'getClusterByDatacenterRequest'),
    url(r'api/updateVMConfiguration', 'updateVMConfigurationRequest'),
    url(r'api/createVMSnapshot', 'createVMSnapshotRequest'),
    url(r'api/getVMSnapshotList', 'getVMSnapshotListRequest'),
    url(r'api/revertToSnapshot', 'revertToSnapshotRequest'),
    url(r'api/removeAllSnapshots', 'removeAllSnapshotsRequest'),
    url(r'api/removeSnapshot', 'removeSnapshotRequest'),




    #资源分析
    url(r'api/getFlowAnalysis', 'getFlowAnalysisRequest'),
    url(r'api/getMemoryAnalysis', 'getMemoryAnalysisRequest'),
    url(r'api/getCpuAnalysis', 'getCpuAnalysisRequest'),
    url(r'api/getStorageAnalysis', 'getStorageAnalysisRequest'),
    url(r'api/getVmMonitorInfos', 'getVmMonitorInfosRequest'),
    url(r'api/getHostMonitorInfos', 'getHostMonitorInfosRequest'),


    #测试api
    url(r'api/async', 'asyncDemo'),


)
